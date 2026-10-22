"""Deterministic quality gates for consolidated requirements.

The checks in this module deliberately cover only objective invariants.  Semantic
duplicates and contradictions remain the responsibility of the reviewer LLM.
"""

from __future__ import annotations

import re
import unicodedata
from collections import Counter
from collections.abc import Iterable, Mapping, Sequence
from enum import Enum
from typing import Any

from .config import MAX_REVIEW_ITERATIONS
from .schemas import (
    BlacklistEntry,
    CandidateRequirement,
    Priority,
    RequirementDraft,
    ReviewIssue,
    ReviewIssueCategory,
    ReviewSeverity,
)


MIN_PARAGRAPH_WORDS = 25
_SENTENCE_END_RE = re.compile(r"[.!?](?:[\"')\]]+)?(?=\s|$)")
_SPACE_RE = re.compile(r"\s+")


def _value(item: object, field: str, default: Any = None) -> Any:
    """Read a field from either a Pydantic model/object or a mapping."""

    if isinstance(item, Mapping):
        return item.get(field, default)
    return getattr(item, field, default)


def _text(value: object) -> str:
    return str(value).strip() if value is not None else ""


def _enum_value(value: object) -> object:
    return value.value if isinstance(value, Enum) else value


def normalize_exact_text(value: object) -> str:
    """Normalize text for deterministic *exact* duplicate detection."""

    normalized = unicodedata.normalize("NFKC", _text(value)).casefold()
    return _SPACE_RE.sub(" ", normalized).strip(" \t\r\n.,;:!?-_")


def _allowed_sources(source_ids: Iterable[object]) -> set[str]:
    result: set[str] = set()
    for source in source_ids:
        source_id = _value(source, "source_id", source)
        if _text(source_id):
            result.add(_text(source_id))
    return result


def _issue(
    severity: ReviewSeverity,
    category: ReviewIssueCategory,
    affected_ids: Iterable[object],
    message: str,
    suggested_fix: str,
) -> ReviewIssue:
    return ReviewIssue(
        severity=severity,
        category=category,
        affected_ids=sorted({_text(item) for item in affected_ids if _text(item)}),
        message=message,
        suggested_fix=suggested_fix,
    )


def _check_required_fields(
    requirements: Sequence[RequirementDraft],
    blacklist: Sequence[BlacklistEntry],
) -> list[ReviewIssue]:
    issues: list[ReviewIssue] = []
    requirement_fields = (
        "draft_id",
        "name",
        "description",
        "priority_rationale",
    )
    blacklist_fields = ("draft_id", "name", "description", "reason", "classification")

    for position, requirement in enumerate(requirements):
        item_id = _text(_value(requirement, "draft_id")) or f"requirement[{position}]"
        missing = [field for field in requirement_fields if not _text(_value(requirement, field))]
        if not _value(requirement, "category"):
            missing.append("category")
        if missing:
            issues.append(
                _issue(
                    ReviewSeverity.HIGH,
                    ReviewIssueCategory.FORMAT,
                    [item_id],
                    f"Requirement is missing required fields: {', '.join(missing)}.",
                    "Populate every required requirement field with a concrete value.",
                )
            )

    for position, entry in enumerate(blacklist):
        item_id = _text(_value(entry, "draft_id")) or f"blacklist[{position}]"
        missing = [field for field in blacklist_fields if not _text(_value(entry, field))]
        if missing:
            issues.append(
                _issue(
                    ReviewSeverity.HIGH,
                    ReviewIssueCategory.FORMAT,
                    [item_id],
                    f"Blacklist entry is missing required fields: {', '.join(missing)}.",
                    "Populate every required blacklist field, especially its reason.",
                )
            )
    return issues


def _check_priorities(requirements: Sequence[RequirementDraft]) -> list[ReviewIssue]:
    allowed = {priority.value for priority in Priority}
    issues: list[ReviewIssue] = []
    for requirement in requirements:
        priority = _enum_value(_value(requirement, "priority"))
        if priority not in allowed:
            item_id = _text(_value(requirement, "draft_id"))
            issues.append(
                _issue(
                    ReviewSeverity.HIGH,
                    ReviewIssueCategory.PRIORITY,
                    [item_id],
                    f"Priority {priority!r} is not one of {sorted(allowed)}.",
                    "Assign exactly High, Medium, or Low.",
                )
            )
    return issues


def _check_sources(
    requirements: Sequence[RequirementDraft],
    blacklist: Sequence[BlacklistEntry],
    allowed_source_ids: set[str],
) -> list[ReviewIssue]:
    issues: list[ReviewIssue] = []
    for kind, entries in (("Requirement", requirements), ("Blacklist entry", blacklist)):
        for entry in entries:
            item_id = _text(_value(entry, "draft_id"))
            refs = [_text(ref) for ref in (_value(entry, "source_refs", []) or []) if _text(ref)]
            if not refs:
                issues.append(
                    _issue(
                        ReviewSeverity.HIGH,
                        ReviewIssueCategory.TRACEABILITY,
                        [item_id],
                        f"{kind} has no source reference.",
                        "Attach at least one source ID from the input manifest.",
                    )
                )
            invalid = sorted(set(refs) - allowed_source_ids)
            if invalid:
                issues.append(
                    _issue(
                        ReviewSeverity.CRITICAL,
                        ReviewIssueCategory.TRACEABILITY,
                        [item_id, *invalid],
                        f"{kind} references sources absent from the manifest: {', '.join(invalid)}.",
                        "Remove invented references or replace them with exact manifest source IDs.",
                    )
                )
    return issues


def _check_candidate_coverage(
    requirements: Sequence[RequirementDraft],
    blacklist: Sequence[BlacklistEntry],
    candidates: Sequence[CandidateRequirement],
) -> list[ReviewIssue]:
    issues: list[ReviewIssue] = []
    known_ids = [_text(_value(candidate, "candidate_id")) for candidate in candidates]
    all_known = {candidate_id for candidate_id in known_ids if candidate_id}
    required = {
        _text(_value(candidate, "candidate_id"))
        for candidate in candidates
        if bool(_value(candidate, "is_requirement", True))
        and _text(_value(candidate, "candidate_id"))
    }
    noise = all_known - required

    final_assignments: list[str] = []
    blacklist_assignments: list[str] = []
    for requirement in requirements:
        final_assignments.extend(
            _text(candidate_id)
            for candidate_id in (_value(requirement, "merged_candidate_ids", []) or [])
            if _text(candidate_id)
        )
    for entry in blacklist:
        blacklist_assignments.extend(
            _text(candidate_id)
            for candidate_id in (_value(entry, "candidate_ids", []) or [])
            if _text(candidate_id)
        )

    final_counts = Counter(final_assignments)
    blacklist_counts = Counter(blacklist_assignments)

    missing = sorted(candidate_id for candidate_id in required if not final_counts[candidate_id] and not blacklist_counts[candidate_id])
    if missing:
        issues.append(
            _issue(
                ReviewSeverity.CRITICAL,
                ReviewIssueCategory.COVERAGE,
                missing,
                f"{len(missing)} candidate(s) are neither consolidated nor blacklisted.",
                "Place every candidate exactly once in a final requirement or a justified blacklist entry.",
            )
        )

    overlap = sorted(candidate_id for candidate_id in required if final_counts[candidate_id] and blacklist_counts[candidate_id])
    if overlap:
        issues.append(
            _issue(
                ReviewSeverity.CRITICAL,
                ReviewIssueCategory.COVERAGE,
                overlap,
                "Candidates occur in both final requirements and the blacklist.",
                "Keep each candidate on exactly one side of the final/blacklist boundary.",
            )
        )

    repeated = sorted(
        candidate_id
        for candidate_id in required
        if final_counts[candidate_id] + blacklist_counts[candidate_id] > 1
    )
    if repeated:
        issues.append(
            _issue(
                ReviewSeverity.HIGH,
                ReviewIssueCategory.COVERAGE,
                repeated,
                "Candidates are assigned more than once.",
                "Deduplicate candidate IDs so every candidate is represented exactly once.",
            )
        )

    assigned = set(final_assignments) | set(blacklist_assignments)
    noise_references = sorted(assigned & noise)
    if noise_references:
        issues.append(
            _issue(
                ReviewSeverity.CRITICAL,
                ReviewIssueCategory.COVERAGE,
                noise_references,
                "Final data references candidates classified as non-requirement noise.",
                "Remove noise candidates from both final requirements and the blacklist.",
            )
        )

    unknown = sorted(assigned - all_known)
    if unknown:
        issues.append(
            _issue(
                ReviewSeverity.CRITICAL,
                ReviewIssueCategory.COVERAGE,
                unknown,
                "Final data references candidate IDs absent from the extraction ledger.",
                "Remove invented IDs or restore the corresponding extracted candidates.",
            )
        )

    duplicate_input_ids = sorted(candidate_id for candidate_id, count in Counter(known_ids).items() if candidate_id and count > 1)
    if duplicate_input_ids:
        issues.append(
            _issue(
                ReviewSeverity.CRITICAL,
                ReviewIssueCategory.COVERAGE,
                duplicate_input_ids,
                "The extraction ledger contains duplicate candidate IDs.",
                "Assign every extracted candidate a unique candidate ID before consolidation.",
            )
        )
    return issues


def _check_exact_duplicates(requirements: Sequence[RequirementDraft]) -> list[ReviewIssue]:
    issues: list[ReviewIssue] = []
    for field in ("name", "description"):
        groups: dict[str, list[str]] = {}
        for requirement in requirements:
            normalized = normalize_exact_text(_value(requirement, field))
            if normalized:
                groups.setdefault(normalized, []).append(_text(_value(requirement, "draft_id")))
        for affected_ids in groups.values():
            if len(affected_ids) > 1:
                issues.append(
                    _issue(
                        ReviewSeverity.HIGH,
                        ReviewIssueCategory.DUPLICATE,
                        affected_ids,
                        f"Requirements have the same normalized {field}.",
                        "Merge the duplicate requirements and preserve all sources and candidate IDs.",
                    )
                )
    return issues


def _check_paragraph_quality(requirements: Sequence[RequirementDraft]) -> list[ReviewIssue]:
    issues: list[ReviewIssue] = []
    for requirement in requirements:
        description = _text(_value(requirement, "description"))
        words = re.findall(r"\b[^\W_]+(?:[-'][^\W_]+)*\b", description, flags=re.UNICODE)
        sentences = _SENTENCE_END_RE.findall(description)
        if len(words) < MIN_PARAGRAPH_WORDS and len(sentences) < 2:
            item_id = _text(_value(requirement, "draft_id"))
            issues.append(
                _issue(
                    ReviewSeverity.MEDIUM,
                    ReviewIssueCategory.QUALITY,
                    [item_id],
                    "Requirement explanation is not paragraph-length "
                    f"({len(words)} words, {len(sentences)} sentence endings).",
                    f"Expand it to at least two complete sentences or {MIN_PARAGRAPH_WORDS} words.",
                )
            )
    return issues


def validate_drafts(
    requirements: Sequence[RequirementDraft],
    blacklist: Sequence[BlacklistEntry],
    candidates: Sequence[CandidateRequirement],
    allowed_source_ids: Iterable[object],
    iteration: int,
    max_iterations: int,
) -> list[ReviewIssue]:
    """Return deterministic validation issues in a stable order."""

    requirements = list(requirements or [])
    blacklist = list(blacklist or [])
    candidates = list(candidates or [])
    allowed = _allowed_sources(allowed_source_ids)

    issues: list[ReviewIssue] = []
    issues.extend(_check_required_fields(requirements, blacklist))
    issues.extend(_check_priorities(requirements))
    issues.extend(_check_sources(requirements, blacklist, allowed))
    issues.extend(_check_candidate_coverage(requirements, blacklist, candidates))
    issues.extend(_check_exact_duplicates(requirements))
    issues.extend(_check_paragraph_quality(requirements))

    if max_iterations < 0 or iteration < 0 or iteration > max_iterations:
        issues.append(
            _issue(
                ReviewSeverity.CRITICAL,
                ReviewIssueCategory.FORMAT,
                [],
                f"Review iteration {iteration} is outside the configured range 0..{max_iterations}.",
                "Stop revising and finalize best-effort without exceeding the iteration limit.",
            )
        )
    return issues


def validate_state(state: Mapping[str, Any]) -> dict[str, Any]:
    """LangGraph node adapter around :func:`validate_drafts`.

    Both ``source_manifest`` and ``documents`` are accepted because the former is
    convenient for persisted runs while the latter is present immediately after
    loading.
    """

    sources = state.get("source_manifest") or state.get("documents") or []
    issues = validate_drafts(
        requirements=state.get("requirements", []),
        blacklist=state.get("blacklist", []),
        candidates=state.get("candidates", []),
        allowed_source_ids=sources,
        iteration=int(state.get("review_iteration", state.get("iteration", 0))),
        max_iterations=int(
            state.get(
                "max_review_iterations",
                state.get("max_iterations", MAX_REVIEW_ITERATIONS),
            )
        ),
    )
    return {
        "validation_issues": issues,
        "validation_passed": not issues,
    }


__all__ = [
    "MIN_PARAGRAPH_WORDS",
    "normalize_exact_text",
    "validate_drafts",
    "validate_state",
]
