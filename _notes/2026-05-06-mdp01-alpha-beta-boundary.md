---
layout: post
title: "The Alpha-Beta Boundary"
date: 2026-05-06
type: phase-update
entry_type: note
subtype: diary
projects: [droolsvol2]
tags: [rete, architecture, propagation]
---

The naming question for the intermediate class in the `BetaNode` hierarchy had been sitting over from last session. Three options — `ConjunctBetaNode`, `ConvergentBetaNode`, `DualInputNode` (from Grok). I went with `LeftAndRightNode`. It maps directly to vol2's field vocabulary and says exactly what the class is without importing semantic baggage. `NotNode extends LeftAndRightNode` reads correctly: same topology, different evaluation logic.

I brought Claude in to work through the rest of the infrastructure backlog. We built `Vol2NodeTypeEnums` — standalone from vol1, because vol1's bitmask compositions encode vol1's model of what beta means, which differs from vol2's. In vol1, `EvalConditionNode` doesn't carry `BetaMask`. In vol2 it does, because vol2 uses Forgy's correct definition: beta means operating on partial tuples, regardless of input count. We also added `NodeCaster` (switch-on-type dispatch to concrete classes, preventing megamorphic call sites in the evaluation loop) and `TupleFactory` (correct concrete tuple type per downstream node — `NotNode` and `ExistsNode` get blockable variants, everything else gets plain `JoinTuple`).

## Making the UnitInstance flow through

The real work was getting `UnitInstance` to flow through the propagation chain rather than being captured in node fields. The principle is that network nodes never hold runtime state — the network is shared across unit instances and must be frozen and stateless.

We implemented the first attempt: swapped `NodeMemories` for `UnitInstance` in the `JoinLeftInlet` and `JoinRightInlet` constructors. I looked at it again and caught the error. Same violation, different field name. The inlet was still holding a reference to per-session state. The rule isn't "don't hold `NodeMemories`" — it's "don't hold runtime state at all." `UnitInstance` is runtime state.

The right design: a new `UnitProcessor<CTX, T>` interface with `add/update/remove(UnitInstance<CTX>, ObjectHandle<T>)`. The `Router` stores `UnitInstance` objects and passes one to each processor on every event. The inlets have no runtime fields — just the `JoinNode` reference (topology), the consumer lambda (rule logic), and the `immediate` flag (DSL intent). Everything per-unit comes in at call time.

The complication: `Filter1` is used in the alpha chain too. `Filter1Test` confirmed it — subscribed directly to a `PropagatingDataStore`, operating on raw handles with no `UnitInstance` in sight. The split was unavoidable: `Filter1DataProcessor` for the alpha chain, `Filter1UnitProcessor` for the unit chain. Same for `Action1`.

## The boundary that was already there

The split landed cleanly onto Forgy's alpha/beta distinction. `DataProcessor` is the alpha interface — single-fact, DataSource chain, shared across all unit instances, no runtime awareness. `UnitProcessor` is the beta interface — multi-fact, partial-tuple work, `UnitInstance` passed at call time.

The `Router` is the exact boundary. Alpha `DataProcessor` calls arrive from the DataSource network. Beta `UnitProcessor` calls depart to the join inlets and rule actions. I hadn't planned this alignment — it emerged from the constraints of the design.

One more clarity before closing: `*Node` for physical network representation, `*Processor` for runtime evaluation. The naming makes the layer separation legible. `JoinNode` is topology. A future `JoinProcessor` implements `UnitProcessor` and drives join evaluation for one particular algorithm. Two layers, clearly named, ready to separate properly.

That separation — frozen network on one side, swappable evaluation engines on the other — is the next phase.
