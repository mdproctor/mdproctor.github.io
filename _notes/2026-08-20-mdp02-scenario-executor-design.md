---
layout: post
title: "A universal scenario executor — from MCP wrapper to GraphQL dispatch"
date: 2026-08-20
entry_type: note
subtype: diary
projects: [casehub-pages]
tags: [scenario-executor, graphql, distributed, aria, testing]
---

The scenario engine started as a browser-only ARIA runner — parse YAML, click buttons, fill forms, assert DOM state. Useful for demos. Not useful for the backend operations that actually drive a helpdesk system: injecting chat messages, checking case state, verifying that the classification engine did its job. The original plan was to add an MCP client so the scenario executor could call `casehub_action` for backend steps. That turned out to be wrong.

MCP is an LLM protocol. `casehub_model` gives an LLM catalog discovery — what domains exist, what operations they support. `casehub_action` wraps calls in string-typed JSON because that's what tool-calling models need. A mechanical executor reading a YAML script needs none of this. It knows exactly what to call. Every `@McpDomain` operation is already exposed via GraphQL — typed mutations and queries generated at compile time by `GraphQLResolverProcessor`. Calling GraphQL directly gives typed parameters, schema validation, and standard HTTP POST. MCP adds JSON-RPC framing and Streamable HTTP transport for zero benefit.

The MCP is still there for the part that actually needs it: the LLM explores operations via `casehub_model`, generates a scenario YAML script, and hands it to the executor. Discovery is an authoring concern. Execution is mechanical.

The architecture that emerged has three tiers. A pure ARIA scenario runs entirely in the browser — no server required. A pure GraphQL scenario runs entirely server-side — no browser required. A hybrid mixes both, with the server as the central orchestrator sending ARIA fragments to the browser via the push wire protocol. The browser engine always owns simulation execution; the server delegates to it, never bypasses it. This matters because CaseHub services can already be distributed. The same push wire pattern that sends ARIA commands to the browser also sends scenario fragments to a remote server's executor. One delegation model, three targets: browser, local server, remote server.

The step model is a sealed interface — `AriaStep`, `GraphQLStep`, `SimulatedStep`. ARIA shorthand in the YAML (`click: { role: button, name: Submit }`) expands to `AriaStep` at parse time. GraphQL steps declare their domain and operation explicitly. Variable interpolation is step-scoped: `${inject-chat.caseId}` references a field from a named step's result. No unqualified references — most-recent-wins resolution is order-dependent and fragile for CI scenarios.

The await mechanism polls a GraphQL query until a match condition is met, with push wire event subscription as the primary path when domains publish state-change events. Timer polling is the fallback. The push wire already carries domain events across the network, so the same event subscription works for local and distributed deployments without protocol changes.

Five Java tasks landed: the sealed step model with parser refactoring, push wire `CommandResult` enrichment with an optional result payload, the `scenario-runtime` module with `VariableContext` for step-scoped interpolation, `GraphQLDispatcher` for typed query construction and HTTP dispatch, and `ScenarioExecutor` with `AwaitEngine` for the central orchestration loop. The TypeScript side now mirrors the Java model — the action-keyed union (`{ click: AriaTarget }`) became a delivery-keyed discriminated union (`{ delivery: 'aria', action: 'click', target }`) so both sides speak the same three-variant vocabulary. The parser expands ARIA shorthand at parse time; the browser runner dispatches on `delivery` and ignores non-aria steps. The scenario topic migrated from `scenario/*` to `scenario:exec` with a `ready` action for the page-load wait protocol. `ScenarioConfig` maps domains to per-service GraphQL and push wire endpoints — distributed deployment configuration without code changes.

The larger realisation is what this becomes. Parameterised include templates turn common setup patterns into reusable seed files. Server-side assertions turn scenario execution into end-to-end testing. Together with the distributed delegation model, it's a universal framework for both frontend and backend scenario automation and testing — and it doesn't need MCP anywhere in its execution path.
