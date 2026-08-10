---
layout: post
title: "The Panel That Wanted a Neighbour"
date: 2026-08-10
entry_type: note
subtype: diary
projects: [trellis]
tags: [workbench, dockview, enrichment, backlog]
---

The backlog panel started as a straightforward feature: read soredium's enrichment tables, render them in a table, add some filter dropdowns. Issue #47, clean spec, four implementation tasks.

The interesting moment came during design. I was deciding where the panel should live in the workbench — its own dock-bar icon, or embedded in the existing dashboard. Both options felt wrong for different reasons. Embedding it means you can't see the dashboard overview and the backlog simultaneously. A separate dock-bar panel means you toggle between them, losing context each time.

The real answer was obvious once I named it: these two panels want to sit side by side. The workbench should support split views. And the workbench content area — which currently hard-switches a single panel on each dock-bar click — doesn't support that at all.

We already have the machinery. The workspace view uses Dockview for frame and tab management inside its own panel. The same layout primitives could drive the content area itself. Split frames, dockable panels, the whole model — it's already a dependency, already proven in trellis. The content area just doesn't use it yet.

I filed #49 to capture the architectural change: pluggable layout models for the content area, optional dock bars on all sides (bottom is already optional; left and right should follow). The backlog panel ships as a standalone dock-bar entry for now — it's a self-contained component that will slot into a split layout without changes when #49 lands.

The implementation itself was clean pattern-following. A `WorklogDataSourceProducer` opens soredium's `worklog.db` read-only (with `?mode=ro` on the JDBC URL and a 3-second `busy_timeout` for concurrent access). If the DB doesn't exist — soredium never ran enrichment — the endpoint returns an empty list instead of crashing the sidecar. The query is a single LEFT JOIN across all three enrichment tables, trajectory notes included via correlated subquery rather than N+1.

The frontend follows the memory panel's pattern exactly: `pages-data-table` with `fromRows()`, colour-coded pills for each classification dimension, dropdown filters populated from the dataset's distinct values. A sidebar shows trajectory detail on row click. Cache age computed from the oldest `cached_at` across all items, not the filtered subset — because the cache age describes the dataset, not the view.

The design review caught the things I'd been sloppy about: the spec said "follows CoordinatorDataSourceProducer exactly" but the coordinator writes its DB while the worklog connection must be read-only. Three independent reviewers flagged it. The review also pushed the trajectory query from N+1 to a single JOIN and added interval cleanup in `disconnectedCallback` — things that were right to specify up front rather than discover in production.

What this opens up is the enrichment feedback loop. The `what-next` recommendation in the work skill already reads the same tables. Now there's a visual surface for the data — a place to see which issues are classified, which are stale, which have trajectory notes from recent sessions. The backlog stops being invisible plumbing and becomes something you can look at while deciding what to work on next.
