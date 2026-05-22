---
layout: post
title: "The Finalization Boundary"
date: 2026-05-21
type: phase-update
entry_type: note
subtype: log
projects: [droolsvol2]
tags: [rete, architecture, lifecycle, changeset]
---

The handover said "build RuleNetworkMap" — a new structure to give the
evaluation engine pre-resolved per-rule topology. Before writing any code, I
asked Claude to walk me through the concept.

It took about two exchanges to see the problem. Vol1 already does this. Each
node in the network has a `Set<Rule>` added to it during build —
`isAssociatedWith(rule)` answers "does this JoinNode belong to that rule"
without any new structure. Claude had invented a concept that already existed.
I redirected: carry forward what vol1 has unless there's a clear reason not to.

That conversation opened into a broader question — what *else* does vol1 do
at build time that vol2 is missing? We ran a proper audit.

## vol1's build lifecycle

The machinery is: `attach()` / `doAttach()` fires per-node when it's new
(shared nodes only get `addAssociation`, no re-attach). `visitLeftTupleNodes`
walks backward from a terminal through every node in its left-input chain,
registering the terminal with each node via `addAssociatedTerminal`.
`setPathEndNodes` runs after each terminal attach to populate the path
structure. Then `EagerPhreakBuilder.addRule()` — the real deferred work —
handles segment prototypes and memory initialisation.

The batch problem in vol1: adding a rule that shares nodes with existing rules
forces updates to live working memory. Not just segment prototypes — actual
in-flight tuples, partial match state in running sessions. Every session gets
patched in place. I never found a better way while working on vol1.

Claude initially claimed vol2 resolves this through the `CompiledEngine` /
`UnitInstance` separation. I disagreed. It doesn't — at least not yet. A
long-lived stateful unit with in-flight state hits the same problem on rule
addition. The architecture is clean enough that a proper solution is
conceivable, but it's deferred.

What vol2 does avoid is the O(N²) part. When 100 rules arrive in one
changeset, finalization runs once after all of them — not incrementally
per-rule with each addition potentially patching the previous rules' segments.

## The boundary that was already there

The reason this works is that the changeset API wasn't just ergonomics. I
never exposed individual `addRule()` publicly deliberately. The changeset IS
the phase boundary — `apply()` is where network build ends and finalization
begins. Without it, there's no natural point to batch, and vol1's incremental
patch loop is the inevitable result.

## What we built

Three pieces.

`BaseNode.associatedTerminals` was declared but never initialized:

```java
private Map<Integer, TerminalNode> associatedTerminals;
```

No `= new HashMap<>()`. The field looked complete — type, name, all methods
present. The NPE was waiting for the first call to `addAssociatedTerminal()`.
Fixed before it had a chance to bite.

`TerminalNode.visitLeftTupleNodes(Consumer<BaseNode>)` walks from
`getLeftInput()` back to `startLeftInput` (the topmost node in the left chain),
calling the consumer on each node. Eight lines, direct vol1 carry-forward.

`RuleBase.finalizeChangeset(List<TerminalNode>)` — called once at the end of
`apply()`, after every rule in the changeset is built. For each terminal:

```java
terminal.visitLeftTupleNodes(node -> node.addAssociatedTerminal(terminal));
```

Four tests confirm: every node in a single-pattern path is associated, every
node in a join path is associated, a shared node gets both terminals from both
rules that use it, the terminal itself is not in its own set. 107 tests total, still green.

The evaluation engine can now traverse using `isAssociatedWith(rule)` and
`hasAssociatedTerminal(terminal)` without any traversal hacks. The
`IncrementalReteEngine` is next.
