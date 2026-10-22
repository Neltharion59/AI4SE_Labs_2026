"""Command-line entry point for the requirements-refinement network."""

from __future__ import annotations

import argparse
import os
import re
import sys
from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any, TextIO

from requirements_refiner.config import Settings
from requirements_refiner.graph import build_graph, invoke_graph
from requirements_refiner.llm_factory import LLMClients, create_llm_clients
from requirements_refiner.loaders import discover_source_files


class CLIError(Exception):
    """An actionable input or configuration error."""


@dataclass(frozen=True)
class RunResult:
    """Small, presentation-neutral summary of a completed graph invocation."""

    state: Mapping[str, Any]
    settings: Settings
    output_path: Path


ProgressCallback = Callable[[str], None]


def _resolve_safe_paths(input_dir: Path, output_path: Path) -> tuple[Path, Path]:
    """Resolve CLI paths and keep generated output outside the source corpus."""

    try:
        input_root = input_dir.resolve(strict=False)
        resolved_output = output_path.resolve(strict=False)
    except (OSError, RuntimeError) as exc:
        raise CLIError(f"Could not resolve input or output path: {exc}") from exc

    if resolved_output == input_root or input_root in resolved_output.parents:
        raise CLIError(
            "Output must be outside the input directory to prevent overwriting "
            "source documents."
        )
    return input_root, resolved_output


def build_parser() -> argparse.ArgumentParser:
    """Create the documented CLI parser."""

    parser = argparse.ArgumentParser(
        description=(
            "Refine a directory of .txt and .eml source documents into one "
            "traceable Markdown requirements specification."
        )
    )
    parser.add_argument(
        "--input-dir",
        required=True,
        type=Path,
        help="directory to scan recursively for .txt and .eml source documents",
    )
    parser.add_argument(
        "--output",
        required=True,
        type=Path,
        help="path of the generated Markdown document",
    )
    return parser


def run(
    args: argparse.Namespace,
    *,
    settings_factory: Callable[[], Settings] = Settings,
    client_factory: Callable[[Settings], LLMClients] = create_llm_clients,
    graph_builder: Callable[..., Any] = build_graph,
    graph_invoker: Callable[..., Mapping[str, Any]] = invoke_graph,
    source_discovery: Callable[[str | Path], Sequence[Path]] = discover_source_files,
    progress: ProgressCallback | None = None,
) -> RunResult:
    """Validate, construct, and invoke the pipeline.

    Dependencies are injectable so CLI orchestration can be tested without a
    network connection. Real runs still require ``OPENAI_API_KEY`` before any
    clients are created.
    """

    report = progress or (lambda _message: None)
    input_dir, output_path = _resolve_safe_paths(
        Path(args.input_dir),
        Path(args.output),
    )

    report(f"Validating input directory: {input_dir}")
    try:
        source_files = list(source_discovery(input_dir))
    except (FileNotFoundError, NotADirectoryError, OSError, ValueError) as exc:
        raise CLIError(str(exc)) from exc
    if not source_files:
        # The production discovery function already enforces this. Keep the
        # guard for injected implementations and clearer orchestration tests.
        raise CLIError(
            f"Input directory contains no supported .txt or .eml files: {input_dir}"
        )

    report(f"Found {len(source_files)} supported source file(s).")
    try:
        settings = settings_factory()
        settings.require_api_key()
    except ValueError as exc:
        raise CLIError(str(exc)) from exc

    report(
        "Initializing models: "
        f"{settings.extractor_model}, {settings.consolidator_model}, "
        f"{settings.reviewer_model}"
    )
    clients = client_factory(settings)
    graph = graph_builder(settings=settings, clients=clients)
    report("Running extraction, consolidation, review, and rendering.")
    state = graph_invoker(
        graph,
        input_dir=input_dir,
        output_path=output_path,
        max_review_iterations=None,
    )
    return RunResult(
        state=state,
        settings=settings,
        output_path=output_path,
    )


def _safe_error_message(error: BaseException) -> str:
    """Render an error without echoing a configured API credential."""

    message = str(error).strip() or error.__class__.__name__
    configured_key = os.environ.get("OPENAI_API_KEY", "")
    if configured_key:
        message = message.replace(configured_key, "[REDACTED]")
    return re.sub(r"\bsk-[A-Za-z0-9_-]{8,}\b", "[REDACTED]", message)


def _print_success(result: RunResult, stream: TextIO) -> None:
    _print_summary(
        result,
        stream,
        heading="Requirements refinement completed successfully.",
    )


def _print_unresolved(result: RunResult, stream: TextIO) -> None:
    _print_summary(
        result,
        stream,
        heading="Requirements refinement completed with unresolved validation errors.",
    )


def _print_summary(result: RunResult, stream: TextIO, *, heading: str) -> None:
    state = result.state
    stats = dict(state.get("run_stats", {}) or {})

    def count(stat_name: str, state_name: str) -> int:
        value = stats.get(stat_name)
        if value is None:
            value = len(state.get(state_name, []) or [])
        return int(value)

    print(heading, file=stream)
    print(f"Documents: {count('document_count', 'documents')}", file=stream)
    print(f"Extracted items: {count('candidate_count', 'candidates')}", file=stream)
    print(f"Requirements: {count('requirement_count', 'requirements')}", file=stream)
    print(f"Blacklist entries: {count('blacklist_count', 'blacklist')}", file=stream)
    print(
        f"Review iterations: {int(stats.get('review_iterations', state.get('review_iteration', 0)))}",
        file=stream,
    )
    print(
        "Models: "
        f"extract={result.settings.extractor_model}, "
        f"consolidate={result.settings.consolidator_model}, "
        f"review={result.settings.reviewer_model}",
        file=stream,
    )
    print(f"Output: {result.output_path}", file=stream)
    for warning in state.get("warnings", []) or []:
        print(f"Warning: {warning}", file=stream)


def main(argv: Sequence[str] | None = None) -> int:
    """Run the CLI and return a process exit code."""

    args = build_parser().parse_args(argv)
    progress = lambda message: print(f"[info] {message}", file=sys.stderr)

    try:
        result = run(args, progress=progress)
    except CLIError as exc:
        print(f"Error: {_safe_error_message(exc)}", file=sys.stderr)
        return 2
    except Exception as exc:  # noqa: BLE001 - CLI boundary must produce a useful exit code
        print(
            f"Error: requirements refinement failed: {_safe_error_message(exc)}",
            file=sys.stderr,
        )
        return 1

    if result.state.get("validation_passed") is True:
        _print_success(result, sys.stdout)
        return 0

    # Missing status is intentionally treated as unresolved: callers and
    # automation must receive positive confirmation before accepting output.
    _print_unresolved(result, sys.stdout)
    return 3


if __name__ == "__main__":
    raise SystemExit(main())
