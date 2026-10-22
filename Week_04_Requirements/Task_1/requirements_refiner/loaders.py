"""Deterministic recursive loading and paragraph-aware chunking."""

from __future__ import annotations

import hashlib
import re
from email import policy
from email.message import Message
from email.parser import BytesParser
from email.utils import parsedate_to_datetime
from html.parser import HTMLParser
from pathlib import Path

from .schemas import DocumentChunk, FileType, SourceDocument

SUPPORTED_SUFFIXES = {".txt": FileType.TXT, ".eml": FileType.EML}


class DocumentLoadError(ValueError):
    """A supported source document could not be decoded or parsed."""


class _HTMLTextExtractor(HTMLParser):
    _NON_VISIBLE_TAGS = {
        "head",
        "script",
        "style",
        "noscript",
        "template",
        "svg",
        "canvas",
    }
    _VOID_TAGS = {
        "area",
        "base",
        "br",
        "col",
        "embed",
        "hr",
        "img",
        "input",
        "link",
        "meta",
        "param",
        "source",
        "track",
        "wbr",
    }

    def __init__(self) -> None:
        super().__init__()
        self.parts: list[str] = []
        self._visibility_stack: list[tuple[str, bool]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attributes = {name.casefold(): (value or "") for name, value in attrs}
        style = re.sub(r"\s+", "", attributes.get("style", "").casefold())
        hidden = (
            (self._visibility_stack[-1][1] if self._visibility_stack else False)
            or tag.casefold() in self._NON_VISIBLE_TAGS
            or "hidden" in attributes
            or attributes.get("aria-hidden", "").casefold() == "true"
            or "display:none" in style
            or "visibility:hidden" in style
        )
        normalized_tag = tag.casefold()
        if normalized_tag not in self._VOID_TAGS:
            self._visibility_stack.append((normalized_tag, hidden))

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.handle_starttag(tag, attrs)
        self.handle_endtag(tag)

    def handle_endtag(self, tag: str) -> None:
        wanted = tag.casefold()
        for index in range(len(self._visibility_stack) - 1, -1, -1):
            if self._visibility_stack[index][0] == wanted:
                del self._visibility_stack[index:]
                break

    def handle_data(self, data: str) -> None:
        hidden = self._visibility_stack and self._visibility_stack[-1][1]
        if not hidden and data.strip():
            self.parts.append(data.strip())

    def text(self) -> str:
        return "\n\n".join(self.parts)


def normalize_text(text: str) -> str:
    """Normalize line endings and whitespace while retaining paragraphs."""

    text = text.replace("\r\n", "\n").replace("\r", "\n").replace("\x00", "")
    lines = [line.rstrip() for line in text.split("\n")]
    normalized = "\n".join(lines).strip()
    return re.sub(r"\n[ \t]*\n(?:[ \t]*\n)+", "\n\n", normalized)


def _split_oversized_paragraph(paragraph: str, char_limit: int) -> list[str]:
    """Split at sentence boundaries, preserving a single oversized sentence."""

    if len(paragraph) <= char_limit:
        return [paragraph]
    sentences = [
        sentence.strip()
        for sentence in re.split(r"(?<=[.!?])\s+(?=[^\s])", paragraph)
        if sentence.strip()
    ]
    if len(sentences) <= 1:
        return [paragraph]

    pieces: list[str] = []
    current = ""
    for sentence in sentences:
        proposal = f"{current} {sentence}".strip()
        if current and len(proposal) > char_limit:
            pieces.append(current)
            current = sentence
        else:
            current = proposal
    if current:
        pieces.append(current)
    return pieces


def chunk_text(
    text: str,
    source_id: str,
    *,
    char_limit: int = 8000,
    overlap_paragraphs: int = 1,
) -> list[DocumentChunk]:
    """Create stable chunks without splitting ordinary paragraphs or sentences."""

    if char_limit < 1:
        raise ValueError("char_limit must be positive")
    if overlap_paragraphs < 0:
        raise ValueError("overlap_paragraphs cannot be negative")

    normalized = normalize_text(text)
    if not normalized:
        raise DocumentLoadError(f"Source {source_id!r} has no textual content")

    raw_paragraphs = [part.strip() for part in re.split(r"\n\s*\n", normalized)]
    paragraphs = [
        piece
        for paragraph in raw_paragraphs
        for piece in _split_oversized_paragraph(paragraph, char_limit)
        if piece
    ]

    groups: list[list[str]] = []
    current: list[str] = []
    current_size = 0
    for paragraph in paragraphs:
        separator_size = 2 if current else 0
        if current and current_size + separator_size + len(paragraph) > char_limit:
            groups.append(current)
            overlap = current[-overlap_paragraphs:] if overlap_paragraphs else []
            # Do not let overlap alone prevent the next paragraph from fitting.
            while overlap and len("\n\n".join([*overlap, paragraph])) > char_limit:
                overlap = overlap[1:]
            current = list(overlap)
            current_size = len("\n\n".join(current))
            separator_size = 2 if current else 0
        current.append(paragraph)
        current_size += separator_size + len(paragraph)
    if current:
        groups.append(current)

    return [
        DocumentChunk(
            chunk_id=f"{source_id}#chunk-{index + 1:04d}",
            source_id=source_id,
            chunk_index=index,
            text="\n\n".join(group),
        )
        for index, group in enumerate(groups)
    ]


def discover_source_files(input_dir: str | Path) -> list[Path]:
    """Validate a directory and return supported files in stable order."""

    root = Path(input_dir)
    if not root.exists():
        raise FileNotFoundError(f"Input directory does not exist: {root}")
    if not root.is_dir():
        raise NotADirectoryError(f"Input path is not a directory: {root}")

    paths = [
        path
        for path in root.rglob("*")
        if path.is_file() and path.suffix.casefold() in SUPPORTED_SUFFIXES
    ]
    paths.sort(key=lambda path: (path.relative_to(root).as_posix().casefold(), path.as_posix()))
    if not paths:
        raise ValueError(f"Input directory contains no supported .txt or .eml files: {root}")
    return paths


def _decode_utf8(raw: bytes, source_id: str) -> str:
    try:
        return raw.decode("utf-8-sig")
    except UnicodeDecodeError as exc:
        raise DocumentLoadError(
            f"Unable to decode {source_id!r} as UTF-8 or UTF-8-SIG"
        ) from exc


def _plain_email_parts(message: Message) -> list[str]:
    parts: list[str] = []
    if message.is_multipart():
        for part in message.walk():
            if part.is_multipart():
                continue
            if _is_attachment_or_named(part):
                continue
            if part.get_content_type() == "text/plain":
                parts.append(_message_part_text(part))
    elif message.get_content_type() == "text/plain" and not _is_attachment_or_named(message):
        parts.append(_message_part_text(message))
    return [part for part in parts if part.strip()]


def _is_attachment_or_named(part: Message) -> bool:
    """Reject attachments and named MIME leaves, including inline files."""

    return part.get_content_disposition() == "attachment" or part.get_filename() is not None


def _message_part_text(part: Message) -> str:
    try:
        content = part.get_content()
    except (LookupError, UnicodeDecodeError) as exc:
        raise DocumentLoadError("Unable to decode an e-mail body as text") from exc
    if isinstance(content, bytes):
        charset = part.get_content_charset() or "utf-8"
        try:
            return content.decode(charset)
        except (LookupError, UnicodeDecodeError) as exc:
            raise DocumentLoadError("Unable to decode an e-mail body as text") from exc
    return str(content)


def _html_email_text(message: Message) -> str:
    html_parts: list[str] = []
    leaves = message.walk() if message.is_multipart() else [message]
    for part in leaves:
        if part.is_multipart() or _is_attachment_or_named(part):
            continue
        if part.get_content_type() == "text/html":
            html_parts.append(_message_part_text(part))
    extractor = _HTMLTextExtractor()
    for html in html_parts:
        extractor.feed(html)
    return extractor.text()


def _email_date(message: Message) -> str | None:
    header = message.get("Date")
    if header is None or not str(header).strip():
        return None
    value = str(header).strip()
    try:
        parsed = parsedate_to_datetime(value)
    except (TypeError, ValueError, OverflowError):
        return value
    return parsed.isoformat()


def _parse_eml(raw: bytes, source_id: str, fallback_title: str) -> tuple[str, str | None, str]:
    # A UTF-8 BOM before the first header is not part of RFC 5322 and would make
    # the parser treat the header block as body text. Accept it because UTF-8-SIG
    # is an explicitly supported source encoding.
    parser_input = raw[3:] if raw.startswith(b"\xef\xbb\xbf") else raw
    try:
        message = BytesParser(policy=policy.default).parsebytes(parser_input)
    except Exception as exc:  # email parser can surface several malformed-message errors
        raise DocumentLoadError(f"Unable to parse e-mail {source_id!r}: {exc}") from exc

    subject = normalize_text(str(message.get("Subject", ""))) or fallback_title
    body_parts = _plain_email_parts(message)
    body = "\n\n".join(body_parts) if body_parts else _html_email_text(message)
    body = normalize_text(body)
    if not body:
        raise DocumentLoadError(f"E-mail {source_id!r} has no readable text body")
    return subject, _email_date(message), body


def load_document(
    path: str | Path,
    input_dir: str | Path,
    *,
    char_limit: int = 8000,
    overlap_paragraphs: int = 1,
) -> SourceDocument:
    """Load one supported source file relative to ``input_dir``."""

    root = Path(input_dir).resolve()
    source_path = Path(path).resolve()
    try:
        source_id = source_path.relative_to(root).as_posix()
    except ValueError as exc:
        raise ValueError(f"Source file is outside the input directory: {source_path}") from exc

    suffix = source_path.suffix.casefold()
    if suffix not in SUPPORTED_SUFFIXES:
        raise ValueError(f"Unsupported source type for {source_id!r}")

    try:
        raw = source_path.read_bytes()
    except OSError as exc:
        raise DocumentLoadError(f"Unable to read {source_id!r}: {exc}") from exc
    fallback_title = source_path.stem.replace("_", " ").replace("-", " ").strip()

    if suffix == ".txt":
        title = fallback_title
        date = None
        content = normalize_text(_decode_utf8(raw, source_id))
        if not content:
            raise DocumentLoadError(f"Text file {source_id!r} is empty")
    else:
        title, date, content = _parse_eml(raw, source_id, fallback_title)

    chunks = chunk_text(
        content,
        source_id,
        char_limit=char_limit,
        overlap_paragraphs=overlap_paragraphs,
    )
    return SourceDocument(
        source_id=source_id,
        file_type=SUPPORTED_SUFFIXES[suffix],
        title=title,
        date=date,
        content=content,
        chunks=chunks,
        sha256=hashlib.sha256(raw).hexdigest(),
    )


def load_documents(
    input_dir: str | Path,
    *,
    char_limit: int = 8000,
    overlap_paragraphs: int = 1,
) -> list[SourceDocument]:
    """Recursively load all supported files from a directory."""

    root = Path(input_dir)
    return [
        load_document(
            path,
            root,
            char_limit=char_limit,
            overlap_paragraphs=overlap_paragraphs,
        )
        for path in discover_source_files(root)
    ]


def build_source_manifest(documents: list[SourceDocument]) -> list[str]:
    """Return a stable allow-list of source IDs for prompts and validation."""

    return sorted({document.source_id for document in documents}, key=str.casefold)

