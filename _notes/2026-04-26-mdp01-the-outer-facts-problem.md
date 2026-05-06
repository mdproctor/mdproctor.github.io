---
layout: post
title: "The Outer Facts Problem"
date: 2026-04-26
type: the-drools-dsl-sandbox
entry_type: note
subtype: diary
projects: [permuplate]
tags: [permuplate, drools, dsl, annotation-processor, java]
excerpt: "The question started simply: should `not()` and `exists()` have lambda scope? The answer required a more fundamental one first — what should a scope actually be?"
---

The question started simply: should `not()` and `exists()` have lambda scope? The answer required a more fundamental one first — what should a scope actually be?

The existing chain form (`.not().join().filter().end()`) evaluates globally. It knows nothing about which outer fact combination triggered it. That's a deliberate sandbox simplification. For a canonical DSL, scope predicates need to see the outer facts — the whole point of `not(Person → no Order where order.customer == person.name)` is that the condition references the person.

I wanted `not(scope -> scope.join(CTX::orders).filter((ctx, p, o) -> o.customer().equals(p.name())))`. The outer fact `p` visible inside, typed, with proper predicate arity.

The elegant part: the scope doesn't need to be a new class. After the outer chain has accumulated facts `(A, B)`, calling `not()` should give a `JoinNGate<Void, DS, A, B>` — the same class family the caller has been working with all along. Chain `join()` and `filter()` inside exactly as outside. The scope IS the builder, backed by a fresh `RuleDefinition` with outer-fact placeholders injected before each scope evaluation.

The existing chain form and `END` phantom type stay. `not()` and `not(Consumer)` coexist as overloads; Java resolves them at the call site without ceremony.

## The Template Fought Back

The first build showed "method not already defined in class JoinNGate" for every generated arity. We'd left stale plain `not()` and `exists()` methods in the template alongside the new `@PermuteMethod` block; the InlineGenerator generated both. Removing the stale methods fixed it immediately — but only after reading the generated output carefully enough to distinguish two separate code paths producing the same method name.

`keepTemplate=true` produced a subtler problem. The template class `ScopeGate1<CTX, B, C>` keeps `C` even when the `@PermuteTypeParam` range is empty — "keep verbatim" means verbatim, including type parameters that should have been dropped. Code referencing `ScopeGate1<CTX, B>` fails with "wrong number of type arguments; required 3." The fix: `keepTemplate=false`.

The `@PermuteTypeParam` approach for renaming the join's type parameter on a standalone method caused a JavaParser parse error during generation. We tried several forms before finding the simplest: reference `T` directly in the `@PermuteReturn typeArgs` string. `typeArgs = "'CTX, ' + typeArgList(2, n+1, 'alpha') + ', T'"` — the method's own type parameter dropped in at the end, no annotation machinery needed.

## Vol2 Started Broken

The vol2 templates for `Consumer2`, `Predicate2`, and `RuleExtendsPoint` used `@PermuteConst("${i}")` — an annotation that didn't exist in `permuplate-annotations`. The generated output had carried unresolved annotations silently. We added `@PermuteConst` properly: the annotation, APT processor support, and Maven plugin support. The `ARITY` constants in `Consumer3`..`Consumer10` now read 3, 4, 5 — as they should have all along.

Vol2's lambda scope required synchronous scope evaluation on top of a reactive subscription model. `DataSource<T>` there is an empty interface with no iteration API — a surprise. We added `asList()` as a default method, implemented in `PropagatingDataStore` via `keySet()`. The `ScopeGate` family — `ScopeGate0<CTX>` through `ScopeGate10` — carries outer fact types through inner joins and filters. `not(scope -> scope.join(CTX::blocklist).filter((ctx, p, name) -> p.name().equals(name)))` works end-to-end on vol2's reactive engine.
