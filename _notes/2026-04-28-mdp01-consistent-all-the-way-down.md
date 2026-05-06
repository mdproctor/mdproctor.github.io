---
layout: post
title: "Consistent All the Way Down"
date: 2026-04-28
type: the-drools-dsl-sandbox
entry_type: note
subtype: diary
projects: [permuplate]
tags: [permuplate, drools, dsl, annotation-processor, java]
excerpt: "The filter and fn overloads dropped ctx from the front. The path traversal API hadn't. Every call still looked like `(pathCtx, lib) -> lib.rooms()` — the unused first argument sitting there as a remin…"
---

The filter and fn overloads dropped ctx from the front. The path traversal API hadn't. Every call still looked like `(pathCtx, lib) -> lib.rooms()` — the unused first argument sitting there as a reminder that the work wasn't finished.

## Three Forms, Not Six

The first question was how many overloads `path()` needs. Predicates already have two forms: no-ctx and ctx-at-end. Traversal functions are the same: navigate from the current element only, or navigate with access to the accumulated path context.

That's a 2×2 grid, but one cell is redundant. If the traversal doesn't need ctx, the predicate can either way. But if the traversal *does* use ctx, you've already declared you're in path-context territory — the predicate that follows should be consistent. I made rule 3 explicit: **traversal with ctx implies predicate with ctx**. No mixed overloads.

Four overloads total, not eight. And the rule is enforced structurally — the missing combinations simply don't exist.

```java
// no-ctx traversal, no predicate — method references work
.path(Library::rooms)

// no-ctx traversal, element-only predicate
.path(lib -> lib.rooms(), book -> book.published())

// ctx-at-end traversal, no predicate
.path((lib, pathCtx) -> lib.rooms())

// ctx-at-end both — rule 3: if traversal has ctx, predicate must too
.path((shelf, pathCtx) -> shelf.books(),
      (book, pathCtx) -> pathCtx.getTuple().getB().name().equals("Physics"))
```

## The Erasure Problem, Again

Vol2 has `Function1<A, R>` already. When we applied the same redesign there, I tried using `Predicate2<B, PathContext<T>>` for the ctx-at-end predicate. The compiler disagreed: `Predicate2<B, PathContext<T>>` and `Predicate2<PathContext<T>, B>` both erase to `Predicate2`. Same class, different type args — same erasure.

The fix is the same one we used for filter and fn: a distinct interface class. `CtxLastPredicate1<A, DS>` goes alongside `Predicate1<A>` in vol2's function package. Different class name, different erasure, no conflict.

## The `keepTemplate=true` Trap

Vol2's `Path3` uses `keepTemplate=true` — the template class itself is preserved in the generated output alongside `Path4`, `Path5`, `Path6`. The sandbox uses `keepTemplate=false`, so the template class is never emitted.

We added `@PermuteBody` to the new overloads and used `return null;` as the placeholder body — standard practice in the sandbox where the template class is discarded. In vol2, `Path3.path(Function1, Predicate1)` returned null at runtime. `@PermuteBody` had replaced the generated classes but left the template class untouched.

The fix is mechanical: write actual delegation bodies in the template class alongside `@PermuteBody`. The template uses the real body; the generated classes use the annotation. One gotcha with no compile-time warning.

## Array and Single-Object Traversal

`Function1<A, B[]>` and `Function1<A, Iterable<B>>` both erase to `Function1`. They need different method names: `pathArray()` and `pathSingle()`.

Both wrap at the DSL boundary before calling the private core — no runtime changes. Array: `Arrays.asList(fn.apply(a))`. Single: a null-safe block lambda that produces an empty list when the traversal returns null, pruning the path branch cleanly.

The wrapping approach means `Library::roomsArray` and `lib -> lib.headRoom()` both work as method references, and the `ListPathNode` traversal loop doesn't need to know the difference.
