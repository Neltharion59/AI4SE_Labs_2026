"""Shared LangGraph state and deterministic reducers."""

from __future__ import annotations

from typing import Annotated, TypedDict

from .schemas import (
    BlacklistEntry,
    CandidateRequirement,
    RequirementDraft,
    ReviewIssue,
    ReviewReport,
    SourceDocument,
)


def add_candidates(
    current: list[CandidateRequirement] | None,
    incoming: list[CandidateRequirement] | None,
) -> list[CandidateRequirement]:
    """Merge parallel extraction results by stable candidate ID.

    Sorting makes the reducer reproducible even when parallel graph branches
    complete in a different order. A repeated ID is accepted only when its
    complete payload is identical; conflicting payloads indicate a programming
    or model-output error and are rejected instead of being silently lost.
    """

    by_id: dict[str, CandidateRequirement] = {}
    for candidate in [*(current or []), *(incoming or [])]:
        previous = by_id.get(candidate.candidate_id)
        if previous is not None and previous != candidate:
            raise ValueError(
                f"Conflicting candidates share ID {candidate.candidate_id!r}"
            )
        by_id[candidate.candidate_id] = candidate
    return [by_id[candidate_id] for candidate_id in sorted(by_id)]


class RequirementsState(TypedDict, total=False):
    input_dir: str
    output_path: str
    documents: list[SourceDocument]
    source_manifest: list[str]
    candidates: Annotated[list[CandidateRequirement], add_candidates]
    requirements: list[RequirementDraft]
    blacklist: list[BlacklistEntry]
    review_report: ReviewReport | None
    validation_errors: list[str]
    validation_issues: list[ReviewIssue]
    validation_passed: bool
    review_iteration: int
    max_review_iterations: int
    run_stats: dict[str, int | float | str]
    final_markdown: str
    warnings: list[str]
    errors: list[str]

