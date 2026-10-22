# Report

## 1. Purpose

This project implements an agentic network that reads a directory of heterogeneous
software-related documents and produces one structured requirements document. 
The implementation is contained in [requirements_network.py] and uses LangGraph to coordinate deterministic processing and OpenAI-powered requirements-engineering agents.

The network was run on the supplied corpus in `data\corpus`. The generated result
is available in [requirements.md].

## 2. Design overview

The network is a directed LangGraph workflow:

```text
load_documents
    -> extract_requirements
    -> pre_dedup
    -> semantic_merge
    -> consistency_check
    -> completeness_review
        -> gap_extract -> pre_dedup       (feedback loop)
        -> adopt_gaps -> prioritize        (iteration limit)
        -> prioritize                      (no gaps)
    -> assemble_document
```

The design separates tasks according to their reliability:

- LLM nodes perform interpretation, semantic comparison, review, completeness
  analysis and prioritisation.
- Deterministic nodes handle file discovery, source validation, ID assignment,
  merge application, routing and final document generation.
- The LLM is required to return JSON, while Python validates and applies the
  resulting operations instead of trusting model-provided state changes blindly.

## 3. Node design choices

### 3.1 Document loading

`load_documents` recursively scans the directory supplied through `--input-dir`.
It accepts `.txt`, `.md` and `.eml` files, assigns stable document identifiers
(`D01`, `D02`, ...), and stores each document's relative filename and text.

Input paths are not hard-coded. The output is also supplied by the user through
`--output` and points directly to the single Markdown output file.

### 3.2 Requirement extraction

`extract_requirements` invokes the extraction model independently for each input
document. Long documents are split into bounded chunks before they are sent to the
model. The extraction prompt requires:

- every supported functional or non-functional need,
- atomic requirements rather than unrelated compound features,
- a short descriptive name,
- a self-contained paragraph explanation,
- preservation of concrete details such as roles, parameters and numbers,
- rejection of nonsensical, contradictory or clearly out-of-scope requirement-like
  statements with a reason.

The extractor records the source document ID on every accepted or rejected item,
which provides the basis for traceability and the blacklist.

### 3.3 Deterministic pre-deduplication

`pre_dedup` performs an initial deterministic pass using token-based Jaccard
similarity. It merges near-identical candidates by combining their source lists,
rejects candidates without valid source documents and prevents discarded items
from being reintroduced.

Requirements receive unique identifiers in the `REQ-001` format. Source IDs are
sanitised against the set of documents actually loaded.

### 3.4 Semantic merge

`semantic_merge` asks a dedicated merge model to identify genuinely equivalent
requirements. The prompt explicitly prohibits merging items that only share a
topic. Merge groups are bounded by `MAX_GROUP`, and the deterministic
`_apply_groups` helper:

- only accepts IDs shown to the model in the current batch,
- ignores malformed or repeated IDs,
- handles overlapping groups safely,
- combines all source documents,
- rejects over-large or invalid groups.

This two-stage design combines cheap deterministic near-duplicate detection with
LLM semantic comparison while keeping the actual mutation of the requirement
pool deterministic.

### 3.5 Consistency and vocabulary review

`consistency_check` reviews the current requirements for:

- contradictions,
- nonsensical or out-of-scope requirements,
- inconsistent terminology,
- canonical vocabulary.

The model may return conflicts, discarded IDs, edited names/descriptions and a
glossary. Python applies only edits referring to existing IDs. Discarded
requirements are added to the blacklist with their source documents and an
explanation.

### 3.6 Completeness feedback loop

`completeness_review` independently compares the current requirements against
the source corpus. It reports missing requirements and their source documents.
When gaps are found and the iteration limit has not been reached,
`gap_extract` performs targeted extraction and sends the new candidates through
the same deduplication and semantic-merge stages.

If the iteration limit is reached while gaps remain, `adopt_gaps` adds the
auditor-reported gaps deterministically rather than silently dropping them. This
ensures that the network addresses completeness even when the bounded feedback
loop cannot perform another full review cycle.

### 3.7 Prioritisation

`prioritize` assigns MoSCoW priorities for the first release. Requirements are
processed in batches, and missing model responses are retried. A deterministic
fallback ensures that every final requirement has a valid priority even if a
model response is incomplete.

The output document explains all four priority levels:

- **Must** — release-blocking or essential for the system's core purpose.
- **Should** — important, but a workaround exists.
- **Could** — desirable improvement or convenience.
- **Won't** — explicitly deferred, excluded or dependent on an undecided issue.

### 3.8 Final assembly and validation

`assemble_document` produces the single Markdown document. It includes:

1. priority scale,
2. source-document list,
3. canonical glossary,
4. requirements summary,
5. full requirement descriptions,
6. discarded-items blacklist,
7. generation notes and validation result.

Each requirement contains its ID, name, priority, source documents and
paragraph-long description. The `Derived from` field provides per-requirement
traceability, so a separate traceability matrix is not required.

The deterministic validator checks unique IDs, valid source IDs, valid priorities
and non-empty names/descriptions. Validation problems are written into the
generation notes instead of being hidden.

## 4. Model allocation

The implementation uses five distinct model roles. Each role can be overridden
through an environment variable:

| Role | Default model | Responsibility |
|---|---|---|
| Extraction | `gpt-5-mini` | High-recall extraction from source documents |
| Merge | `gpt-5.4-nano` | Semantic duplicate detection |
| Consistency | `gpt-6-luna` | Conflict resolution and vocabulary review |
| Completeness | `gpt-5.6-luna` | Independent gap audit |
| Prioritisation | `gpt-4o-mini` | MoSCoW priority assignment |

All model calls use the OpenAI client and request JSON output. API failures and
malformed JSON are retried with bounded exponential backoff.

## 5. Compliance with Task 1

### Agentic network specifications

| Specification | Implementation |
|---|---|
| ANS1: at least three LLM nodes | Six LLM-driven nodes: extraction, semantic merge, consistency, completeness, gap extraction and prioritisation |
| ANS2: at least one deterministic node | Document loading, pre-deduplication, gap adoption and document assembly |
| ANS3: feedback loop | Completeness review routes through gap extraction back to pre-deduplication |
| ANS4: at least three different models | Five configured model roles |
| ANS5: Python LangGraph | `StateGraph`, `START`, conditional routing and `END` in `requirements_network.py` |

### Output specifications

| Specification | Implementation |
|---|---|
| OS1: single structured document | One Markdown file written to the path passed through `--output` |
| OS2: unique identification | Deterministic `REQ-xxx` identifiers |
| OS3: no semantic duplicates | Deterministic pre-deduplication plus bounded LLM semantic merge |
| OS4: tracing | Every requirement contains `Derived from` with document IDs and filenames |
| OS5: name and explanation | Extraction prompt and final assembly require a short name and paragraph description |
| OS6: priority and scale | MoSCoW priority on every requirement and a documented priority-scale table |
| OS7: consistency | Consistency-review node, conflict handling and canonical glossary |
| OS8: completeness | Independent completeness audit and bounded feedback loop |
| OS9: blacklist | Separate discarded-items section with sources and reasons |

The separate design report required by the assignment is this file. The generated
requirements document remains a separate deliverable.

## 6. Execution

Install the dependencies from [requirements.txt], set the OpenAI API key, and run:

```powershell
$env:OPENAI_API_KEY="your-key"
python .\requirements_network.py --input-dir .\data\corpus --output .\requirements.md
```

Optional `--max-iterations` controls the maximum number of completeness feedback
rounds and defaults to `2`.

## 7. Results for the supplied corpus

The checked generated document reports:

- 20 loaded source documents,
- 413 initially extracted candidates,
- 116 semantic duplicates removed in the first merge stage,
- additional duplicates removed during feedback rounds,
- 269 final requirements,
- 7 discarded/blacklisted items,
- 269 priority assignments,
- source tracing on every final requirement,
- validation passed for unique IDs, valid traces and valid priorities.

The generation log also records two completeness-review rounds with targeted
gap extraction before the final review reported no remaining gaps.


