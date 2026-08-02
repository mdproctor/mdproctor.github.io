---
layout: post
title: "When Knowledge Forgets Where It Came From"
date: 2026-08-02
type: phase-update
entry_type: note
subtype: diary
projects: [trellis]
tags: [garden, provenance, knowledge-management, cbr]
---

## When Knowledge Forgets Where It Came From

The garden has been running for months now — a corpus of gotchas, techniques, and undocumented behaviours that Claude searches during brainstorming and work-start. It works. I search for "CDI restart," get back the entry about `@InjectMock` triggering Quarkus CDI profile recalculation, and that knowledge shapes how I design a test strategy. The right decision gets made because the right knowledge surfaced at the right time.

But the connection vanishes the moment I move on. A month later, someone asks why the test suite avoids `@InjectMock` on `@ApplicationScoped` beans. The answer is in a garden entry — GE-20260618-c552c3 — but nothing links that entry to the spec it informed. The knowledge did its job and left no trace.

This is the provenance problem: knowledge systems that retrieve well but don't remember what they influenced. You can search the garden, but you can't ask "which design decisions did this entry shape?" or "what knowledge informed issue #14?"

### The architecture question

I started with the obvious approach — `.provenance.yaml` files sitting next to specs, version-controlled in git. Record the GE-IDs during brainstorming, ship the file with the spec. It's the same pattern the garden itself uses: files are truth, indexes are caches.

Claude pushed back: why not centralise through the engine? The engine already owns the garden corpus (Qdrant), retrieval tracking (SQLite), and all the search infrastructure. Provenance is garden usage metadata — the same category as retrieval tracking. Making trellis own provenance would mean two systems tracking garden usage, with reverse lineage queries requiring filesystem scans across every workspace.

I agreed. The engine gets a `provenance` table in SQLite, REST endpoints for recording and querying, and a new MCP tool (`gardenRecordProvenance`) that the brainstorming and work-start skills call after the user selects relevant entries. Trellis becomes a pure UI client — it calls the engine for search, entry detail, and lineage queries, enriches the results with workspace context from its own scanner, and presents them in a Garden View.

The design review caught several things worth fixing before implementation. The original unique constraint on `(issue_repo, issue_number, ge_id, spec_name)` would silently allow duplicates when `spec_name` was NULL — SQL NULL semantics. The fix: `spec_name` as `NOT NULL DEFAULT ''` with a 3-column constraint and UPSERT semantics that update the spec name when it becomes known. The review also pushed the provenance store into its own SQLite file, separate from the retrieval-tracking DB — provenance is hortora-specific metadata, retrieval tracking is a casehub-generic library concern.

### Three signals

The garden now has two usage signals, with a third designed and filed:

**Retrieval** — automatic. The engine records every search query and which entries were returned. This existed before. It answers "what gets surfaced?" but not "what gets used."

**Provenance** — explicit. Skills record which entries the user selected as relevant for a specific issue. This is what we built. It answers "which knowledge informed which design decisions?" and supports both forward lineage (issue → GEs) and reverse lineage (GE → issues).

**Outcome** — future. After the work is done, did the garden entry actually help? Was it accurate? Outdated? Misleading? This is filed as engine#74 and will build on the casehub CBR infrastructure — `CbrOutcome` with `SUCCESS/PARTIAL/FAILURE`, `adjustConfidence()` with a learning rate that drifts entry confidence toward its true value over time. The CBR API already exists in `casehub-neocortex-memory-api` — `CbrCase`, `CbrCaseMemoryStore.recordOutcome()`, the full model. It's sitting there waiting to be plugged in.

The three signals form a funnel: retrieval is broad (what was found), provenance is narrow (what was used), outcome is evaluative (was it good). Together they close the loop — the garden can learn which entries actually deliver value and surface them more aggressively, while entries that consistently mislead can be flagged for revision.

### The Garden View

Trellis now has a `#garden` route — a search panel on the left, entry detail on the right. Search hits the engine's adaptive endpoint (the same 5-signal hybrid retrieval with cross-encoder reranking that powers `gardenSearch` MCP). Results show domain badges, type badges, and cross-encoder scores. Click an entry and the detail panel loads the full markdown body plus a usage map showing which issues this entry has informed.

The provenance stats dashboard at the bottom shows total records, unique entries referenced, unique issues tracked, and the top-referenced entries. Right now it's all zeros — no skills have recorded provenance yet, because the updated brainstorming and work-start skills need to run against a real issue first. The next brainstorming session will be the first to write provenance.

### Where this leads

The interesting question isn't the plumbing — it's what becomes possible when knowledge tracks its own influence. A garden entry that informed 15 design decisions across 8 repos is a different kind of knowledge than one that was never consulted. The first is load-bearing; retiring it requires understanding what it supports. The second is a candidate for pruning.

With outcome tracking (engine#74), the signals get richer. An entry consulted 15 times with a 0.9 success rate is validated knowledge. One consulted 15 times with a 0.3 success rate is actively misleading — every consultation costs more than it saves. CBR's `adjustConfidence()` makes this automatic: the entry's confidence drifts toward its true value with every outcome recorded, no manual curation needed.

The garden started as a flat corpus of markdown files. It's becoming something closer to a memory system — one that knows not just what it contains, but how its contents are being used, by whom, and whether they're helping.
