---
layout: post
title: "The Body Was Already There"
date: 2026-05-22
type: phase-update
entry_type: note
subtype: diary
projects: [droolsvol2]
tags: [rete, architecture, rule-descriptor, pattern, drools-base]
---

The branch started as a filter bug. `storeFilter()` in `RuleBuilder` used
`List.set(size-1, pred)` — overwriting, not accumulating. Chain two `.filter()`
calls and you keep only the last one, silently. No error, no warning. Once I saw
it, I wanted to fix it properly rather than just patch the overwrite.

"Properly" turned out to mean rethinking where rule body state lives.

The existing `RuleDescriptor` was a parallel flat-list shadow of `RuleImpl.body` —
sources here, filters there, head elsewhere, scopes in a fourth list. None of it
was in `RuleImpl`. The `GroupElement` tree was used only to build the Rete network;
the evaluation engine read a completely separate structure. Two sources of truth,
kept in sync by convention.

I asked Claude to check whether vol1's `EntryPointId` was the equivalent of vol2's
DataSource accessor. It is: `EntryPointId extends ConditionalElement implements
PatternSource` sits in `Pattern.source`, keyed by a String name resolved at session
creation. Vol2 needs the same slot, keyed by a method reference instead of a String.
`DataSourceId` is one new class — no new base infrastructure.

The same logic applied to filters. `Pattern.constraints` already holds
`List<Constraint>` — accumulating, multiple per pattern. A `LambdaConstraint` with
an explicit `arity` field (1 = alpha, >1 = beta) replaces the reflection-based
detection entirely. The alpha/beta distinction is now encoded at store time, not
inferred at wire time.

For fn/ifn: vol2's claim has always been that fn/ifn can appear anywhere in the body,
not just at the terminal. Pulling them out as a head wrapper — which is what
`ImmediateHead`/`DeferredHead` did — was a vol1 consequence-at-leaf holdover. Two new
`GroupElement.Type` values (`FN`, `IFN`) with a `consequence` field make fn/ifn
first-class body elements at their declared position.

`RuleDescriptor`, `ScopeDescriptor`, `RULE_STATE`, `ImmediateHead`, `DeferredHead` —
all gone. `RuleImpl.body` is the body.

## The one catch

The code review flagged that `GroupElement.clone(boolean)` is a manual field-copy
method. Add a field, forget to add a copy line, and cloned rule bodies silently drop
it. The new `consequence` field wasn't copied — the clone would produce FN/IFN nodes
with null consequences after `LogicTransformer` touches the body. Fixed before merge.

## What RuleBaseModifier is actually for

Toward the end of the session I noticed that `RuleBaseModifier.apply()` builds a
changeset with the delta but then passes the full `UnitDescriptor` to the engine —
not the delta. The engine does a full rebuild every time any rules change.

That's a separate issue, but naming it clarified something I'd wanted to articulate
for a while. `RuleBaseModifier` isn't just ergonomics — it's a replaceable strategy.
In vol1, session creation was put directly on `KieBase`. Once consumers depended on
it, it couldn't be moved. The modifier indirection means the mutation strategy can be
deprecated and replaced without touching `RuleBase`'s public surface. Different
modifier implementations can coexist. The rule is: if something might need to change,
it belongs on the modifier.
