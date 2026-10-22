"""LangGraph assembly and deterministic routing for the refinement pipeline."""

from __future__ import annotations

from collections.abc import Callable, Mapping
from pathlib import Path
from typing import Any, Literal

from .config import MAX_REVIEW_ITERATIONS, Settings
from .llm_factory import LLMClients, create_llm_clients
from .loaders import build_source_manifest, load_documents
from .nodes import (
    ConsolidateRequirementsNode,
    ExtractCandidatesNode,
    ReviewQualityNode,
    ReviseRequirementsNode,
)
from .renderer import render_markdown, write_markdown
from .schemas import SourceDocument
from .state import RequirementsState
from .validation import validate_state


REVIEW_NODE = "review_quality"
REVISION_NODE = "revise_requirements"
VALIDATION_NODE = "validate_deterministically"
FINALIZE_NODE = "finalize_best_effort"
RENDER_NODE = "assign_ids_and_render"

ReviewRoute = Literal[
    "revise_requirements",
    "validate_deterministically",
]
ValidationRoute = Literal[
    "revise_requirements",
    "assign_ids_and_render",
    "finalize_best_effort",
]
DocumentLoader = Callable[..., list[SourceDocument]]
MarkdownWriter = Callable[[str | Path, str], Path]


def _revision_budget_remaining(state: Mapping[str, Any]) -> bool:
    iteration = int(state.get("review_iteration", 0))
    maximum = int(state.get("max_review_iterations", MAX_REVIEW_ITERATIONS))
    return iteration < maximum


def _review_value(report: object, field: str, default: Any) -> Any:
    if isinstance(report, Mapping):
        return report.get(field, default)
    return getattr(report, field, default)


def needs_revision(state: Mapping[str, Any]) -> ReviewRoute:
    """Route an LLM review to validation, revision, or bounded finalization."""

    report = state.get("review_report")
    if report is not None and bool(_review_value(report, "approved", False)):
        return VALIDATION_NODE
    if _revision_budget_remaining(state):
        return REVISION_NODE
    # Even a rejected final LLM review must not bypass objective validation.
    # validation_route will send the checked state to bounded best-effort output.
    return VALIDATION_NODE


def validation_route(state: Mapping[str, Any]) -> ValidationRoute:
    """Route objective validation failures back through the same revision loop."""

    report = state.get("review_report")
    review_approved = report is None or bool(_review_value(report, "approved", False))
    if bool(state.get("validation_passed", False)) and review_approved:
        return RENDER_NODE
    if _revision_budget_remaining(state):
        return REVISION_NODE
    return FINALIZE_NODE


def _load_node(
    settings: Settings,
    document_loader: DocumentLoader,
) -> Callable[[Mapping[str, Any]], dict[str, Any]]:
    def load(state: Mapping[str, Any]) -> dict[str, Any]:
        input_dir = state.get("input_dir")
        if not input_dir:
            raise ValueError("The graph requires a non-empty input_dir.")
        documents = document_loader(
            str(input_dir),
            char_limit=settings.chunk_char_limit,
            overlap_paragraphs=settings.chunk_overlap_paragraphs,
        )
        stats = dict(state.get("run_stats", {}))
        stats.update(
            {
                "document_count": len(documents),
                "chunk_count": sum(len(document.chunks) for document in documents),
            }
        )
        return {
            "documents": documents,
            "source_manifest": build_source_manifest(documents),
            "candidates": [],
            "requirements": [],
            "blacklist": [],
            "review_report": None,
            "validation_errors": [],
            "validation_issues": [],
            "validation_passed": False,
            "review_iteration": 0,
            "max_review_iterations": int(
                state.get("max_review_iterations", settings.max_review_iterations)
            ),
            "run_stats": stats,
            "warnings": [],
            "errors": [],
        }

    return load


def _best_effort_node(state: Mapping[str, Any]) -> dict[str, Any]:
    # Keep this node safe even if a future graph edge reaches it directly: the
    # exact draft being rendered is validated here, not an earlier revision.
    validation = validate_state(state)
    report = state.get("review_report")
    review_issue_count = (
        sum(
            len(_review_value(report, field, []) or [])
            for field in (
                "issues",
                "duplicate_pairs",
                "conflicts",
                "missing_candidate_ids",
                "invalid_source_refs",
                "terminology_findings",
                "coverage_findings",
            )
        )
        if report
        else 0
    )
    validation_issues = list(validation["validation_issues"])
    validation_issue_count = len(validation_issues)
    maximum = int(state.get("max_review_iterations", MAX_REVIEW_ITERATIONS))
    stats = dict(state.get("run_stats", {}))
    stats.update(
        {
            "deterministic_validation_status": (
                "passed" if validation["validation_passed"] else "failed"
            ),
            "deterministic_validation_issue_count": validation_issue_count,
        }
    )
    warning = (
        "Best-effort output: the review limit was reached with "
        f"{review_issue_count} review issue(s) and "
        "deterministic validation was evaluated on the final draft and found "
        f"{validation_issue_count} unresolved issue(s) "
        f"after {maximum} permitted revision(s)."
    )
    return {
        "warnings": [*list(state.get("warnings", [])), warning],
        "validation_issues": validation_issues,
        "run_stats": stats,
        "validation_passed": False,
    }


def _render_node(
    clients: LLMClients,
    markdown_writer: MarkdownWriter,
) -> Callable[[Mapping[str, Any]], dict[str, Any]]:
    def render(state: Mapping[str, Any]) -> dict[str, Any]:
        output_path = state.get("output_path")
        if not output_path:
            raise ValueError("The graph requires a non-empty output_path.")
        warnings = list(state.get("warnings", []))
        markdown = render_markdown(
            requirements=list(state.get("requirements", [])),
            blacklist=list(state.get("blacklist", [])),
            source_manifest=list(state.get("source_manifest", [])),
            metadata={
                "Extractor model": clients.extractor_model,
                "Consolidator model": clients.consolidator_model,
                "Reviewer model": clients.reviewer_model,
                "Review revisions": int(state.get("review_iteration", 0)),
            },
            warning=" ".join(warnings) if warnings else None,
        )
        written_path = markdown_writer(str(output_path), markdown)
        stats = dict(state.get("run_stats", {}))
        stats.update(
            {
                "requirement_count": len(state.get("requirements", [])),
                "blacklist_count": len(state.get("blacklist", [])),
                "review_iterations": int(state.get("review_iteration", 0)),
                "output_path": str(written_path),
            }
        )
        return {"final_markdown": markdown, "run_stats": stats}

    return render


def build_graph(
    settings: Settings | None = None,
    clients: LLMClients | None = None,
    *,
    document_loader: DocumentLoader = load_documents,
    markdown_writer: MarkdownWriter = write_markdown,
) -> Any:
    """Build and compile the complete requirements-refinement graph.

    Passing ``clients`` keeps tests and alternative runtimes completely
    offline. When omitted, real structured OpenAI clients are constructed from
    ``settings`` and an API key is required by :func:`create_llm_clients`.
    Input and output locations remain invocation state, so one compiled graph
    can process different corpora without reconstruction.
    """

    try:
        from langgraph.graph import END, START, StateGraph
    except ImportError as exc:  # pragma: no cover - exercised only without extras
        raise RuntimeError(
            "LangGraph is not installed. Install the packages from requirements.txt."
        ) from exc

    resolved_settings = settings or Settings()
    resolved_clients = clients or create_llm_clients(resolved_settings)

    graph = StateGraph(RequirementsState)
    graph.add_node("load_documents", _load_node(resolved_settings, document_loader))
    graph.add_node(
        "extract_candidates",
        ExtractCandidatesNode(
            resolved_clients.extractor,
            resolved_clients.extractor_model,
            batch_size=resolved_settings.extraction_batch_size,
        ),
    )
    graph.add_node(
        "consolidate_requirements",
        ConsolidateRequirementsNode(
            resolved_clients.consolidator,
            resolved_clients.consolidator_model,
        ),
    )
    graph.add_node(
        REVIEW_NODE,
        ReviewQualityNode(resolved_clients.reviewer, resolved_clients.reviewer_model),
    )
    graph.add_node(
        REVISION_NODE,
        ReviseRequirementsNode(resolved_clients.reviser, resolved_clients.consolidator_model),
    )
    graph.add_node(VALIDATION_NODE, validate_state)
    graph.add_node(FINALIZE_NODE, _best_effort_node)
    graph.add_node(RENDER_NODE, _render_node(resolved_clients, markdown_writer))

    graph.add_edge(START, "load_documents")
    graph.add_edge("load_documents", "extract_candidates")
    graph.add_edge("extract_candidates", "consolidate_requirements")
    graph.add_edge("consolidate_requirements", REVIEW_NODE)
    graph.add_conditional_edges(
        REVIEW_NODE,
        needs_revision,
        {
            REVISION_NODE: REVISION_NODE,
            VALIDATION_NODE: VALIDATION_NODE,
        },
    )
    graph.add_edge(REVISION_NODE, REVIEW_NODE)
    graph.add_conditional_edges(
        VALIDATION_NODE,
        validation_route,
        {
            REVISION_NODE: REVISION_NODE,
            RENDER_NODE: RENDER_NODE,
            FINALIZE_NODE: FINALIZE_NODE,
        },
    )
    graph.add_edge(FINALIZE_NODE, RENDER_NODE)
    graph.add_edge(RENDER_NODE, END)
    return graph.compile()


def invoke_graph(
    graph: Any,
    *,
    input_dir: str | Path,
    output_path: str | Path,
    max_review_iterations: int | None = None,
) -> RequirementsState:
    """Invoke a compiled graph with validated path-shaped state inputs."""

    initial_state: RequirementsState = {
        "input_dir": str(input_dir),
        "output_path": str(output_path),
    }
    if max_review_iterations is not None:
        if max_review_iterations < 0:
            raise ValueError("max_review_iterations must be non-negative")
        initial_state["max_review_iterations"] = max_review_iterations
    maximum = (
        MAX_REVIEW_ITERATIONS
        if max_review_iterations is None
        else max_review_iterations
    )
    return graph.invoke(
        initial_state,
        config={"recursion_limit": (2 * maximum) + 10},
    )


__all__ = [
    "build_graph",
    "invoke_graph",
    "needs_revision",
    "validation_route",
]
