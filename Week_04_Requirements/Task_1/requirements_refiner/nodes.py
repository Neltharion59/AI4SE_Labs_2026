"""LLM-backed LangGraph nodes with strict structured-output boundaries."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable, Mapping, Sequence, TypeVar

from .prompts import (
    CONSOLIDATION_SYSTEM_PROMPT,
    EXTRACTION_SYSTEM_PROMPT,
    REVIEW_SYSTEM_PROMPT,
    REVISION_SYSTEM_PROMPT,
    consolidation_input,
    extraction_input,
    review_input,
    revision_input,
)
from .schemas import (
    BlacklistEntry,
    CandidateRequirement,
    ConsolidationResult,
    ExtractionResult,
    ReviewReport,
)


T = TypeVar("T")


class LLMNodeError(RuntimeError):
    """A safe, user-facing failure raised at an LLM node boundary."""


def _invoke_structured(
    runner: Any,
    schema: type[T],
    *,
    system_prompt: str,
    human_prompt: str,
    node_name: str,
    model_name: str,
) -> T:
    try:
        raw = runner.invoke([("system", system_prompt), ("human", human_prompt)])
        if isinstance(raw, schema):
            return raw
        return schema.model_validate(raw)
    except Exception as exc:
        # Do not interpolate exception text: SDK errors can contain request data,
        # headers, endpoint credentials, or corpus excerpts.
        kind = type(exc).__name__
        raise LLMNodeError(
            f"Node '{node_name}' failed with model '{model_name}' "
            f"({kind}). Check model access, connectivity, and structured output."
        ) from None


def _source_manifest(state: Mapping[str, Any]) -> list[str]:
    manifest = state.get("source_manifest")
    if manifest:
        return sorted(set(str(item) for item in manifest))
    return sorted({str(document.source_id) for document in state.get("documents", [])})


def _true_candidates(
    candidates: Sequence[CandidateRequirement],
) -> list[CandidateRequirement]:
    """Return only candidates eligible for consolidation and review coverage."""

    return [candidate for candidate in candidates if candidate.is_requirement]


def _validate_refs(
    *,
    source_refs: Iterable[str],
    candidate_ids: Iterable[str] = (),
    allowed_sources: set[str],
    allowed_candidates: set[str] | None = None,
    node_name: str,
) -> None:
    unknown_sources = set(source_refs) - allowed_sources
    unknown_candidates = (
        set(candidate_ids) - allowed_candidates if allowed_candidates is not None else set()
    )
    if unknown_sources or unknown_candidates:
        # Values themselves are deliberately omitted: they originated in untrusted
        # model output and should not be reflected into logs or terminal messages.
        raise LLMNodeError(
            f"Node '{node_name}' returned identifiers outside its allow-list "
            f"({len(unknown_sources)} source, {len(unknown_candidates)} candidate)."
        )


def _validate_consolidation(
    result: ConsolidationResult,
    *,
    sources: Sequence[str],
    candidates: Sequence[CandidateRequirement],
    node_name: str,
) -> None:
    allowed_sources = set(sources)
    allowed_candidates = {
        candidate.candidate_id for candidate in candidates if candidate.is_requirement
    }
    candidate_sources = {
        candidate.candidate_id: set(candidate.source_refs)
        for candidate in candidates
        if candidate.is_requirement
    }
    seen_draft_ids: set[str] = set()
    for position, requirement in enumerate(result.requirements, start=1):
        if requirement.draft_id in seen_draft_ids:
            raise LLMNodeError(f"Node '{node_name}' returned duplicate draft identifiers.")
        seen_draft_ids.add(requirement.draft_id)
        _validate_refs(
            source_refs=requirement.source_refs,
            candidate_ids=requirement.merged_candidate_ids,
            allowed_sources=allowed_sources,
            allowed_candidates=allowed_candidates,
            node_name=node_name,
        )
        expected_sources = set().union(
            *(candidate_sources[item] for item in requirement.merged_candidate_ids)
        )
        actual_sources = set(requirement.source_refs)
        if actual_sources != expected_sources:
            missing_sources = expected_sources - actual_sources
            unexpected_sources = actual_sources - expected_sources
            raise LLMNodeError(
                f"Node '{node_name}' did not preserve the source lineage of merged "
                f"candidates for requirement position {position} "
                f"({len(missing_sources)} missing, {len(unexpected_sources)} unexpected "
                "source reference(s))."
            )
    for position, entry in enumerate(result.blacklist, start=1):
        if entry.draft_id in seen_draft_ids:
            raise LLMNodeError(f"Node '{node_name}' returned duplicate draft identifiers.")
        seen_draft_ids.add(entry.draft_id)
        _validate_refs(
            source_refs=entry.source_refs,
            candidate_ids=entry.candidate_ids,
            allowed_sources=allowed_sources,
            allowed_candidates=allowed_candidates,
            node_name=node_name,
        )
        expected_sources = set().union(
            *(candidate_sources[item] for item in entry.candidate_ids)
        )
        actual_sources = set(entry.source_refs)
        if actual_sources != expected_sources:
            missing_sources = expected_sources - actual_sources
            unexpected_sources = actual_sources - expected_sources
            raise LLMNodeError(
                f"Node '{node_name}' did not preserve the source lineage of blacklisted "
                f"candidates for blacklist position {position} "
                f"({len(missing_sources)} missing, {len(unexpected_sources)} unexpected "
                "source reference(s))."
            )


def _normalise_review_report(
    report: ReviewReport,
    *,
    candidates: Sequence[CandidateRequirement],
    requirements: Sequence[Any],
    blacklist: Sequence[Any],
    sources: Sequence[str],
) -> ReviewReport:
    """Validate reviewer identifiers and return a deterministic report.

    Reviewer output is untrusted even after structural schema validation.  Every
    identifier must therefore be grounded in the exact state that was supplied to
    the reviewer.  Free-form finding text is retained unchanged.
    """

    allowed_candidates = {
        candidate.candidate_id for candidate in candidates if candidate.is_requirement
    }
    allowed_requirements = {str(item.draft_id) for item in requirements}
    allowed_blacklist = {str(item.draft_id) for item in blacklist}
    allowed_sources = set(sources)
    allowed_affected = (
        allowed_candidates | allowed_requirements | allowed_blacklist | allowed_sources
    )

    def unique(values: Iterable[str]) -> list[str]:
        return sorted(set(values))

    invalid_missing = set(report.missing_candidate_ids) - allowed_candidates
    invalid_sources = set(report.invalid_source_refs) - allowed_sources
    invalid_conflicts = set(report.conflicts) - allowed_requirements
    invalid_affected = {
        identifier
        for issue in report.issues
        for identifier in issue.affected_ids
        if identifier not in allowed_affected
    }

    normalised_pairs: set[tuple[str, str]] = set()
    invalid_pair_ids: set[str] = set()
    self_pairs = 0
    for left, right in report.duplicate_pairs:
        invalid_pair_ids.update({left, right} - allowed_requirements)
        if left == right:
            self_pairs += 1
            continue
        normalised_pairs.add(tuple(sorted((left, right))))

    invalid_count = (
        len(invalid_missing)
        + len(invalid_sources)
        + len(invalid_conflicts)
        + len(invalid_affected)
        + len(invalid_pair_ids)
        + self_pairs
    )
    if invalid_count:
        raise LLMNodeError(
            "Node 'review_quality' returned fabricated or invalid identifiers "
            f"outside the supplied state allow-lists ({invalid_count} reference(s))."
        )

    issues = [
        issue.model_copy(update={"affected_ids": unique(issue.affected_ids)})
        for issue in report.issues
    ]
    payload = report.model_dump(mode="python")
    payload.update(
        {
            "issues": issues,
            "duplicate_pairs": sorted(normalised_pairs),
            "conflicts": unique(report.conflicts),
            "missing_candidate_ids": unique(report.missing_candidate_ids),
            "invalid_source_refs": unique(report.invalid_source_refs),
            "terminology_findings": unique(report.terminology_findings),
            "coverage_findings": unique(report.coverage_findings),
        }
    )
    return ReviewReport.model_validate(payload)


def _chunk_payload(document: Any, chunk: Any) -> dict[str, Any]:
    return {
        "source_id": document.source_id,
        "source_title": document.title,
        "source_date": document.date,
        "chunk_id": chunk.chunk_id,
        "text": chunk.text,
    }


def _batches(items: Sequence[T], size: int) -> Iterable[Sequence[T]]:
    if size < 1:
        raise ValueError("batch_size must be at least 1")
    for start in range(0, len(items), size):
        yield items[start : start + size]


def _repair_chunk_refs(
    candidate: CandidateRequirement,
    allowed_chunks: set[str],
    chunk_sources: Mapping[str, str],
) -> CandidateRequirement | None:
    """Ground common LLM identifier formatting mistakes in the current batch."""

    repaired: list[str] = []
    for reference in candidate.chunk_refs:
        if reference in allowed_chunks:
            repaired.append(reference)
            continue

        source_part, separator, suffix = reference.partition("#")
        number = suffix.casefold().removeprefix("chunk-") if separator else ""
        if number.isdigit():
            matches = []
            for allowed in allowed_chunks:
                allowed_source, _, allowed_suffix = allowed.partition("#")
                allowed_number = allowed_suffix.casefold().removeprefix("chunk-")
                source_matches = not source_part or allowed_source == source_part
                if source_matches and allowed_number.isdigit() and int(allowed_number) == int(number):
                    matches.append(allowed)
            if len(matches) == 1:
                repaired.append(matches[0])

    if not repaired:
        source_matches = [
            chunk_id
            for chunk_id, source_id in chunk_sources.items()
            if source_id in candidate.source_refs
        ]
        if source_matches:
            repaired = source_matches

    if not repaired:
        return None
    return candidate.model_copy(update={"chunk_refs": sorted(set(repaired))})


def _normalise_candidates(candidates: Sequence[CandidateRequirement]) -> list[CandidateRequirement]:
    """Deduplicate only identical overlap artefacts and assign stable IDs.

    Matching normalized titles and statements are not enough to prove that two
    extractions describe the same evidence.  In particular, differing priority,
    category, explanation, evidence summary, confidence, or rejection metadata
    must remain visible to consolidation instead of being silently discarded.
    Only references may differ between candidates that are merged here.
    """

    unique: dict[tuple[Any, ...], CandidateRequirement] = {}
    for candidate in candidates:
        payload = candidate.model_dump(mode="python", exclude={
            "candidate_id",
            "source_refs",
            "chunk_refs",
        })
        key = (
            " ".join(candidate.title.casefold().split()),
            " ".join(candidate.statement.casefold().split()),
            tuple(
                (field, value.value if hasattr(value, "value") else value)
                for field, value in sorted(payload.items())
                if field not in {"title", "statement"}
            ),
        )
        previous = unique.get(key)
        if previous is None:
            unique[key] = candidate
            continue
        update = {
            "source_refs": sorted(set(previous.source_refs) | set(candidate.source_refs)),
            "chunk_refs": sorted(set(previous.chunk_refs) | set(candidate.chunk_refs)),
        }
        unique[key] = previous.model_copy(update=update)

    output: list[CandidateRequirement] = []
    for index, candidate in enumerate(unique.values(), start=1):
        output.append(candidate.model_copy(update={"candidate_id": f"ITEM-{index:05d}"}))
    return output


@dataclass
class ExtractCandidatesNode:
    runner: Any
    model_name: str
    batch_size: int = 6
    max_identifier_retries: int = 1

    def __call__(self, state: Mapping[str, Any]) -> dict[str, Any]:
        chunks = [
            _chunk_payload(document, chunk)
            for document in state.get("documents", [])
            for chunk in document.chunks
        ]
        if not chunks:
            raise LLMNodeError("Node 'extract_candidates' received no document chunks.")

        extracted: list[CandidateRequirement] = []
        lineage_corrections = 0
        identifier_retries = 0
        identifier_repairs = 0
        dropped_ungrounded_items = 0
        for batch in _batches(chunks, self.batch_size):
            allowed_chunks = {str(item["chunk_id"]) for item in batch}
            chunk_sources = {
                str(item["chunk_id"]): str(item["source_id"]) for item in batch
            }
            result: ExtractionResult | None = None
            for attempt in range(self.max_identifier_retries + 1):
                result = _invoke_structured(
                    self.runner,
                    ExtractionResult,
                    system_prompt=EXTRACTION_SYSTEM_PROMPT,
                    human_prompt=extraction_input(
                        batch,
                        identifier_retry=attempt > 0,
                    ),
                    node_name="extract_candidates",
                    model_name=self.model_name,
                )
                invalid_refs = sum(
                    len(set(candidate.chunk_refs) - allowed_chunks)
                    for candidate in result.candidates
                )
                if invalid_refs == 0:
                    break
                if attempt == self.max_identifier_retries:
                    break
                identifier_retries += 1

            assert result is not None  # The bounded loop always invokes the runner.
            normalised_batch: list[CandidateRequirement] = []
            for candidate in result.candidates:
                repaired = _repair_chunk_refs(candidate, allowed_chunks, chunk_sources)
                if repaired is None:
                    dropped_ungrounded_items += 1
                    continue
                if repaired.chunk_refs != candidate.chunk_refs:
                    identifier_repairs += 1
                candidate = repaired
                evidence_sources = {chunk_sources[item] for item in candidate.chunk_refs}
                if set(candidate.source_refs) != evidence_sources:
                    # Chunk IDs are the most specific evidence references and have
                    # already been checked against the exact batch allow-list.
                    # Derive the redundant document references from them instead
                    # of failing the complete corpus run on a correctable LLM
                    # bookkeeping mistake.
                    candidate = candidate.model_copy(
                        update={"source_refs": sorted(evidence_sources)}
                    )
                    lineage_corrections += 1
                normalised_batch.append(candidate)
            extracted.extend(normalised_batch)

        candidates = _normalise_candidates(extracted)
        stats = dict(state.get("run_stats", {}))
        stats.update(
            {
                "extraction_calls": (len(chunks) + self.batch_size - 1) // self.batch_size,
                "identifier_retries": identifier_retries,
                "identifier_repairs": identifier_repairs,
                "dropped_ungrounded_items": dropped_ungrounded_items,
                "candidate_count": len(candidates),
                "lineage_corrections": lineage_corrections,
            }
        )
        return {"candidates": candidates, "run_stats": stats}


@dataclass
class ConsolidateRequirementsNode:
    runner: Any
    model_name: str

    def __call__(self, state: Mapping[str, Any]) -> dict[str, Any]:
        candidates = list(state.get("candidates", []))
        eligible_candidates = _true_candidates(candidates)
        sources = _source_manifest(state)
        if not candidates:
            raise LLMNodeError("Node 'consolidate_requirements' received no candidates.")
        result = _invoke_structured(
            self.runner,
            ConsolidationResult,
            system_prompt=CONSOLIDATION_SYSTEM_PROMPT,
            human_prompt=consolidation_input(eligible_candidates, sources),
            node_name="consolidate_requirements",
            model_name=self.model_name,
        )
        _validate_consolidation(
            result, sources=sources, candidates=candidates, node_name="consolidate_requirements"
        )
        return {"requirements": result.requirements, "blacklist": result.blacklist}


@dataclass
class ReviewQualityNode:
    runner: Any
    model_name: str
    max_identifier_retries: int = 1

    def __call__(self, state: Mapping[str, Any]) -> dict[str, Any]:
        candidates = list(state.get("candidates", []))
        eligible_candidates = _true_candidates(candidates)
        requirements = list(state.get("requirements", []))
        blacklist = list(state.get("blacklist", []))
        for attempt in range(self.max_identifier_retries + 1):
            report = _invoke_structured(
                self.runner,
                ReviewReport,
                system_prompt=REVIEW_SYSTEM_PROMPT,
                human_prompt=review_input(
                    eligible_candidates,
                    requirements,
                    blacklist,
                    _source_manifest(state),
                    identifier_retry=attempt > 0,
                ),
                node_name="review_quality",
                model_name=self.model_name,
            )
            try:
                normalised = _normalise_review_report(
                    report,
                    candidates=candidates,
                    requirements=requirements,
                    blacklist=blacklist,
                    sources=_source_manifest(state),
                )
            except LLMNodeError:
                if attempt == self.max_identifier_retries:
                    raise
                continue
            update: dict[str, Any] = {"review_report": normalised}
            if attempt:
                stats = dict(state.get("run_stats", {}))
                stats["review_identifier_retries"] = int(
                    stats.get("review_identifier_retries", 0)
                ) + attempt
                update["run_stats"] = stats
            return update
        raise AssertionError("The bounded review retry loop did not return or raise.")


@dataclass
class ReviseRequirementsNode:
    runner: Any
    model_name: str

    def __call__(self, state: Mapping[str, Any]) -> dict[str, Any]:
        candidates = list(state.get("candidates", []))
        eligible_candidates = _true_candidates(candidates)
        sources = _source_manifest(state)
        result = _invoke_structured(
            self.runner,
            ConsolidationResult,
            system_prompt=REVISION_SYSTEM_PROMPT,
            human_prompt=revision_input(
                eligible_candidates,
                list(state.get("requirements", [])),
                list(state.get("blacklist", [])),
                state.get("review_report"),
                list(state.get("validation_errors", [])),
                list(state.get("validation_issues", [])),
                sources,
            ),
            node_name="revise_requirements",
            model_name=self.model_name,
        )
        _validate_consolidation(
            result, sources=sources, candidates=candidates, node_name="revise_requirements"
        )
        return {
            "requirements": result.requirements,
            "blacklist": result.blacklist,
            "review_iteration": int(state.get("review_iteration", 0)) + 1,
            "review_report": None,
            "validation_errors": [],
            "validation_issues": [],
            "validation_passed": False,
        }


# Concise aliases make graph assembly readable while preserving descriptive class
# names in tests and documentation.
ExtractionNode = ExtractCandidatesNode
ConsolidationNode = ConsolidateRequirementsNode
ReviewNode = ReviewQualityNode
RevisionNode = ReviseRequirementsNode
