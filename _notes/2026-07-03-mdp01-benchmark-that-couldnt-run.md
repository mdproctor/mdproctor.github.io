---
layout: post
title: "Hortora Engine — The Benchmark That Couldn't Run"
date: 2026-07-03
type: phase-update
entry_type: note
subtype: diary
projects: [hortora-engine]
tags: [bge-m3, onnx, benchmark, retrieval, neocortex]
---

# Hortora Engine — The Benchmark That Couldn't Run

**Date:** 2026-07-03
**Type:** phase-update

---

## What I was trying to achieve: establish the BGE-M3 retrieval baseline

The ONNX export landed last session — BGE-M3's three heads (dense, sparse, ColBERT) baked into one model file. The next step was obvious: run the 14 real-world benchmark scenarios against the four-signal pipeline and see if it beats the three-leg baseline at 94% precision. That number is what #33 (fusion experiments) and #34 (quantization) both need before they can start.

## What we believed going in: the hard part was done

The model was exported, the benchmark harness existed from #28, and the analysis was a matter of comparing BGE-M3 results against `three-leg.json`. I expected the design to take an hour and the implementation to take two. The actual benchmark run was the only uncertain part — 2095 garden entries through a 550M parameter model on CPU.

## The export was broken in a way that looked fine

The `model.onnx` file existed. It was 3.1MB. It had valid ONNX magic bytes. The checksums matched. But it was just the graph — the 2.1GB weight tensor file was missing entirely.

`torch.onnx.export` for models over 2GB needs to use external data format, splitting the output into `model.onnx` (graph structure) and `model.onnx.data` (weights). The export script from last session didn't pass the flag. The file it produced was structurally valid ONNX — it would even load into an `OrtSession` — but every weight was uninitialised.

Claude caught the parameter name issue when we tried to fix it. The spec said `use_external_data_format=True`, which is what every tutorial and Stack Overflow answer uses. torch 2.12 renamed it to `external_data` with no deprecation warning. The TypeError was clear enough — `unexpected keyword argument` — but nothing in the error pointed to the replacement. We found it via `inspect.signature(torch.onnx.export)`.

After that fix, the export ran clean: 2.1GB weights file, validation passed against PyTorch for six test sentences including multilingual and repeated-token edge cases.

## Three scripts and a design review

The benchmark needed three pieces of code: the export fix itself, a `--min-points` CLI argument for the benchmark harness (the garden grew from 1900 to 7050 entries since the last run), and `analyze_bge_m3.py` to compare results against the three-leg baseline.

I scoped this as a pipeline-level go/no-go gate — not a controlled model comparison. BGE-M3 changes the dense model, sparse model, and adds ColBERT reranking simultaneously. Attributing precision changes to individual signals is #33's problem. This benchmark answers one question: does the target pipeline meet the quality bar?

The design review pushed back on the framing. The original spec used attribution language in the per-failure-mode analysis — "does BGE-M3's learned sparse close the gaps that SPLADE couldn't?" — which implies causal claims the benchmark can't support. The review also caught that the three-leg 94% baseline was computed from scored entries only, with 87 entries unscored. Both are methodological caveats that the report now carries explicitly.

## Then the engine wouldn't ingest

With the code done and the model exported, I started the engine in dev mode against a fresh Qdrant. It started cleanly, loaded the ONNX model, started the filesystem watcher. No errors. No warnings beyond a Qdrant version check. Search returned empty results. Qdrant had zero collections.

The first red herring was the `casehub.corpus.corpora.garden.source` property. The engine's `CorpusBindingProducer` warned that no storage config existed for the garden corpus, which looked like a missing property. Adding it created a second corpus binding — one from the config-driven producer, one from the engine's own `GardenBindingProducer`. Both watched the same directory, shared the same cursor key, and the first to run consumed all the changes before the second could process them.

The real issue is deeper. Even with only one binding, the `CorpusIngestionService` runs its `fullScan`, walks 11,689 files (including the `.git/` directory), saves a 674KB cursor — and produces zero chunks. No errors at any log level. The cursor is saved because `anyFailure` stays false when `allChunks` is empty. On next startup, `changesSince(cursor)` returns nothing because the filesystem hasn't changed. The engine looks healthy. The garden is invisible.

This is a neocortex SNAPSHOT regression — the same engine ran three-leg benchmarks successfully two weeks ago with 2026 indexed points. Something in the recent rename or BGE-M3 migration commits broke the ingestion pipeline silently.

## Where this leaves us

The benchmark code is complete: export fix, harness improvement, analysis script with tests. The design review tightened the spec. Three garden entries capture the gotchas. But the actual benchmark run is blocked on casehubio/neocortex#67 — the ingestion pipeline that won't ingest.

The irony isn't lost on me that the retrieval benchmark is blocked by the retrieval engine's inability to retrieve. The code is ready. The model is ready. The engine starts, accepts queries, and returns empty results with perfect confidence.
