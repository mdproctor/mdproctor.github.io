---
layout: post
title: "When `when` Doesn't"
date: 2026-04-27
type: the-drools-dsl-sandbox
entry_type: note
subtype: diary
projects: [permuplate]
tags: [permuplate, drools, dsl, annotation-processor, java]
excerpt: "We left yesterday with a documented gap: lambda `not()` and `exists()` worked at every arity in vol2 except 2. The DECISIONS.md said "fix requires restructuring." I wanted to see that restructuring ac…"
---

We left yesterday with a documented gap: lambda `not()` and `exists()` worked at every arity in vol2 except 2. The DECISIONS.md said "fix requires restructuring." I wanted to see that restructuring actually done.

## The First Attempt Broke Things It Shouldn't

The fix seemed simple: change `Join2Gate` from `keepTemplate=true, from=3` to `keepTemplate=false, from=2`. That would generate each JoinNGate independently — no template body copying, no erasure conflicts.

It broke `path5()`. Not on `Join2Gate`; on `Join2First`, which extends it. The path5 method wasn't misplaced — From1First has always had its own path5. The problem was that `Join2Gate`'s template-only path5 stub disappeared entirely when the template class was no longer kept.

The reason: `@PermuteReturn(className="void", when="false")` on path5. We'd used `when="false"` to suppress the method from generated classes while keeping it on the kept template. With keepTemplate=false, there's no kept template. For the generated `Join2Gate` at i=2, `applyPermuteReturn` evaluates `when="false"` → removes the method. Path5 gone.

## `when` is Silently Ignored on Non-Object Return Types

That was the diagnosis — but tracing *why* the method disappeared led somewhere more interesting. We discovered that `applyPermuteReturn` only processes methods whose declared return type is `Object` (the sentinel). If a method has a concrete return type — `Join2First<END, CTX, B, Tuple5<...>>` — the method is skipped entirely. The `when` condition is never evaluated. The annotation does nothing.

```java
// This looks like it suppresses path5 from generated classes.
// It doesn't. applyPermuteReturn never sees it.
@PermuteReturn(className = "void", when = "false")
public Join2First<END, CTX, B, Tuple5<...>> path5(...) { ... }
```

The fix was to change `when="false"` to `when="i == 2"`. For i=2: `when="true"` → method kept on the generated class. For i=3..10: `when="false"` → method suppressed. `Join2First` inherits path5 from the generated `Join2Gate` at i=2. ✓

Once that was clear, the rest of the restructuring went smoothly. `Join2Gate` and `Join2First` both changed to `from=2, keepTemplate=false`. Each JoinNGate and JoinNFirst is now generated independently — no body copying, no erasure conflicts.

## The Second Bug Was Hiding in the Reactive Model

With the template restructuring done, `not(Consumer<ScopeGate2>)` appeared on `Join2Gate` at i=2. The test `testLambdaNotScopeTwoOuterFacts` compiled. Then it failed at runtime:

```
Scope predicate invocation failed: wrong number of arguments: 3 expected: 4
```

The predicate was `(ctx, p, city, entry)` — four parameters. We were passing three arguments (ctx + two facts). The person was missing.

We'd wired scopeGuard to wrap the `JoinRightInlet` for 2-source rules. The right inlet only fires with the right fact (city). The left fact (person) is in the JoinNode's beta memory — not accessible at the inlet level. So `outerFacts = [city]` instead of `[person, city]`.

The fix: wrap the `Consumer3` instead of the inlet. The consumer receives both facts before firing:

```java
Consumer3<Context<CTX>, Object, Object> scopedConsumer = (c, leftFact, rightFact) -> {
    if (scopesAllow2(c, negations, existences, leftFact, rightFact))
        consumer.accept(c, leftFact, rightFact);
};
```

Straightforward once the cause was clear. `testLambdaNotScopeTwoOuterFacts` passed on the next run: Alice blocked (name on blocklist), Bob+London and Bob+Paris both fire.

91 vol2 tests, all green.
