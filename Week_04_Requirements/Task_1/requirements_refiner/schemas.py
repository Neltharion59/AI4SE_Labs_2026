"""Validated data contracts exchanged by deterministic and LLM nodes."""

from __future__ import annotations

from enum import Enum
from typing import Annotated

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    StringConstraints,
    field_validator,
    model_validator,
)

NonEmptyStr = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]
DuplicatePair = Annotated[list[NonEmptyStr], Field(min_length=2, max_length=2)]


class FileType(str, Enum):
    TXT = "txt"
    EML = "eml"


class RequirementCategory(str, Enum):
    FUNCTIONAL = "functional"
    NON_FUNCTIONAL = "non_functional"
    CONSTRAINT = "constraint"
    DOCUMENTATION = "documentation"
    DEPENDENCY = "dependency"


class Priority(str, Enum):
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"


class PriorityBasis(str, Enum):
    EXPLICIT = "explicit"
    INFERRED = "inferred"
    UNKNOWN = "unknown"


class BlacklistClassification(str, Enum):
    CONFLICTING = "conflicting"
    NONSENSICAL = "nonsensical"
    OUT_OF_SCOPE = "out_of_scope"
    OBSOLETE = "obsolete"
    UNSUPPORTED = "unsupported"


class ReviewSeverity(str, Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class ReviewIssueCategory(str, Enum):
    DUPLICATE = "duplicate"
    CONFLICT = "conflict"
    TERMINOLOGY = "terminology"
    TRACEABILITY = "traceability"
    COVERAGE = "coverage"
    FORMAT = "format"
    PRIORITY = "priority"
    QUALITY = "quality"


class SchemaModel(BaseModel):
    """Strict base class used for all structured pipeline payloads."""

    model_config = ConfigDict(extra="forbid", use_enum_values=False)


class DocumentChunk(SchemaModel):
    chunk_id: NonEmptyStr
    source_id: NonEmptyStr
    chunk_index: int = Field(ge=0)
    text: NonEmptyStr


class SourceDocument(SchemaModel):
    source_id: NonEmptyStr
    file_type: FileType
    title: NonEmptyStr
    date: NonEmptyStr | None = None
    content: NonEmptyStr
    chunks: list[DocumentChunk] = Field(min_length=1)
    sha256: str = Field(pattern=r"^[0-9a-f]{64}$")

    @model_validator(mode="after")
    def validate_chunk_ownership(self) -> "SourceDocument":
        expected_indexes = list(range(len(self.chunks)))
        indexes = [chunk.chunk_index for chunk in self.chunks]
        if indexes != expected_indexes:
            raise ValueError("Document chunk indexes must be contiguous and start at zero")
        if any(chunk.source_id != self.source_id for chunk in self.chunks):
            raise ValueError("Every chunk must refer to its owning source document")
        if len({chunk.chunk_id for chunk in self.chunks}) != len(self.chunks):
            raise ValueError("Chunk IDs must be unique within a source document")
        return self


class CandidateRequirement(SchemaModel):
    candidate_id: NonEmptyStr
    title: NonEmptyStr
    statement: NonEmptyStr
    explanation: NonEmptyStr
    category: RequirementCategory
    priority_hint: Priority | None = None
    priority_basis: PriorityBasis = PriorityBasis.UNKNOWN
    source_refs: list[NonEmptyStr] = Field(min_length=1)
    chunk_refs: list[NonEmptyStr] = Field(min_length=1)
    evidence_summary: NonEmptyStr
    confidence: float = Field(ge=0.0, le=1.0)
    is_requirement: bool = True
    rejection_reason: NonEmptyStr | None = None

    @field_validator("source_refs", "chunk_refs")
    @classmethod
    def unique_references(cls, values: list[str]) -> list[str]:
        if len(values) != len(set(values)):
            raise ValueError("References must not contain duplicates")
        return values

    @model_validator(mode="after")
    def validate_rejection_reason(self) -> "CandidateRequirement":
        if not self.is_requirement and self.rejection_reason is None:
            raise ValueError("A rejected candidate must include rejection_reason")
        return self


class RequirementDraft(SchemaModel):
    draft_id: NonEmptyStr
    category: RequirementCategory
    name: NonEmptyStr
    description: NonEmptyStr
    priority: Priority
    priority_rationale: NonEmptyStr
    source_refs: list[NonEmptyStr] = Field(min_length=1)
    merged_candidate_ids: list[NonEmptyStr] = Field(min_length=1)
    conflict_resolution: NonEmptyStr | None = None
    verification_hint: NonEmptyStr | None = None

    @field_validator("source_refs", "merged_candidate_ids")
    @classmethod
    def unique_references(cls, values: list[str]) -> list[str]:
        if len(values) != len(set(values)):
            raise ValueError("References must not contain duplicates")
        return values


class BlacklistEntry(SchemaModel):
    draft_id: NonEmptyStr
    name: NonEmptyStr
    description: NonEmptyStr
    reason: NonEmptyStr
    source_refs: list[NonEmptyStr] = Field(min_length=1)
    candidate_ids: list[NonEmptyStr] = Field(min_length=1)
    classification: BlacklistClassification

    @field_validator("source_refs", "candidate_ids")
    @classmethod
    def unique_references(cls, values: list[str]) -> list[str]:
        if len(values) != len(set(values)):
            raise ValueError("References must not contain duplicates")
        return values


class ReviewIssue(SchemaModel):
    severity: ReviewSeverity
    category: ReviewIssueCategory
    affected_ids: list[NonEmptyStr] = Field(default_factory=list)
    message: NonEmptyStr
    suggested_fix: NonEmptyStr


class ReviewReport(SchemaModel):
    approved: bool
    issues: list[ReviewIssue] = Field(default_factory=list)
    duplicate_pairs: list[DuplicatePair] = Field(default_factory=list)
    conflicts: list[NonEmptyStr] = Field(default_factory=list)
    missing_candidate_ids: list[NonEmptyStr] = Field(default_factory=list)
    invalid_source_refs: list[NonEmptyStr] = Field(default_factory=list)
    terminology_findings: list[NonEmptyStr] = Field(default_factory=list)
    coverage_findings: list[NonEmptyStr] = Field(default_factory=list)

    @model_validator(mode="after")
    def approved_report_has_no_reported_problems(self) -> "ReviewReport":
        problem_lists = (
            self.issues,
            self.duplicate_pairs,
            self.conflicts,
            self.missing_candidate_ids,
            self.invalid_source_refs,
            self.terminology_findings,
            self.coverage_findings,
        )
        if self.approved and any(problem_lists):
            raise ValueError("An approved review report cannot contain unresolved problems")
        if not self.approved and not any(problem_lists):
            raise ValueError(
                "A rejected review report must contain at least one actionable finding"
            )
        return self


class ExtractionResult(SchemaModel):
    candidates: list[CandidateRequirement] = Field(default_factory=list)


class ConsolidationResult(SchemaModel):
    requirements: list[RequirementDraft] = Field(default_factory=list)
    blacklist: list[BlacklistEntry] = Field(default_factory=list)

