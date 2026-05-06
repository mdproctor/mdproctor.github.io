---
layout: post
title: "What the Tests Found"
date: 2026-04-27
type: the-drools-dsl-sandbox
entry_type: note
subtype: diary
projects: [permuplate]
tags: [permuplate, drools, dsl, annotation-processor, java]
excerpt: "The session started with test coverage and ended with two things that shouldn't"
---

The session started with test coverage and ended with two things that shouldn't
have worked the way they did.

## The 2-Source Filter That Silently Died

Vol2 shipped ctx-optional last session. The tests confirmed the new overloads
compiled and ran for 1-source and 3-source rules. What nobody had checked was
2-source all-facts filters — `filter((p, n) -> p.name().equals(n))` after a join.

Writing the test revealed the bug. Claude and I traced it to `wireHead()` in
`UnitInstance`: the 2-source path calls `subscribeWithFilter()` for both filter
slots, and that method blindly casts every filter to `Predicate2<Context<CTX>, Object>`.
A single-fact filter is stored as a `Predicate2` and survives the cast. An all-facts
filter is stored as a `Predicate3` — ClassCastException at runtime, no warning at
compile time.

The fix routes by arity. A new helper, `isMultiFactFilter()`, checks the predicate's
method parameter count by reflection. Anything with more than 2 params gets wrapped
into the join consumer at the point where both facts are in scope, rather than applied
per-inlet where only one is visible. The 3-source path already did this correctly
through `evaluateAllCombinations`; the 2-source path just needed the same principle.

```java
if (filter1 != null && isMultiFactFilter(filter1)) {
    final Object postJoinFilter = filter1;
    finalConsumer = (c, left, right) -> {
        if (invokePredicate(postJoinFilter, c, new Object[]{left, right}))
            scopedConsumer.accept(c, left, right);
    };
    inletFilter1 = null;
}
```

The chained case — single-fact filter before the join and all-facts after — worked
correctly after the fix. Two more tests to confirm the edge cases.

## Fixing the Sandbox API — and the Erasure Puzzle It Revealed

The sandbox still had ctx as the first lambda parameter everywhere —
`filter((ctx, p) -> ...)`, `fn((ctx, p, a) -> ...)`. Vol2 had already dropped it.
The sandbox needed the same treatment: ctx removed from the front, available at the
end when genuinely needed.

The obvious approach fails immediately. `Consumer2<DS, A>` (ctx first) and
`Consumer2<A, DS>` (ctx last) both erase to `Consumer2`. Java won't let you overload
them in the same class. The same collision appears for predicates at every arity.

The fix is to step sideways: generate two entirely new interface families with
distinct class names. `NCtxConsumer1<A>`, `NCtxConsumer2<A, B>` — no context,
different class, different erasure. `CtxLastConsumer1<A, DS>`,
`CtxLastConsumer2<A, B, DS>` — ctx at the end, again a different class.

```java
// Both live on the same class without conflict:
public RuleResult<DS> fn(NCtxConsumer1<A> fn) { ... }         // fn(a -> ...)
public RuleResult<DS> fn(CtxLastConsumer1<A, DS> fn) { ... }  // fn((a, ctx) -> ...)
```

Two Permuplate templates generate both families — about 25 lines each, producing
12 interfaces apiece. Zero runtime overhead; the wrappers normalise everything to
ctx-first before it reaches the evaluation engine.

There's one real constraint. For any given arity, you can have two overloads — but
not three. No-ctx and ctx-at-end have different param counts, so they coexist. But
adding ctx-first alongside either one produces a count collision: `Predicate2<DS, B>`
(ctx-first single-fact) and `NCtxPredicate2<A, B>` (no-ctx all-facts) both have
2-param methods, and Java can't resolve which one a 2-param lambda targets. The
moment you keep ctx-first, the no-ctx all-facts overload needs suppression at arity 2.
Remove ctx-first entirely and the problem disappears — all param counts are distinct
at every arity.

The full picture at arity 2 with ctx-first gone:

| Form | Interface | Params |
|---|---|---|
| no-ctx single-fact | `NCtxPredicate1<B>` | 1 |
| ctx-at-end single-fact | `CtxLastPredicate1<B, DS>` | 2 |
| no-ctx all-facts | `NCtxPredicate2<A, B>` | 2 |
| ctx-at-end all-facts | `CtxLastPredicate2<A, B, DS>` | 3 |

`CtxLastPredicate1` and `NCtxPredicate2` share a param count but are different
classes — different erasure, no conflict. All four forms are available at every
arity with no workarounds and no suppressions.

Nine new tests in vol2, five in the sandbox.
