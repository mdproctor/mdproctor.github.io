---
layout: note
title: "CaseHub Work — Making Progress Extensible"
date: 2026-08-04
entry_type: note
subtype: diary
type: phase-update
projects: [casehub-work]
tags: [progress, extensibility, rollback, casehub]
published: false
---

# CaseHub Work — Making Progress Extensible

**Date:** 2026-08-04
**Type:** phase-update

---

## What we were trying to achieve: extend the progress subsystem beyond its three built-in shapes

The progress model shipped with percentage, count, and step shapes. Enough to cover the real cases. But three shapes is a ceiling, not a demonstration of what the platform can do. I wanted to show that progress tracking is genuinely extensible — that a consumer can bring their own domain-specific shape and get the same validation, rollback detection, and event semantics as the built-in ones.

Three things were deferred from the original spec: a custom JSON schema shape type (#307), visualisation mode hints (#309), and a rollback control mechanism (#308). This session delivered all three.

---

## The custom shape: extensibility through definition

The `custom` shape type stores a JSON Schema in the existing `definition` field and validates state against it on every update. No new concepts — the `definition` field already existed for the step shape's DAG definition. A consumer defines their schema once at creation time, and every subsequent state update is validated against it.

The interesting design question was rollback detection. For built-in shapes, we know the semantics — a percentage decreasing is a rollback, a count going down is a rollback. For a custom shape, we don't know what "backward" means. Three tiers handle this:

1. No rollback config → no detection. State changes are always `STATE_UPDATED`.
2. `rollbackField: "score"` → numeric regression on a named field.
3. `rollbackDetectorId: "deployment-health"` → a pluggable `CustomRollbackDetector` resolved via `StrategyResolver`.

The tiers compose. Most consumers won't need rollback detection at all. Those who do pick the level of sophistication they need.

---

## The rollback puzzle: why "undo last change" is harder than it sounds

The rollback control mechanism started as the simplest feature and turned into the most interesting. The lean scope: a rollback policy field (`"denied"` blocks accidental backward movement), a convenience endpoint (`POST /rollback` undoes the last state change), and a snapshot query.

The naive algorithm — take the `previousState` of the most recent event — oscillates. Call rollback twice and you're back where you started, because the first rollback emitted an event that the second one undoes.

The obvious fix — skip `ROLLED_BACK` events when scanning — breaks when a user legitimately updates state backward via the normal `PUT /state` endpoint. That auto-detects as `ROLLED_BACK` too, and skipping it means the undo jumps over a change the user made deliberately.

The root problem: organic backward movement and explicit rollback both emit the same `ROLLED_BACK` changeType. We can't tell them apart from the event trail.

We solved this with a forward-state-sequence algorithm. Build the list of states that were set by `CREATED` and `STATE_UPDATED` events — the forward progression, ignoring all `ROLLED_BACK` events. Find the current state's position in that list. Return the one before it.

Consecutive rollbacks walk back through the forward history: S0 → S1 → S2, first rollback → S1, second rollback → S0. No oscillation. If the current state isn't in the forward sequence (because it was set by an organic backward movement), a fallback path finds the event that produced it and undoes it — restoring the state before the regression.

The asymmetry between the rollback policy and the rollback endpoint is deliberate. `rollbackPolicy: "denied"` protects against accidental backward movement via `PUT /state`. The explicit `POST /rollback` endpoint bypasses it — it's an intentional undo, not an accident.

---

## Visualisation modes: the simplest feature

A `visualisationMode` string field on `ProgressInstance`. Set at creation, returned on queries, ignored by the platform. Consumers read it alongside `shapeType` and decide how to render. Platform constants (`"gauge"`, `"progress-bar"`, `"step-list"`, `"timeline"`, `"tree-map"`, `"count-badge"`) are conventions, not enforcement. A consumer can use `"gantt"` without waiting for a platform release.

Four tests proved the round-trip works. The entire feature is a single nullable column and a constant class.

---

## What this unlocks

Custom shapes mean the progress subsystem can represent domain-specific progress without waiting for platform releases. Visualisation hints give consumers a rendering convention without prescribing implementation. Rollback controls let orchestrators protect progress state from accidental regression while keeping deliberate undo available.

Multi-instance coordinated rollback — rolling back an entire subtree atomically — is filed as #332 under the federation epic (#92). The single-instance foundation built here is the prerequisite.
