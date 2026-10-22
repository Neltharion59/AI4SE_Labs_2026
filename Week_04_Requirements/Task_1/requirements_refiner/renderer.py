"""Deterministic Markdown rendering for the refined requirements document."""

from __future__ import annotations

import html
import os
import re
import tempfile
from collections.abc import Iterable, Mapping, Sequence
from enum import Enum
from pathlib import Path
from typing import Any

from .schemas import BlacklistEntry, RequirementCategory, RequirementDraft
from .validation import normalize_exact_text


CATEGORY_ORDER = (
    RequirementCategory.FUNCTIONAL,
    RequirementCategory.NON_FUNCTIONAL,
    RequirementCategory.CONSTRAINT,
    RequirementCategory.DOCUMENTATION,
    RequirementCategory.DEPENDENCY,
)

CATEGORY_INFO = {
    RequirementCategory.FUNCTIONAL: ("Functional Requirements", "FUN"),
    RequirementCategory.NON_FUNCTIONAL: ("Non-functional Requirements", "NFR"),
    RequirementCategory.CONSTRAINT: ("Constraints", "CON"),
    RequirementCategory.DOCUMENTATION: ("Documentation Requirements", "DOC"),
    RequirementCategory.DEPENDENCY: ("Dependencies and Assumptions", "DEP"),
}


def _value(item: object, field: str, default: Any = None) -> Any:
    if isinstance(item, Mapping):
        return item.get(field, default)
    return getattr(item, field, default)


def _text(value: object) -> str:
    return str(value).strip() if value is not None else ""


def _enum_value(value: object) -> object:
    return value.value if isinstance(value, Enum) else value


def _category(value: object) -> RequirementCategory:
    return value if isinstance(value, RequirementCategory) else RequirementCategory(_enum_value(value))


def _source_ids(source_manifest: Iterable[object] | Mapping[str, object]) -> list[str]:
    values: Iterable[object]
    if isinstance(source_manifest, Mapping):
        values = source_manifest.keys()
    else:
        values = source_manifest
    return sorted(
        {
            source_id
            for item in values
            if (source_id := _text(_value(item, "source_id", item)))
        },
        key=lambda value: (value.casefold(), value),
    )


_MARKDOWN_PUNCTUATION = re.compile(r"([\\`*_{}\[\]()#+\-.!|~:@])")


def _normalized_inline(value: object) -> str:
    """Normalize arbitrary input to one plain-text line."""

    return " ".join(_text(value).replace("\r\n", "\n").replace("\r", "\n").split())


def _escape_plain_text(value: str) -> str:
    """Neutralize HTML and Markdown while retaining readable rendered text.

    Dynamic/model-controlled values never supply document structure. HTML is
    encoded first, then Markdown punctuation (including constructs used by
    headings, lists, links, images, tables, quotes, and code) is escaped.
    """

    html_safe = html.escape(value, quote=False)
    return _MARKDOWN_PUNCTUATION.sub(r"\\\1", html_safe)


def _md_inline(value: object) -> str:
    return _escape_plain_text(_normalized_inline(value))


def _md_block(value: object) -> str:
    """Render plain-text paragraphs without allowing multiline block injection."""

    normalized = _text(value).replace("\r\n", "\n").replace("\r", "\n")
    paragraphs = re.split(r"\n\s*\n", normalized)
    rendered = [
        _escape_plain_text(" ".join(part.split()))
        for part in paragraphs
        if part.strip()
    ]
    return "\n\n".join(rendered)


def _md_code(value: object) -> str:
    """Render one untrusted identifier as a safe inline-code span."""

    content = html.escape(_normalized_inline(value), quote=False).replace("|", r"\|")
    longest_run = max((len(match.group(0)) for match in re.finditer(r"`+", content)), default=0)
    delimiter = "`" * (longest_run + 1)
    # CommonMark permits a longer delimiter around embedded backticks. Padding
    # is needed in that case so the embedded run remains literal content.
    padding = " " if longest_run else ""
    return f"{delimiter}{padding}{content}{padding}{delimiter}"


def _code_list(values: Iterable[object]) -> str:
    unique = sorted({_text(value) for value in values if _text(value)}, key=lambda value: (value.casefold(), value))
    return ", ".join(_md_code(value) for value in unique) if unique else "_None_"


def _requirement_sort_key(requirement: RequirementDraft) -> tuple[int, str, str]:
    category = _category(_value(requirement, "category"))
    return (
        CATEGORY_ORDER.index(category),
        normalize_exact_text(_value(requirement, "name")),
        _text(_value(requirement, "draft_id")),
    )


def _blacklist_sort_key(entry: BlacklistEntry) -> tuple[str, str]:
    return (normalize_exact_text(_value(entry, "name")), _text(_value(entry, "draft_id")))


def assign_stable_ids(
    requirements: Sequence[RequirementDraft],
    blacklist: Sequence[BlacklistEntry],
) -> tuple[list[tuple[str, RequirementDraft]], list[tuple[str, BlacklistEntry]]]:
    """Assign display IDs without mutating the structured draft objects."""

    counters = {category: 0 for category in CATEGORY_ORDER}
    assigned_requirements: list[tuple[str, RequirementDraft]] = []
    for requirement in sorted(requirements, key=_requirement_sort_key):
        category = _category(_value(requirement, "category"))
        counters[category] += 1
        prefix = CATEGORY_INFO[category][1]
        assigned_requirements.append((f"REQ-{prefix}-{counters[category]:03d}", requirement))

    assigned_blacklist = [
        (f"BL-{index:03d}", entry)
        for index, entry in enumerate(sorted(blacklist, key=_blacklist_sort_key), start=1)
    ]
    return assigned_requirements, assigned_blacklist


def render_markdown(
    requirements: Sequence[RequirementDraft],
    blacklist: Sequence[BlacklistEntry],
    source_manifest: Iterable[object] | Mapping[str, object],
    glossary: Mapping[str, str] | None = None,
    metadata: Mapping[str, object] | None = None,
    warning: str | None = None,
) -> str:
    """Create the complete single Markdown deliverable in a reproducible order."""

    assigned, assigned_blacklist = assign_stable_ids(list(requirements or []), list(blacklist or []))
    sources = _source_ids(source_manifest)
    lines = [
        "# Software Requirements Specification",
        "",
        "## Document Information",
        "",
        "This document was generated from the supplied source corpus by the requirements-refinement network.",
    ]

    if metadata:
        for key, value in sorted(metadata.items(), key=lambda pair: (str(pair[0]).casefold(), str(pair[0]))):
            lines.append(f"- **{_md_inline(key)}:** {_md_inline(value)}")
    if warning:
        lines.extend(["", f"> **Validation warning:** {_md_inline(warning)}"])

    lines.extend(
        [
            "",
            "## Purpose and Scope",
            "",
            "The specification consolidates software capabilities, quality attributes, constraints, documentation needs, and dependencies found in the input documents. Each item retains traceability to its source documents.",
            "",
            "## Priority Scale",
            "",
            "- **High** — Essential for the intended system outcome or a mandatory constraint; omission would make the solution unacceptable.",
            "- **Medium** — Important and expected, but the solution can still provide core value if delivery is deferred.",
            "- **Low** — Optional enhancement whose deferral has limited effect on core operation.",
            "",
            "## Glossary and Terminology",
            "",
        ]
    )
    if glossary:
        for term, definition in sorted(glossary.items(), key=lambda pair: (str(pair[0]).casefold(), str(pair[0]))):
            lines.append(f"- **{_md_inline(term)}:** {_md_inline(definition)}")
    else:
        lines.append(
            "Requirement names and descriptions use the terminology selected during consolidation; the same concept should be named consistently throughout this document."
        )

    lines.extend(["", "## Requirements", ""])
    grouped: dict[RequirementCategory, list[tuple[str, RequirementDraft]]] = {
        category: [] for category in CATEGORY_ORDER
    }
    for assigned_id, requirement in assigned:
        grouped[_category(_value(requirement, "category"))].append((assigned_id, requirement))

    for category in CATEGORY_ORDER:
        title = CATEGORY_INFO[category][0]
        lines.extend([f"### {title}", ""])
        if not grouped[category]:
            lines.extend(["_No requirements in this category._", ""])
            continue
        for assigned_id, requirement in grouped[category]:
            lines.extend(
                [
                    f"#### {assigned_id} — {_md_inline(_value(requirement, 'name'))}",
                    "",
                    f"**Priority:** {_md_inline(_enum_value(_value(requirement, 'priority')))}  ",
                    f"**Sources:** {_code_list(_value(requirement, 'source_refs', []) or [])}  ",
                    f"**Priority rationale:** {_md_inline(_value(requirement, 'priority_rationale'))}",
                    "",
                    _md_block(_value(requirement, "description")),
                ]
            )
            conflict_resolution = _text(_value(requirement, "conflict_resolution"))
            verification_hint = _text(_value(requirement, "verification_hint"))
            if conflict_resolution:
                lines.extend(["", f"**Conflict resolution:** {_md_inline(conflict_resolution)}"])
            if verification_hint:
                lines.extend(["", f"**Verification hint:** {_md_inline(verification_hint)}"])
            lines.append("")

    lines.extend(["## Blacklist", ""])
    if not assigned_blacklist:
        lines.extend(["_No identified requirements were discarded._", ""])
    else:
        for assigned_id, entry in assigned_blacklist:
            lines.extend(
                [
                    f"### {assigned_id} — {_md_inline(_value(entry, 'name'))}",
                    "",
                    f"**Classification:** {_md_inline(_enum_value(_value(entry, 'classification')))}  ",
                    f"**Sources:** {_code_list(_value(entry, 'source_refs', []) or [])}  ",
                    f"**Reason:** {_md_inline(_value(entry, 'reason'))}",
                    "",
                    _md_block(_value(entry, "description")),
                    "",
                ]
            )

    lines.extend(
        [
            "## Traceability Matrix",
            "",
            "| ID | Type | Sources | Extracted Item IDs |",
            "|---|---|---|---|",
        ]
    )
    for assigned_id, requirement in assigned:
        lines.append(
            f"| {assigned_id} | Requirement | {_code_list(_value(requirement, 'source_refs', []) or [])} | "
            f"{_code_list(_value(requirement, 'merged_candidate_ids', []) or [])} |"
        )
    for assigned_id, entry in assigned_blacklist:
        lines.append(
            f"| {assigned_id} | Blacklist | {_code_list(_value(entry, 'source_refs', []) or [])} | "
            f"{_code_list(_value(entry, 'candidate_ids', []) or [])} |"
        )
    if not assigned and not assigned_blacklist:
        lines.append("| — | — | _None_ | _None_ |")

    coverage: dict[str, list[str]] = {source: [] for source in sources}
    for assigned_id, item in [*assigned, *assigned_blacklist]:
        for source in {_text(ref) for ref in (_value(item, "source_refs", []) or []) if _text(ref)}:
            coverage.setdefault(source, []).append(assigned_id)

    lines.extend(
        [
            "",
            "## Source Coverage",
            "",
            f"The input manifest contains **{len(sources)}** source document(s).",
            "",
            "| Source document | Derived requirement or blacklist IDs |",
            "|---|---|",
        ]
    )
    for source in sources:
        linked = sorted(coverage.get(source, []))
        rendered = ", ".join(linked) if linked else "_No derived item_"
        lines.append(f"| {_md_code(source)} | {rendered} |")
    if not sources:
        lines.append("| _No sources in manifest_ | _No derived item_ |")

    return "\n".join(lines).rstrip() + "\n"


def write_markdown(path: str | Path, text: str) -> Path:
    """Atomically write a complete UTF-8 Markdown document."""

    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    temporary_path: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            newline="\n",
            delete=False,
            dir=output_path.parent,
            prefix=f".{output_path.name}.",
            suffix=".tmp",
        ) as handle:
            handle.write(text)
            handle.flush()
            os.fsync(handle.fileno())
            temporary_path = Path(handle.name)
        os.replace(temporary_path, output_path)
    except Exception:
        if temporary_path is not None:
            temporary_path.unlink(missing_ok=True)
        raise
    return output_path


__all__ = [
    "CATEGORY_INFO",
    "CATEGORY_ORDER",
    "assign_stable_ids",
    "render_markdown",
    "write_markdown",
]
