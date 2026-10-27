#!/usr/bin/env python3
r"""
Input : a directory with free-text documents 
Output: one structured Markdown document with refined requirements

Pipeline (LangGraph):

  load_documents (det) -> extract_requirements (LLM) -> pre_dedup (det)
      -> semantic_merge (LLM) -> consistency_check (LLM)
      -> completeness_review (LLM) --gaps found--> gap_extract (LLM) -> pre_dedup ...   <- FEEDBACK LOOP
                                   \--limit reached--> adopt_gaps (det) -> prioritize (LLM)
                                   \--no gaps--> prioritize (LLM)
      -> assemble_document (det, validates + writes output)
"""
from __future__ import annotations

import argparse
import json
import operator
import os
import re
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Annotated, Any, TypedDict

from langgraph.graph import END, START, StateGraph

# ANS4: five different models, one per role
MODELS = {
    "extract": os.getenv("MODEL_EXTRACT", "gpt-5-mini"),          # reads raw text, needs recall
    "merge": os.getenv("MODEL_MERGE", "gpt-5.4-nano"),            # cheap clustering of short items
    "consistency": os.getenv("MODEL_CONSISTENCY", "gpt-6-luna"),  # strongest reasoning: conflicts
    "completeness": os.getenv("MODEL_COMPLETENESS", "gpt-5.6-luna"),  # independent auditor of recall
    "prioritize": os.getenv("MODEL_PRIORITIZE", "gpt-4o-mini"),   # simple classification
}

TEXT_SUFFIXES = {".txt", ".md", ".eml"}
CHUNK_CHARS = 30_000          # documents longer than this are split for extraction
CORPUS_CHARS = 350_000        # cap on corpus text shown to the completeness reviewer
MERGE_BATCH = 120             # max items per semantic-merge call
MAX_GROUP = 5                 # a merge group larger than this is rejected as over-merging
NEIGHBOURS = 8                # settled items shown next to each new item in later merge rounds
PRIORITY_BATCH = 25           # requirements per prioritisation call
API_RETRIES = 5
MAX_WORKERS = 4
PRIORITIES = ["Must", "Should", "Could", "Won't"]

PRIORITY_SCALE = {
    "Must": "Release-blocking. The system cannot go live or fails its core purpose without it: a legal, regulatory "
            "or accessibility obligation, security or data integrity, a function the stakeholders call critical or "
            "essential, or a prerequisite of another Must.",
    "Should": "High value, but the release is still usable without it: a manual or ad-hoc workaround exists, even if "
              "painful. Planned for the first release unless time is critically short.",
    "Could": "Nice to have. Small benefit or convenience; most users would not notice its absence. "
             "Include only if capacity allows.",
    "Won't": "Explicitly deferred or excluded by the stakeholders for this release, or dependent on a question "
             "they left undecided. Kept for future planning.",
}

class State(TypedDict, total=False):
    input_dir: str
    output: str
    max_iterations: int
    docs: list[dict]                       # {id, filename, text}
    candidates: list[dict]                 # freshly extracted, not yet merged
    requirements: list[dict]               # current merged list
    blacklist: Annotated[list[dict], operator.add]  # discarded items (OS9)
    glossary: list[dict]
    gaps: list[dict]                       # missing requirements reported by the auditor
    iteration: int
    log: Annotated[list[str], operator.add]
    output_path: str


# LLM access

_client = None

def call_llm(role: str, system: str, user: str) -> dict:
    """Call a model and return parsed JSON. Retries API errors (rate limit, timeout) with backoff
    and malformed JSON once, so one hiccup does not destroy a long run."""
    import time
    global _client
    if _client is None:
        from openai import OpenAI
        _client = OpenAI()  # reads OPENAI_API_KEY
    bad_json = 0
    last_err: Exception | None = None
    for attempt in range(API_RETRIES):
        msgs = [{"role": "system", "content": system},
                {"role": "user", "content": user}]
        if bad_json:
            msgs.append({"role": "user", "content": "Your previous reply was not valid JSON. "
                                                    "Reply again with ONLY the JSON object."})
        try:
            resp = _client.chat.completions.create(
                model=MODELS[role], messages=msgs, response_format={"type": "json_object"})
            return json.loads(resp.choices[0].message.content or "")
        except json.JSONDecodeError as e:
            last_err, bad_json = e, 1
        except Exception as e:  # rate limit, timeout, 5xx ...
            last_err = e
            time.sleep(min(2 ** attempt, 30))
    raise RuntimeError(f"[{role}] LLM call failed after {API_RETRIES} attempts: {last_err}")


# Helpers (deterministic)

def _tokens(s: str) -> set[str]:
    return set(re.findall(r"[a-z0-9]+", s.lower()))


def _jaccard(a: str, b: str) -> float:
    ta, tb = _tokens(a), _tokens(b)
    return len(ta & tb) / len(ta | tb) if ta and tb else 0.0


def _chunks(text: str, size: int) -> list[str]:
    if len(text) <= size:
        return [text]
    out, cur = [], ""
    for para in text.split("\n"):
        if len(cur) + len(para) + 1 > size and cur:
            out.append(cur)
            cur = ""
        cur += para + "\n"
    if cur:
        out.append(cur)
    return out


def _next_id(reqs: list[dict]) -> int:
    nums = [int(r["id"].split("-")[1]) for r in reqs if r.get("id", "").startswith("REQ-")]
    return max(nums, default=0) + 1


def _valid_sources(sources: Any, docs: list[dict]) -> list[str]:
    valid = {d["id"] for d in docs}
    if isinstance(sources, str):
        sources = [sources]
    return sorted({s for s in (sources or []) if s in valid})


def _doc_block(d: dict, text: str | None = None) -> str:
    return f"=== DOCUMENT {d['id']} | {d['filename']} ===\n{text if text is not None else d['text']}\n"

# Node 1 (deterministic): load documents

def load_documents(state: State) -> dict:
    root = Path(state["input_dir"])
    if not root.is_dir():
        raise SystemExit(f"Input directory not found: {root}")
    files = sorted(p for p in root.rglob("*") if p.is_file() and p.suffix.lower() in TEXT_SUFFIXES)
    if not files:
        raise SystemExit(f"No text documents ({sorted(TEXT_SUFFIXES)}) found in {root}")
    docs = []
    for i, p in enumerate(files, 1):
        docs.append({"id": f"D{i:02d}", "filename": str(p.relative_to(root)),
                     "text": p.read_text(encoding="utf-8", errors="replace")})
    return {"docs": docs, "iteration": 0, "requirements": [], "candidates": [], "gaps": [],
            "glossary": [],
            "log": [f"Loaded {len(docs)} documents from {root}"]}

# Node 2 (LLM): extract requirements per document

EXTRACT_SYSTEM = """You are a requirements engineer. You read ONE source document (an email thread, meeting
minutes, interview, survey, draft specification, ...) and extract every software requirement it contains.

Rules:
- A requirement is a capability, constraint, quality attribute, interface, documentation or operating-environment
  need that the software system must satisfy. Include requirements stated by anyone and requirements that
  are only implied by a stated need (e.g. a request for a report implies the data must be available).
- SILENTLY IGNORE small talk, jokes, personal chatter, restaurants, sports, scheduling, action items, who-will-do-what
  and anything unrelated to the software. Never list these anywhere in your answer.
- Do NOT invent anything not supported by the text. Be specific: keep numbers, parameters, report names, user roles.
- One requirement = one feature a stakeholder would test as a single item. Split statements that bundle unrelated
  features, but do NOT create separate requirements for single columns, counts or fields of the same report:
  list them inside one requirement's description.
- Give each a SHORT descriptive name (3-8 words) and a self-contained explanation of one paragraph
  (what, who needs it, why / acceptance hints). Use neutral, consistent vocabulary: "the system", "staff user",
  "library", "branch", "patron", "item".
- "rejected" is ONLY for statements that look like software requirements but are nonsensical, self-contradictory,
  untestable or clearly out of scope for the software. Give a reason. Normally this list is empty or very short.

Reply with a JSON object:
{"requirements":[{"name":str,"description":str}],
 "rejected":[{"name":str,"description":str,"reason":str}]}"""


def _extract_one(doc: dict, extra: str = "") -> tuple[list, list]:
    reqs, rej = [], []
    for ch in _chunks(doc["text"], CHUNK_CHARS):
        user = _doc_block(doc, ch) + (f"\n{extra}" if extra else "")
        out = call_llm("extract", EXTRACT_SYSTEM, user)
        for r in out.get("requirements", []):
            if r.get("name") and r.get("description"):
                reqs.append({"name": r["name"].strip(), "description": r["description"].strip(),
                             "sources": [doc["id"]]})
        for r in out.get("rejected", []):
            rej.append({"name": r.get("name", "(unnamed)"), "description": r.get("description", ""),
                        "sources": [doc["id"]], "reason": r.get("reason", "Rejected by extractor.")})
    return reqs, rej


def extract_requirements(state: State) -> dict:
    with ThreadPoolExecutor(MAX_WORKERS) as ex:
        results = list(ex.map(_extract_one, state["docs"]))
    cands = [c for r, _ in results for c in r]
    rejected = [x for _, rj in results for x in rj]
    return {"candidates": cands, "blacklist": rejected,
            "log": [f"Extractor: {len(cands)} candidate requirements, {len(rejected)} rejected"]}

# Node 3 (deterministic): pre-deduplication, id assignment, trace sanitising

def pre_dedup(state: State) -> dict:
    docs = state["docs"]
    pool = [dict(r) for r in state.get("requirements", [])]
    black = state.get("blacklist", [])
    added = dropped = 0
    for c in state.get("candidates", []):
        c["sources"] = _valid_sources(c.get("sources"), docs)
        if not c["sources"]:
            dropped += 1                      # OS4: no trace -> not allowed
            continue
        text = c["name"] + " " + c["description"]
        if any(_jaccard(text, b["name"] + " " + b.get("description", "")) >= 0.8 for b in black):
            dropped += 1                      # do not resurrect blacklisted items
            continue
        twin = next((p for p in pool
                     if _jaccard(p["name"], c["name"]) >= 0.85
                     or _jaccard(p["name"] + " " + p["description"], text) >= 0.8), None)
        if twin:                              # near-identical -> merge sources only
            twin["sources"] = sorted(set(twin["sources"]) | set(c["sources"]))
            continue
        pool.append(c)
        added += 1
    n = _next_id(pool)
    for p in pool:
        if not p.get("id"):
            p["id"] = f"REQ-{n:03d}"          # OS2: unique, stable ids
            n += 1
    return {"requirements": pool, "candidates": [],
            "log": [f"Pre-dedup: +{added} new, {dropped} dropped, pool={len(pool)}"]}

# Node 4 (LLM): semantic merge of duplicates (OS3)

MERGE_SYSTEM = f"""You deduplicate a list of software requirements. Find requirements that express the SAME need
(even if worded differently or coming from different documents) and group them.
Rules:
- Only group items that are truly semantically equivalent or where one is fully contained in the other.
  Do NOT group items that merely share a topic, a report or a user role. Different features stay separate.
- A group has at most {MAX_GROUP} items.
- For each group give the merged name (short) and a merged one-paragraph description that keeps every
  distinct detail (numbers, parameters, roles) from all members.
Reply with JSON: {{"groups":[{{"ids":["REQ-001","REQ-007"],"name":str,"description":str}}]}}
Items that have no duplicate must NOT appear."""

def _apply_groups(reqs: list[dict], groups: list[dict], allowed_ids: set[str] | None = None,
                  must_touch: set[str] | None = None, max_group: int = MAX_GROUP) -> tuple[list[dict], int, int]:
    """Apply merge groups proposed by the LLM. Code, not the model, performs the merge.
    allowed_ids: ids shown to the model in this call; must_touch: a group must contain at least one of these
    (used in later rounds so that already merged items are not merged with each other again);
    groups bigger than max_group are rejected. Returns (reqs, removed, skipped_groups)."""
    by_id = {r["id"]: r for r in reqs}
    allowed = set(by_id) if allowed_ids is None else allowed_ids
    used, removed, skipped = set(), 0, 0
    for g in groups:
        if not isinstance(g, dict) or not isinstance(g.get("ids"), list):
            continue
        ids = []
        for item_id in g["ids"]:
            if (isinstance(item_id, str) and item_id in allowed and item_id in by_id
                    and item_id not in used and item_id not in ids):
                ids.append(item_id)
        if len(ids) < 2:
            continue
        if len(ids) > max_group or (must_touch is not None and not (set(ids) & must_touch)):
            skipped += 1
            continue
        keep_id = sorted(ids)[0]
        keep = by_id[keep_id]
        for i in ids:
            if i == keep_id:
                continue
            duplicate = by_id.pop(i)
            keep["sources"] = sorted(set(keep["sources"]) | set(duplicate["sources"]))
            removed += 1
        used.update(ids)
        if isinstance(g.get("name"), str) and g["name"].strip():
            keep["name"] = g["name"].strip()
        if isinstance(g.get("description"), str) and g["description"].strip():
            keep["description"] = g["description"].strip()
        keep["reviewed"] = False          # text changed -> consistency check may edit it again
    return list(by_id.values()), removed, skipped

def _neighbours(fresh: list[dict], settled: list[dict], k: int = NEIGHBOURS) -> set[str]:
    """For every new item, the k most similar already-settled items (so duplicates can be found cheaply)."""
    ids: set[str] = set()
    for f in fresh:
        ft = f["name"] + " " + f["description"]
        ranked = sorted(settled, key=lambda r: _jaccard(ft, r["name"] + " " + r["description"]), reverse=True)
        ids.update(r["id"] for r in ranked[:k])
    return ids

def semantic_merge(state: State) -> dict:
    reqs = list(state["requirements"])
    settled = [r for r in reqs if r.get("settled")]
    # First round: the whole pool is new. Later rounds: only NEW items are compared with the settled pool,
    # so the same items are not merged over and over (which used to erase granularity).
    restrict: set[str] | None = None if not settled else {r["id"] for r in reqs if not r.get("settled")}
    total_removed = total_skipped = 0
    for _ in range(2 if restrict is None else 1):
        if restrict is None:
            pool = sorted(reqs, key=lambda r: r["name"].lower())
        else:
            fresh = [r for r in reqs if r["id"] in restrict]
            near = _neighbours(fresh, [r for r in reqs if r["id"] not in restrict])
            pool = sorted([r for r in reqs if r["id"] in restrict or r["id"] in near],
                          key=lambda r: r["name"].lower())
        batches = [pool[i:i + MERGE_BATCH] for i in range(0, len(pool), MERGE_BATCH)]
        removed_pass = 0
        for b in batches:
            if len(b) < 2:
                continue
            payload = [{"id": r["id"], "name": r["name"], "description": r["description"]} for r in b]
            out = call_llm("merge", MERGE_SYSTEM, json.dumps(payload, ensure_ascii=False))
            reqs, removed, skipped = _apply_groups(reqs, out.get("groups", []), {r["id"] for r in b}, restrict)
            removed_pass += removed
            total_skipped += skipped
        total_removed += removed_pass
        if restrict is not None or len(batches) <= 1 or removed_pass == 0:
            break
    for r in reqs:
        r["settled"] = True
    return {"requirements": reqs,
            "log": [f"Semantic merge: removed {total_removed} duplicates, rejected {total_skipped} over-large/"
                    f"invalid groups, {len(reqs)} left"]}

# Node 5 (LLM): consistency, vocabulary, conflicts, nonsense (OS7, OS9)

CONSISTENCY_SYSTEM = """You are a senior requirements reviewer checking a requirements list for CONSISTENCY.
Do four things:
1. CONFLICTS: find pairs/sets of requirements that cannot both be satisfied (contradictions). For each, decide
   which one to discard (prefer the one with fewer sources, less specific, or contradicted by a more authoritative
   statement) and give a clear reason. If two requirements only look conflicting but can be reconciled, do NOT
   discard: instead rewrite them via "edits" so they are compatible (e.g. "optional" vs "mandatory" -> clarify scope).
2. NONSENSE: flag requirements that are meaningless, untestable, purely personal chatter, or outside the
   software's scope. Give a reason.
3. VOCABULARY: make language consistent. Pick ONE term per concept (e.g. always "patron", never "user/customer"
   for library borrowers; "branch" vs "library" used consistently; "staff user"). Return rewritten name/description
   ONLY for requirements that need changes (keep meaning and details).
4. GLOSSARY: list the canonical terms with one-line definitions.
Reply with JSON:
{"conflicts":[{"ids":[str,str],"discard":str,"reason":str}],
 "nonsense":[{"id":str,"reason":str}],
 "edits":[{"id":str,"name":str,"description":str}],
 "glossary":[{"term":str,"definition":str}]}
Only use ids that appear in the input."""


def consistency_check(state: State) -> dict:
    reqs = state["requirements"]
    payload = [{"id": r["id"], "name": r["name"], "description": r["description"],
                "sources": r["sources"]} for r in reqs]
    out = call_llm("consistency", CONSISTENCY_SYSTEM, json.dumps(payload, ensure_ascii=False))
    by_id = {r["id"]: r for r in reqs}
    new_black = []
    discard: dict[str, str] = {}
    for c in out.get("conflicts", []):
        d = c.get("discard")
        if d in by_id and d not in discard:
            others = ", ".join(i for i in c.get("ids", []) if i != d)
            discard[d] = f"Conflicts with {others}: {c.get('reason', '')}".strip()
    for n in out.get("nonsense", []):
        if n.get("id") in by_id and n["id"] not in discard:
            discard[n["id"]] = f"Discarded as nonsensical/out of scope: {n.get('reason', '')}".strip()
    for i, reason in discard.items():
        r = by_id.pop(i)
        new_black.append({"name": r["name"], "description": r["description"],
                          "sources": r["sources"], "reason": reason})
    edited = 0
    for e in out.get("edits", []):
        r = by_id.get(e.get("id"))
        if r and not r.get("reviewed"):      # already reviewed items are not rewritten again and again
            r["name"] = e.get("name") or r["name"]
            r["description"] = e.get("description") or r["description"]
            edited += 1
    for r in by_id.values():
        r["reviewed"] = True
    glossary = out.get("glossary") or state.get("glossary", [])
    return {"requirements": list(by_id.values()), "blacklist": new_black, "glossary": glossary,
            "log": [f"Consistency: {len(new_black)} discarded, {edited} edited"]}

# Node 6 (LLM): completeness review -> decides whether to loop (OS8, ANS3)

COMPLETENESS_SYSTEM = """You are an independent auditor. You get (a) one part of the corpus of source documents and
(b) the current list of requirements (id, name, short description) and the list of deliberately discarded items.
Find requirements stated or clearly implied in THIS PART of the corpus that are MISSING from the list (and are not
covered by a discarded item). A requirement is NOT missing if an existing item already covers it, even under a
broader name: read the descriptions. Ignore small talk and duplicates of existing items.
For each missing requirement give a short name, a self-contained description (one or two sentences) and the ids of
the documents (e.g. "D03") that contain it.
Reply with JSON: {"missing":[{"name":str,"description":str,"sources":[str]}]}
If nothing is missing reply {"missing":[]}."""

def _corpus_blocks(docs: list[dict]) -> tuple[list[tuple[list[dict], str]], list[str]]:
    """Split the corpus into parts that fit CORPUS_CHARS, so that nothing is silently cut off."""
    blocks, cur_docs, cur_txt, size, truncated = [], [], [], 0, []
    for d in docs:
        txt = _doc_block(d)
        if len(txt) > CORPUS_CHARS:
            txt, _ = txt[:CORPUS_CHARS], truncated.append(d["id"])
        if cur_docs and size + len(txt) > CORPUS_CHARS:
            blocks.append((cur_docs, "".join(cur_txt)))
            cur_docs, cur_txt, size = [], [], 0
        cur_docs.append(d)
        cur_txt.append(txt)
        size += len(txt)
    if cur_docs:
        blocks.append((cur_docs, "".join(cur_txt)))
    return blocks, truncated

def completeness_review(state: State) -> dict:
    docs = state["docs"]
    listing = [{"id": r["id"], "name": r["name"], "description": r["description"][:220]}
               for r in state["requirements"]]
    black = [b["name"] for b in state.get("blacklist", [])]
    blocks, truncated = _corpus_blocks(docs)
    gaps: list[dict] = []
    for _, corpus in blocks:
        user = (f"CURRENT REQUIREMENTS:\n{json.dumps(listing, ensure_ascii=False)}\n\n"
                f"DISCARDED:\n{json.dumps(black, ensure_ascii=False)}\n\nCORPUS PART:\n{corpus}")
        out = call_llm("completeness", COMPLETENESS_SYSTEM, user)
        for g in out.get("missing", []):
            src = _valid_sources(g.get("sources"), docs)
            if not (g.get("name") and src):
                continue
            twin = next((x for x in gaps if _jaccard(x["name"], g["name"]) >= 0.7), None)
            if twin:
                twin["sources"] = sorted(set(twin["sources"]) | set(src))
            else:
                gaps.append({"name": g["name"], "description": g.get("description", ""), "sources": src})
    note = f" ({len(blocks)} corpus parts)" if len(blocks) > 1 else ""
    log = [f"Completeness review (iteration {state.get('iteration', 0)}): {len(gaps)} gaps found{note}"]
    if truncated:
        log.append(f"WARNING: documents {', '.join(truncated)} are longer than CORPUS_CHARS and were cut "
                   f"for the completeness review")
    return {"gaps": gaps, "log": log}

def route_after_review(state: State) -> str:
    if not state.get("gaps"):
        return "prioritize"
    if state.get("iteration", 0) < state.get("max_iterations", 2):
        return "gap_extract"
    return "adopt_gaps"

def adopt_gaps(state: State) -> dict:
    """Loop limit reached but the auditor still reports gaps: add them as requirements (deterministically,
    through the same dedup/trace checks) instead of silently dropping them. They are named in the log."""
    cands = [{"name": g["name"], "description": g["description"] or g["name"],
              "sources": g["sources"]} for g in state["gaps"]]
    res = pre_dedup({**state, "candidates": cands})
    names = "; ".join(g["name"] for g in state["gaps"])
    return {"requirements": res["requirements"], "gaps": [],
            "log": [f"Adopted {len(cands)} auditor-reported gaps after the loop limit (not re-reviewed): {names}"]}

# Node 7 (LLM): targeted re-extraction of reported gaps (closes the loop)

def gap_extract(state: State) -> dict:
    docs = {d["id"]: d for d in state["docs"]}
    per_doc: dict[str, list[dict]] = {}
    for g in state["gaps"]:
        for s in g["sources"]:
            per_doc.setdefault(s, []).append(g)

    def work(item):
        did, gaps = item
        hint = ("An auditor found that the following requirements are MISSING from the extraction of this "
                "document. Extract ONLY these (written as full requirements, per the rules above):\n"
                + json.dumps([{"name": g["name"], "description": g["description"]} for g in gaps],
                             ensure_ascii=False))
        return _extract_one(docs[did], hint)

    with ThreadPoolExecutor(MAX_WORKERS) as ex:
        results = list(ex.map(work, per_doc.items()))
    cands = [c for r, _ in results for c in r]
    rejected = [x for _, rj in results for x in rj]
    it = state.get("iteration", 0) + 1
    return {"candidates": cands, "blacklist": rejected, "iteration": it, "gaps": [],
            "log": [f"Gap extraction (iteration {it}): {len(cands)} new candidates"]}

# Node 8 (LLM): prioritisation (OS6)

PRIORITY_SYSTEM = f"""You assign MoSCoW priorities to software requirements for the FIRST release.
Scale:
{json.dumps(PRIORITY_SCALE, indent=1)}
Decide with this procedure, in order, and stop at the first step that applies:
1. WON'T: the text explicitly postpones, defers, excludes or leaves the item undecided.
2. MUST: a legal/regulatory/accessibility obligation; security or data-integrity need; the stakeholders call it
   critical/essential/non-negotiable/high priority; or it is a prerequisite of another requirement. Test: "could we
   go live without it?" If yes, it is NOT a Must.
3. SHOULD: clearly requested and valuable, but a workaround exists (manual work, export, ad-hoc query).
4. COULD: everything else (convenience, polish, speculative wishes).
Judge by importance to the stakeholders' stated needs. n_sources (number of documents mentioning the item) is a WEAK
hint only: a single-document requirement can be Must, and one mentioned everywhere can be only Should.
Do not force a distribution; use only the levels that fit.
You MUST return exactly one entry for EVERY id in the input.
Reply with JSON: {{"priorities":[{{"id":str,"priority":"Must|Should|Could|Won't","rationale":str}}]}}
rationale = "<criterion>: <short evidence>", e.g. "Accessibility obligation: Section 508 stated as required" or
"Workaround exists: staff can export and sort manually"."""

def prioritize(state: State) -> dict:
    reqs = state["requirements"]

    def ask(items: list[dict]) -> dict[str, dict]:
        payload = [{"id": r["id"], "name": r["name"], "description": r["description"][:400],
                    "n_sources": len(r["sources"])} for r in items]
        out = call_llm("prioritize", PRIORITY_SYSTEM, json.dumps(payload, ensure_ascii=False))
        return {p["id"]: p for p in out.get("priorities", [])
                if isinstance(p, dict) and p.get("priority") in PRIORITIES and "id" in p}

    got: dict[str, dict] = {}
    for i in range(0, len(reqs), PRIORITY_BATCH):
        batch = reqs[i:i + PRIORITY_BATCH]
        res = ask(batch)
        missing = [r for r in batch if r["id"] not in res]
        if missing:                           # one retry for items the model skipped
            res.update(ask(missing))
        got.update(res)
    fallback = 0
    for r in reqs:
        p = got.get(r["id"])
        if p:
            r["priority"], r["rationale"] = p["priority"], p.get("rationale", "")
        else:  # deterministic fallback so that every requirement has a valid priority
            fallback += 1
            r["priority"] = "Must" if len(r["sources"]) >= 3 else "Should" if len(r["sources"]) == 2 else "Could"
            r["rationale"] = f"Fallback: based on number of supporting documents ({len(r['sources'])})."
    return {"requirements": reqs, "log": [f"Prioritisation done ({fallback} of {len(reqs)} via fallback)"]}

# Node 9 (deterministic): validate + assemble the final document (OS1, OS2, OS4, OS5, OS6, OS9)

def _validate(reqs: list[dict], docs: list[dict]) -> list[str]:
    problems, seen = [], set()
    valid_docs = {d["id"] for d in docs}
    for r in reqs:
        if r["id"] in seen:
            problems.append(f"duplicate id {r['id']}")
        seen.add(r["id"])
        if not r.get("sources") or not set(r["sources"]) <= valid_docs:
            problems.append(f"{r['id']}: invalid/missing sources")
        if r.get("priority") not in PRIORITIES:
            problems.append(f"{r['id']}: invalid priority")
        if not r.get("name") or not r.get("description"):
            problems.append(f"{r['id']}: missing name/description")
    return problems

def assemble_document(state: State) -> dict:
    docs, reqs = state["docs"], state["requirements"]
    fname = {d["id"]: d["filename"] for d in docs}
    reqs = [{k: v for k, v in r.items() if k not in ("settled", "reviewed")}
            for r in sorted(reqs, key=lambda r: r["id"])]
    problems = _validate(reqs, docs)
    black = state.get("blacklist", [])
    for i, b in enumerate(black, 1):
        b["id"] = f"BL-{i:03d}"
        b["sources"] = _valid_sources(b.get("sources"), docs)

    L = ["# Software Requirements Specification (generated)", "",
         f"Generated from {len(docs)} input documents by the requirements-refinement agentic network.", "",
         "## 1. Priority scale", "", "| Priority | Meaning |", "|---|---|"]
    L += [f"| **{k}** | {v} |" for k, v in PRIORITY_SCALE.items()]
    L += ["", "## 2. Source documents", "", "| ID | File |", "|---|---|"]
    L += [f"| {d['id']} | {d['filename']} |" for d in docs]
    if state.get("glossary"):
        L += ["", "## 3. Glossary (canonical vocabulary)", "", "| Term | Definition |", "|---|---|"]
        L += [f"| {g.get('term', '')} | {g.get('definition', '')} |" for g in state["glossary"]]
    L += ["", "## 4. Requirements summary", "", "| ID | Name | Priority | Sources |", "|---|---|---|---|"]
    L += [f"| {r['id']} | {r['name']} | {r['priority']} | {', '.join(r['sources'])} |"
          for r in sorted(reqs, key=lambda r: (PRIORITIES.index(r["priority"]), r["id"]))]
    L += ["", "## 5. Requirements", ""]
    for r in reqs:
        L += [f"### {r['id']} — {r['name']}", "",
              f"- **Priority:** {r['priority']} — {r.get('rationale', '')}",
              f"- **Derived from:** " + ", ".join(f"{s} ({fname[s]})" for s in r["sources"]), "",
              r["description"], ""]
    L += ["## 6. Discarded items (blacklist)", ""]
    if black:
        for b in black:
            L += [f"### {b['id']} — {b['name']}", "",
                  f"- **Derived from:** " + (", ".join(f"{s} ({fname[s]})" for s in b["sources"]) or "n/a"),
                  f"- **Reason for discarding:** {b['reason']}", "",
                  b.get("description", ""), ""]
    else:
        L += ["_No items were discarded._", ""]
    L += ["## 7. Generation notes", ""]
    L += [f"- {x}" for x in state.get("log", [])]
    if state.get("gaps"):
        L += ["- Gaps still reported by the completeness auditor when the loop limit was reached:"]
        L += [f"  - {g['name']} (sources: {', '.join(g['sources'])})" for g in state["gaps"]]
    if problems:
        L += ["- **Validation problems:** " + "; ".join(problems)]
    else:
        L += ["- Validation passed: unique ids, valid traces, valid priorities."]

    md_path = Path(state["output"])
    md_path.parent.mkdir(parents=True, exist_ok=True)
    md_path.write_text("\n".join(L) + "\n", encoding="utf-8")
    return {"output_path": str(md_path), "log": [f"Wrote {md_path}"]}

# Graph

def build_graph():
    g = StateGraph(State)
    g.add_node("load_documents", load_documents)            # deterministic
    g.add_node("extract_requirements", extract_requirements)  # LLM
    g.add_node("pre_dedup", pre_dedup)                      # deterministic
    g.add_node("semantic_merge", semantic_merge)            # LLM
    g.add_node("consistency_check", consistency_check)      # LLM
    g.add_node("completeness_review", completeness_review)  # LLM (feedback)
    g.add_node("gap_extract", gap_extract)                  # LLM
    g.add_node("adopt_gaps", adopt_gaps)                    # deterministic
    g.add_node("prioritize", prioritize)                    # LLM
    g.add_node("assemble_document", assemble_document)      # deterministic

    g.add_edge(START, "load_documents")
    g.add_edge("load_documents", "extract_requirements")
    g.add_edge("extract_requirements", "pre_dedup")
    g.add_edge("pre_dedup", "semantic_merge")
    g.add_edge("semantic_merge", "consistency_check")
    g.add_edge("consistency_check", "completeness_review")
    g.add_conditional_edges("completeness_review", route_after_review,
                            {"gap_extract": "gap_extract", "adopt_gaps": "adopt_gaps",
                             "prioritize": "prioritize"})
    g.add_edge("gap_extract", "pre_dedup")                  # <- feedback loop
    g.add_edge("adopt_gaps", "prioritize")
    g.add_edge("prioritize", "assemble_document")
    g.add_edge("assemble_document", END)
    return g.compile()

def main() -> None:
    ap = argparse.ArgumentParser(description="Requirements refinement agentic network")
    ap.add_argument("--input-dir", required=True, help="directory with the input text documents")
    ap.add_argument("--output", required=True, help="path of the output Markdown file")
    ap.add_argument("--max-iterations", type=int, default=2, help="max completeness feedback loops")
    a = ap.parse_args()
    if not os.getenv("OPENAI_API_KEY"):
        raise SystemExit("Set OPENAI_API_KEY.")
    final = build_graph().invoke({"input_dir": a.input_dir, "output": a.output,
                                  "max_iterations": a.max_iterations})
    print("\n".join(final["log"]))
    print(f"\nOutput: {final['output_path']}")

if __name__ == "__main__":
    main()