---
layout: post
title: "The Evaluation Engine Seam"
date: 2026-05-12
type: phase-update
entry_type: note
subtype: log
projects: [droolsvol2]
tags: [rete, architecture, evaluation-engine]
---

`wireHead()` lived inside `UnitInstance`, and it was always borrowed time. Hundreds of lines reading `RuleDescriptor` sources directly, walking the Rete with `findJoinNode()`, branching on 1 vs 2 vs N sources. I put it there to get the tests green — 103 of them. The real engine belongs somewhere else.

I brought Claude in to work through the design and wire in the seam.

## Compile once, create fast

The constraint that shaped everything: unit instance creation is on the hot path. It happens at RuleUnit activation time, under real latency pressure. All heavy computation belongs at compile time — once per rulebase change, amortised across every unit instance that follows.

We landed on two phases:

```java
interface EvaluationEngine<CTX> {
    CompiledEngine<CTX> compile(UnitDescriptor<CTX> descriptor, EntryPointNode rete);
}
interface CompiledEngine<CTX> {
    UnitInstance<CTX> createUnit(CTX ctx);
    void disposeUnit(UnitInstance<CTX> unit);
}
```

`compile()` resolves slot mappings, creates processor instances, wires the Router. `createUnit()` subscribes those pre-created processors and registers the unit for dispatch — close to free.

The observation that makes sharing work: `UnitProcessor` implementations — `JoinLeftInlet`, `JoinRightInlet`, `Filter1UnitProcessor` — carry no runtime state in their fields. All per-unit state flows through the `UnitInstance` parameter at call time. The same processor instances serve every unit of the same type. Create once, share across all.

## O(1) Router dispatch

The current Router holds `List<List<UnitProcessor>>` — an inner list per slot. On every DataStore event it iterates the list: linear in the number of rules on that slot.

The right design: `UnitProcessor[]` — one array entry per slot, O(1) lookup. Fan-out to multiple rules on the same slot is pre-compiled into a single composite processor at `compile()` time; the Router never knows it's there. This isn't in yet — it belongs to the real Rete engine, not the brute-force stub.

## UnitInstance stripped to state

After the refactor, `UnitInstance` is about 40 lines — memories, agenda, context:

```java
public class UnitInstance<CTX> {
    private final ContextPojoDS<CTX> context;
    private final Agenda agenda = new Agenda();
    private final NodeMemories nodeMemories = new SimpleNodeMemories();
    // ...
}
```

No Router reference, no wiring logic. The brute-force code moved to `BruteForceCompiledEngine` — same logic, clearly labelled temporary. `BruteForceEngine` is the stateless factory singleton; `UnitDescriptor` defaults to it.

One mistake on the way. I put `BruteForceCompiledEngine` doing double duty — factory and product in the same class, with a static `INSTANCE()` method calling the constructor with null args. The constructor immediately hit `descriptor.getRules()`. NPE. The error pointed at `getRules()`, which looked like a broken descriptor lookup — not a null sentinel from a factory call. Splitting into two classes cleared it.

When the real incremental Rete engine is ready, `UnitDescriptor.setEngine()` is the swap.
