---
order: 6
title: "When the Machine Codes: Parallel Design and Spec-Led Development at Scale — An Empirical Study"
author: Mark Proctor
date: 2026-04-26 18:00:00 +0000
series: "When the Machine Codes"
series_part: 5
tags:
  - AI
  - LLM
  - Java
  - Python
  - Software Engineering
  - Static Typing
excerpt: "An empirical examination across five integrated casehub systems built Java-first from inception — API evolution, integration outcomes, and whether the model scales."
---

# When the Machine Codes: Parallel Design and Spec-Led Development at Scale — An Empirical Study

**Part 5 of 6 — When the Machine Codes series**  
*Parts 1 through 4 made structural arguments for static typing in LLM-first development. Part 3 documented a single migration — Python to Java/Quarkus — where the compiler caught errors that would have been silent. This article tests the argument at scale: not one project, but a family of thirty-five integrated systems developed concurrently by LLM sessions navigating evolving APIs without shared memory. The question is whether the type system carried the weight the series claims it can.*

---

## 1. The Systems Under Study

CaseHub is a case management platform developed LLM-first from inception. It is not a single repository. It is a family of thirty-five interdependent systems spanning a shared engine, domain verticals, UI components, and supporting infrastructure.

| System | Domain | Commits |
|--------|--------|---------|
| engine | Core case management runtime, SPIs, blackboard orchestration | 841 |
| quarkmind | StarCraft II AI — real-time strategy with CBR, HTN planning | 694 |
| parent | Multi-repo build infrastructure, subtree sync, dependency management | 693 |
| work | Work item tracking, scheduling, notifications | 643 |
| qhorus | Messaging platform — stores, persistence, watchdog | 592 |
| claudony | Conversational AI — dialogue management, persona layers | 580 |
| pages | Data visualisation dashboards — charting, theming, gallery | 443 |
| platform | Shared platform services — expression engine, tenancy, RBAC | 377 |
| ledger | Financial ledger — double-entry accounting, reconciliation | 363 |
| clinical | Clinical case management — pathways, assessments | 304 |
| drafthouse | Content management and publishing | 270 |
| devtown | Development environment tooling | 256 |
| neocortex | Neural architecture and ML integration | 242 |
| eidos | Identity and agent modelling | 225 |
| *21 others* | *AML, blocks, connectors, IoT, life, openclaw, ops, etc.* | *2,695* |
| **Total** | | **8,598** |

All Java/Quarkus. All developed by LLM sessions working from specifications, resuming from cold reads of the codebase, with no shared conversation history between sessions. The development produced 1,334 diary entries documenting what happened — what worked, what broke, and what the type system caught that nothing else would have.

---

## 2. The Refactoring Density

The series argues that static typing matters most during change — not during initial generation. If a codebase never evolved, type safety would be a quality luxury. Codebases evolve. This one evolved constantly.

Of 8,598 commits across the project family, **1,171 are refactoring commits** — renames, extractions, module restructurings, API migrations, sealed hierarchy changes. That is **13.6 percent** of all work. Not concentrated in an early exploratory phase — distributed across the project's lifetime, because spec-led development with LLM sessions produces continuous structural refinement as understanding deepens.

The top refactoring-heavy systems:

| System | Refactoring commits | Total commits | Percentage |
|--------|-------------------|---------------|------------|
| engine | 124 | 841 | 14.7% |
| quarkmind | 108 | 694 | 15.6% |
| work | 108 | 643 | 16.8% |
| qhorus | 84 | 592 | 14.2% |
| claudony | 79 | 580 | 13.6% |
| ledger | 65 | 363 | 17.9% |
| parent | 66 | 693 | 9.5% |

### The obvious counter-arguments

Two objections arise immediately. First: *a dynamically typed codebase would be smaller — fewer type declarations, fewer generic signatures, fewer module boundaries enforced by the build — and smaller codebases require less refactoring.* Second: *refactoring at this volume suggests inadequate up-front design; a more disciplined specification process would reduce the need for structural rework.* Both deserve honest answers.

The first objection conflates verbosity with architectural structure. Part 2 of this series addressed the verbosity argument directly: modern Java — records, sealed interfaces, CDI annotations, JAX-RS endpoint declarations — eliminates the boilerplate that once justified the "verbose" label. A record type is a single line that declares a type, its fields, their types, and generates equals/hashCode/toString/accessors. A JAX-RS annotation on an endpoint method simultaneously declares the HTTP contract, generates the OpenAPI spec, and provides the type-checked parameter bindings. These are not lines of overhead — they are the specification expressed as code. But even setting the verbosity question aside: a Python codebase implementing the same thirty-five integrated systems would not have fewer modules, fewer API boundaries, fewer integration contracts, or fewer design decisions that need revisiting as understanding deepens. The refactorings documented here are not moving type annotations around. They are extracting shared modules, separating persistence from API contracts, removing dead infrastructure, consolidating duplicated configuration, and restructuring domain hierarchies. These are architectural operations that any language requires at this scale.

The second objection assumes that the need for refactoring indicates a design failure. The development record shows the opposite. The milestone consolidation (engine #84) is a clear example: the original epic was written when Stage was the containment model. A year later, Compound replaced Stage. The epic's assumptions about structural milestone containment were invalidated by architectural evolution elsewhere in the platform. The refactoring wasn't correcting a mistake — it was adapting the design to a change that could not have been anticipated when the original code was written. The diary entry records the session asking whether the platform needed structural containment at all, discovering that the expression evaluator already provided the integration point, and removing the back-pointer rather than replacing it. That is design deepening, not design failure.

Similarly, the Worker primitives extraction (engine #543) moved nine type files from engine-api to a new casehub-worker-api module — because other systems needed to implement workers without depending on the full engine. The original placement was correct for a single-system project. It became incorrect when the system grew into a family. No amount of up-front design eliminates the need to restructure module boundaries as the number of consumers changes.

### What the refactorings delivered

The numbers above show scale. What they don't show is value — whether these refactorings were architectural improvements or busy work that moves code around without purpose. The commit history answers that question directly.

**Engine #543 — Worker primitives extraction** (121 files across 15 modules). Nine types — `Worker`, `WorkerFunction`, `WorkerResult`, `Capability`, `ExecutionPolicy`, `RetryPolicy`, `BackoffStrategy`, `PlannedAction`, `WorkerOutcome` — were defined in engine-api. Every system that needed to implement a worker had to depend on the full engine API. The refactoring extracted these to casehub-worker-api as a foundation module, letting `ledger`, `work`, `qhorus`, and others implement workers against a minimal contract. The design spec went through three review rounds before implementation, each surfacing production callers that the naive extraction would have broken: `AgentDescriptor` had four active callers that needed redesigning, `FlowWorkerFunction` had an SDK dependency that constrained where it could live, `ActionRiskClassifier` needed a new `ClassificationContext` record to replace its implicit parameter passing. A Python project extracting the same shared module boundary would need the same refactoring. The question is what catches the mistakes during extraction.

**Qhorus #314 — Store SPI migration** (337 files, 20 progressive commits). Store interfaces and their domain types lived in the runtime module, tangled with JPA persistence. Any consumer that needed a `DataStore` or `MessageStore` had to depend on runtime — pulling in persistence infrastructure it didn't need. The refactoring moved SPI interfaces to api/ and introduced immutable domain records (`Channel`, `Message`, `Commitment`, `Instance`, `SharedData`, `Watchdog`) as the API contract, with JPA entities renamed to `*Entity` and converting at the persistence boundary via `fromDomain()`/`toDomain()`. The 20-commit trail — each titled "fix [next module]" — shows the LLM session working through the project module by module, guided by the next set of compiler errors: persistence-memory stores, then contract test bases, then standalone tests, then query tests, then reactive stores, then watchdog, then the testing module, then connector-backend, then examples. Each commit fixed one layer and revealed the next. In Python, there would be no compiler errors to guide the walk. The developer would need to discover each broken module by running its tests — assuming all paths are exercised — or by manual inspection.

**Engine #84 — Milestone consolidation** (multiple commits). Milestone lifecycle state was tracked in three places: EventLog (queried on every `CONTEXT_CHANGED` for every milestone — O(milestones × events)), `CasePlanModel` (a ConcurrentHashMap updated by a handler), and CaseContext (written by lifecycle handlers). IntelliJ's `findReferences` on `getMilestoneStatus()` scoped to production code returned zero hits. The CasePlanModel tracking — six interface methods, the handler class, the ConcurrentHashMap — was dead infrastructure. Written to, never read. The refactoring removed it and consolidated reads to CaseContext, reducing per-context-change cost from O(milestones × events) to O(1). But the design review caught a subtlety: `MilestoneSLATimeoutJob` is a Quartz job that fires after JVM restarts, when CaseContext isn't populated. It needs EventLog. A clean-looking consolidation that unified on CaseContext would have silently broken SLA violation detection after restarts — with no error, just null reads defaulting to PENDING. The dead code and the live edge case were both invisible without type-aware tooling.

**Naming alignment** (multiple repos). A systematic scan of nine repos revealed consistent naming drift — `dev.claudony` groupId instead of `io.casehub.claudony`, folder names not matching artifactIds, inconsistent prefixes. The claudony package rename ran through IntelliJ's Move Package refactoring and silently corrupted four test files: `@Inject SessionRegistry registry;` on one line split into two lines, producing `@InjectCaseEventBroadcaster` — a syntactically plausible but semantically wrong fake annotation. The compiler refused it. Two downstream repos — `casehub-work-notifications` and `casehub-devtown-app` — had the old artifact name hardcoded in their poms, missed until the full-stack build failed. A Python project renaming a package across nine repos would need the same operation. It would not have the compiler catching the corruption.

---

## 3. Cross-Repo API Propagation

The hardest test of the type safety argument is not within a single project. It is across project boundaries — where a change in `engine` must propagate through `ledger`, `work`, `clinical`, `qhorus`, and every other system that depends on the changed API.

The `casehub-ledger` rename (groupId `io.casehub`, package `io.casehub.ledger`) touched 202 files within ledger itself. Then it propagated: 495 files in `work`, 262 files in `qhorus`, and further changes across every consuming system. The package rename changed import statements, Maven coordinates, and CDI injection points simultaneously. In a statically typed language, the build fails until every reference is updated. In Python, import errors surface at runtime — and only on the code paths that happen to be exercised.

The `CaseLedgerEntryRepository` refactoring (documented in the diary as "The Inheritance Chain Nobody Missed") illustrates the subtlety of cross-repo coupling. The class extended `JpaLedgerEntryRepository`, which implements `LedgerEntryRepository`. The extension was `@DefaultBean @ApplicationScoped` — discoverable by CDI and active by default. Every module on the test classpath that needed a `LedgerEntryRepository` got one for free through inheritance, whether or not it knew where the bean came from. A composition refactoring removed the `extends` — for perfectly sound reasons — and broke eight injection points in `casehub-engine-flow`, a module that wasn't touched in the change. The upstream library had marked its implementation `@Alternative` without `@Priority` — never activated unless explicitly selected. The inheritance chain had been silently satisfying a dependency that no import statement, no dependency declaration, and no static analysis would have revealed. The build caught it. In Python, this is a runtime `ImportError` or `AttributeError` on a path that tests may never exercise — dependency injection coupling through inheritance has no compile-time analogue in a dynamically typed language.

The Worker primitives extraction (engine #543, described in Section 2) is the strongest cross-repo example because the refactoring need is language-independent. Nine types needed to move from engine-api to a shared worker-api module so that downstream systems could implement workers without depending on the full engine. Any language — Python included — needs this kind of module extraction when a project grows into a family of integrated systems. The difference is what happens during the extraction. The commit records approximately 130 files updated across 15 modules, with all tests passing. The design spec's three review rounds identified production callers that the naive extraction would have broken — callers that the compiler enumerates and the build verifies. In Python, the extraction is the same architectural decision. The verification that every consumer has been updated is a hope rather than a proof.

---

## 4. The Type System as Session Bridge

Parts 1 and 2 of this series argued that the type system serves as a persistence mechanism across LLM sessions — that when a session begins cold, the types carry architectural intent that conversation history cannot. The development of these thirty-five systems is an extended test of that claim.

Every session began from a cold read. No session had access to the conversation history of any previous session. The specifications, the CLAUDE.md files, and the types were the only context available. The diary entries document what happened when the type system guided a session correctly — and what happened when it didn't.

The "Type System as Architecture Document" entry (2026-07-10) records a session where the developer wanted to add LLM-backed goal decomposition. The type system stopped the naive approach: `PrimitiveTask` carried a `Predicate<T>` precondition and a `Consumer<T>` effect — Java lambdas that an LLM cannot produce. Cramming LLM output into `PrimitiveTask` with always-true predicates would have compiled and lied about what the task represented. The sealed hierarchy forced a design decision: introduce `PlannedTask` as a peer under a shared `LeafTask` base, with `description()` and `agent()` as the shared contract. The type system didn't just catch a bug — it prevented a design that would have been structurally unsound.

In Python, the naive approach would have worked. A dictionary with a `precondition` key set to `lambda: True` raises no errors. The design flaw would have been invisible until someone traced a runtime failure to a task whose precondition was meaningless.

---

## 5. When the IDE Dropped to Bash

<!-- TODO: This section is grounded in documented incidents from the diary.
     The controlled experiment (Section 6) would add measured timing and
     completion data. The narrative here stands without it. -->

The development workflow depended on IntelliJ MCP for refactoring — semantic rename, find references, move class, extract interface. These operations understand the type system: a rename updates every reference, every import, every Javadoc mention, every test assertion that names the class. The operation takes seconds regardless of how many files are affected.

When the LLM session dropped out of IntelliJ and fell back to text-based tools — grep, sed, regex replacement — the results were consistently worse. Not marginally worse. Qualitatively different. The development diary documents specific incidents across the project's history, and the failure modes are instructive.

### Regex cannot parse structure

The tenancy threading refactoring (engine, 2026-05-31) added a `tenancyId` parameter to every SPI method. Forty-plus test files across six modules needed their call sites updated. A Python regex script handled the bulk of the work, but hit a structural edge case: the pattern `[^)]+` stops at the first closing parenthesis regardless of nesting depth. `findByUuid(instance.getUuid())` became `findByUuid(instance.getUuid(, tenancyId))` — a nested call split at the wrong boundary. The diary records that Claude caught some of these during review, and the lasting fix was replacing the regex with explicit `str.replace()` for each known call pattern. The regex approach was not merely slower than IDE refactoring — it introduced corruption that required a second pass to detect and a third approach to fix.

### String replacement misses what it cannot see

The neocortex rename (2026-07-01) changed every package reference across 426 files — `io.casehub.inference` to `io.casehub.neocortex.inference`. The string replacement missed `import static` declarations entirely. `import static io.casehub.inference.tasks.NliLabel.ENTAILMENT` has `static` between `import` and the package path, so the replacement pattern — written to match `import io.casehub.inference` — did not fire. Eleven `DependencyConstraintTest` files used old package names as string literals in ArchUnit rules — invisible to any tool that only scans import statements. Both categories were caught on the first build attempt. In a dynamically typed language, the `import static` equivalent would have been a runtime `ImportError` on the specific code path that exercises it.

### Bulk scripts blocked for good reason

The ContextBridge protocol implementation (engine, 2026-07-10) needed `WorkerFunction.Sync` constructors updated across 60 files in three repos — adding a type class parameter to each constructor call. A bulk script approach was blocked by the project's IntelliJ-first hook. The diary records this as correct: "the Edit tool's exact matching is safer than regex for this kind of substitution." The session worked through it file by file with IDE tooling, dispatching subagents for the larger batches. Two files used `java.util.Map.of()` with fully-qualified imports and needed `java.util.Map.class` rather than `Map.class` — a distinction that a regex pattern matching `Map.class` would have silently missed. The build caught both.

### Even IDE tooling has failure modes — but the compiler catches them

The evidence is not that IDE refactoring is infallible. The naming alignment session (2026-05-12) ran IntelliJ's Move Package refactoring to change `dev.claudony` to `io.casehub.claudony`. The operation reported success and silently corrupted four test files: `@Inject SessionRegistry registry;` on a single line split into two lines during the move, and the following field's `@Inject` merged with its class name, producing `@InjectCaseEventBroadcaster` — a syntactically plausible but semantically wrong fake annotation. The compiler refused it. The corruption was found by grepping for `@Inject[A-Z]` — no space — and fixed manually.

A separate incident (engine, 2026-07-13) exposed a subtler failure mode: IntelliJ's `ide_build_project` compiles everything the IDE has open, not just the current project's Maven reactor. The LLM session saw `TrustRoutingPolicy` errors, fixed them via IntelliJ's text replacement API, then found none of the changes appeared in `git diff`. The fixed files were in casehub-blocks — a sibling project open in the same IDE window. The fixes went to the right files in the wrong repo.

### What the pattern shows

The failure modes differ in kind. Text-based tools fail silently — the regex parses, the replacement runs, and the corruption is invisible until something downstream breaks. IDE refactoring can also fail, but the type system provides a verification layer: the compiler catches `@InjectCaseEventBroadcaster`, the build catches the missing `import static`, `git diff` catches the wrong-repo edit. The safety net is not the tool — it is the type system underneath the tool. Without compile-time verification, there is no reliable mechanism to distinguish a correct refactoring from a plausible-looking one that has introduced subtle inconsistencies across a 400-file change.

---

## 6. What the Evidence Shows

The quantitative picture is already clear. A project family of this scale — 8,598 commits, 35 interconnected systems, 13.6 percent of all work being structural refactoring — could not have been developed in the way it was developed without compile-time type enforcement. The claim is not that it would have been slower. The claim is that specific categories of work would not have completed at all.

Extracting nine Worker types to a shared module across 121 files and 15 modules is a guided walk when the compiler enumerates every consumer that needs rewiring. Migrating a Store SPI across 337 files in 20 progressive commits — each guided by the next set of compiler errors — is a structured traversal of a dependency graph. Without compile errors, both are search problems with no termination condition: you fix what you find and hope you've found everything.

The development diary provides the qualitative evidence that the quantitative data cannot. Five documented incidents — regex corruption of nested parentheses, string replacement blind to `import static` syntax, bulk scripts blocked because exact matching was safer, IDE refactoring corruption caught by the compiler, and cross-repo edits applied to the wrong project — show the same pattern from different angles. Text-based tools fail silently. The type system fails loudly. In a codebase that refactors constantly, the difference between silent corruption and immediate, precise feedback is the difference between a refactoring that completes and one that has to be abandoned.

The diary entries document 1,334 sessions of development. Across those sessions, the pattern is consistent: the type system caught errors at boundaries the developer hadn't considered, prevented designs that would have been structurally unsound, and provided the continuity mechanism that let each cold-start session pick up where the last one left off. The specifications provided intent. The types provided verification. Neither alone would have been sufficient.

---

## References

- CaseHub project family — GitHub commit history across 35 repositories (8,598 commits, 1,171 refactoring commits as of August 2026)
- Development diary — 1,334 entries documenting LLM-first development sessions (published at mdproctor.github.io)
- *The Debugging Decay Index* — arxiv.org/html/2506.18403v2
- Mündler et al. (PLDI 2025) — 94% of LLM-generated Java compilation errors are type-related
- Parts 1–4 of this series
