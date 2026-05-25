---
layout: post
title: "The Authoring Layer"
date: 2026-05-25
type: phase-update
entry_type: note
subtype: diary
projects: [droolsvol2]
tags: [rete, authoring, incremental, changeset, drools-vol2]
---

The last entry ended with an observation: `RuleBaseModifier.apply()` computes the delta
but then discards it, passing the full `UnitDescriptor` to the engine. Every changeset
meant a full rebuild. I'd named the problem. Fixing it took longer than I expected —
not because the engine patching was hard, but because the design conversation kept expanding.

The starting question was simple: pass the delta to the engine instead of the full
descriptor. But tracing what "apply a changeset" actually means revealed constraints
I hadn't fully articulated before.

Packages shouldn't be directly mutable. Users shouldn't call
`RuleBaseModifier.with(rb).apply()` for day-to-day rule authoring — that's the wrong
granularity. If you want to author rules before committing them to a live rulebase, you
need a scoped session with explicit lifecycle, not raw modifier access.

`AuthoringSession` is what emerged. You create it from a `RuleBase` — any `RuleBase`,
including an empty one. It records the rulebase's generation at that point. You apply
changesets freely, accumulating intent without touching the rulebase. When ready,
`syncTo(ruleBase)` validates that nobody else has modified the rulebase since you opened
the session, then delegates to `RuleBaseModifier` atomically.

```java
RuleBuilder<CTX> builder = new RuleBuilder<>();

AuthoringSession<CTX> session = AuthoringSession.from(rb);
session.apply(changeSet()
    .selectPackage("org.example").selectUnit("Rules")
    .add(builder.rule("adults")
            .from(CTX::persons).filter(p -> p.age() > 18)
            .ifn(p -> fired.add(p.name()))));
session.syncTo(rb);  // validates generation stamp, applies atomically
```

The generation stamp is optimistic locking — cheap for the common case where one
session owns the rulebase for its lifetime. If someone else modified the rulebase
while you were authoring, you get a `StaleSessionException`. Re-open and start again.

Net delta uses set-diff: snapshot the rule lists at `from()`, compare at `syncTo()`.
Add a rule then remove it in the same session — the net delta is empty. Simpler than
incremental folding, correct by definition.

`RuleBaseFactory` followed from the same principle. "RuleBase exposes nothing directly"
has to apply to construction too. Package-private constructor, factory as the single
entry point — the same discipline as `RuleBaseModifier` for mutation.

## The wrong layer

The incremental engine patching — `EvaluationEngine.apply(compiled, added, removed, rete)`
— has a specific invariant: called from `RuleBaseModifier`, never from `RuleBase`.
`RuleBase.applyAndFinalize()` is structural only: build Rete nodes, swap containers,
finalize. Engine lifecycle decisions belong to the modifier.

A separate Claude reviewing the implementation found that `engine.apply()` had landed
inside `applyAndFinalize()` — put there to make the tests pass. We moved it back and
accepted two failing tests until the orchestration step landed. They did.

The finding mattered less than the sequence: check the design first, then check the
code quality. Reviewing well-written code in the wrong architectural layer is wasted
effort.

## Residue from the past

`ReteEngineTest` had a `useReteEngine()` helper that called
`desc.setEngine(new ReteEngine<>())`. Since `ReteEngine` is now the default, all sixteen
call sites were no-ops. We removed the helper.

Test method names had accumulated several styles: three-part underscores, numbered tests,
PascalCase after underscores. The Google Java Style Guide permits one underscore in test
method names — `subject_state`, both components lowerCamelCase. Thirty renames cleaned
it up.
