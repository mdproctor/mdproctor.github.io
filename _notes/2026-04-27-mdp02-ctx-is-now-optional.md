---
layout: post
title: "ctx Is Now Optional"
date: 2026-04-27
type: the-drools-dsl-sandbox
entry_type: note
subtype: diary
projects: [permuplate]
tags: [permuplate, drools, dsl, annotation-processor, java]
excerpt: "Three things shipped for vol2 today: 3+ source pattern execution, the chain-form `not()`/`exists()`, and ctx-optional across every builder method. The third one took most of the session."
---

Three things shipped for vol2 today: 3+ source pattern execution, the chain-form `not()`/`exists()`, and ctx-optional across every builder method. The third one took most of the session.

## Three-Source Rules Were Straightforward

The `wireHead()` function in `UnitInstance` threw `UnsupportedOperationException` for any rule with 3+ source patterns. We extended it using delta evaluation — when fact F is added to source K, fire only the new combinations where source K=F. All other slots snapshot their current state. This avoids re-firing existing combinations on every change, which matches RETE semantics without RETE infrastructure.

Two TDD tests, both green first run after fixing a pre-existing bug: `filter(Predicate${i+1})` (the all-facts filter in `Join2First`) was a stub that called `return this` without ever calling `storeFilter(predicate)`. The filter just silently did nothing. Spotted only when the 3-source filter test failed.

## Chain-Form not()/exists() Completed

`ChainScope<END, CTX>` gives the chain form its typed scope builder with `join()`, `filter()`, and `end()`. It uses the same `ScopeDescriptor` and `scopeHasMatch` infrastructure built for the lambda form, but sets `globalEval=true` so the scope evaluates against the whole data set rather than per outer tuple. Two tests, both pass.

## ctx Optional Everywhere — Messier Than Expected

The design is clean: add ctx-optional overloads that wrap to ctx-first at store time. The hot path — `JoinLeftInlet`, `JoinRightInlet`, `evaluateAllCombinations` — needs zero changes. The wrapping happens at registration:

```java
public From1First<END, CTX, B> ifn(Consumer1<B> fn) {
    storeHead((Consumer2<Context<CTX>, B>)(ctx, b) -> fn.accept(b));
    return this;
}
```

The messiness came from three places:

**Erasure at arity 2.** At n=2 in `ScopeGate` (and i=2 in `Join2First`), `Predicate2<B,C>` (all-facts no-ctx) and `Predicate2<Context<CTX>,C>` (single-fact ctx-first) erase identically. Java can't distinguish them. We suppressed the single-fact ctx-first overload specifically at n=2 using `@PermuteReturn(when="n != 2")`. The trade-off: at arity 2, users who want single-fact + ctx use the all-facts ctx-last form instead.

**A sed command that was too broad.** When stripping `(ctx, b) ->` from ifn/fn/filter lambdas across the test files, the pattern also matched path callback lambdas like `(ctx, b) -> b.pages()`. Path methods take `Function2<PathContext<...>, B, ?>` not `Context<CTX>` — those `ctx` params should stay. We caught it from the `cannot find symbol: method pages()` errors, not from the sed output. Fixed by restoring the path callbacks manually.

**invokePredicate needed arity detection.** The reflection-based predicate invocation always prepended ctx: `args = [ctx, fact1, fact2, ...]`. A no-ctx `Predicate1<String>` with `test(String)` gets 2 args where 1 is expected. The fix: check `m.getParameterCount()` vs `facts.length + 1` (ctx-first) or `facts.length` (no-ctx) and route accordingly. Zero branching in the hot path — only the registration wrappers and this one reflection detection site.

94 vol2 tests, all green.
