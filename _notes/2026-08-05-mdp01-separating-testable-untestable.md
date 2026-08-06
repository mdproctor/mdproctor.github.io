---
layout: post
title: "Separating the testable from the untestable"
date: 2026-08-05
type: phase-update
entry_type: note
subtype: diary
projects: [trellis]
tags: [workspace-view, dockview, tdd]
series: issue-33-workspace-view-spec
---

Trellis's workspace view lets you position floating terminal frames across
a desktop — think tiling window manager inside an Electron app, backed by
Dockview. The spec was approved weeks ago. This session tackled the first
batch: z-order management, keyboard navigation, and organiser presets.

The interesting problem wasn't the features themselves — z-order counters,
spatial navigation, layout presets are all straightforward algorithms. The
problem was testing them. Dockview owns its own DOM. It uses ResizeObserver
internally, which happy-dom doesn't support, so the full library can't
initialize in vitest. We had a mock that covered the basics — `addPanel`,
`removeGroup`, `dispose` — but every new feature that touched a Dockview
API property the mock didn't have would crash silently in tests while
working fine at runtime.

I decided to draw a hard line: anything that's pure logic gets its own
module and its own test file. Anything that touches Dockview's DOM stays
in the component and gets tested through public method calls on internal
state.

The z-order system split cleanly. The spec calls for two tiers — normal
frames in \[1, 9999\], pinned frames in \[10001, 20000\] — with compaction
when either counter exceeds 5000 to prevent unbounded growth. That's three
pure functions: `bringToFront`, `compactFrames`, `normalizeForSave`. They
went into `workspace-zorder.ts` with fourteen tests covering tier
separation, compaction triggers, and save normalization. The component
imports them and applies the z-index to Dockview's container element —
which, incidentally, is `.dv-resize-container`, a DOM structure Dockview
doesn't document anywhere.

Spatial navigation split the same way. The algorithm — filter candidates
by directional half-plane, pick nearest by Euclidean distance, break ties
by primary axis alignment — is a pure function of frame rectangles and a
direction. Nine tests. The component just reads positions from its
internal map and calls it.

The organiser presets were already extracted from a previous session —
five pure functions (`sideBySide`, `stacked`, `grid`, `mainSidebar`,
`focus`) that take frames and a canvas size and return repositioned frames.
I added twelve tests and wired a picker UI that opens on `Cmd+Shift+L`
with `1`–`5` number keys for quick selection.

The frame chrome was the one piece that couldn't be extracted. Injecting
pin, detach, and close buttons into Dockview's floating titlebar is
inherently DOM work. The pattern: find `.dv-floating-titlebar` via
`group.element.closest('.dv-resize-container')`, prepend or append
buttons, stop pointer event propagation so the titlebar drag handler
doesn't swallow clicks. A click anywhere on the container calls
`bringToFront`. This is the kind of code where the test verifies CSS
classes exist in the shadow root and internal state changes on method
calls — not pixel-perfect DOM assertions.

One gotcha bit us: Claude edited the wrong repository. The IntelliJ MCP's
`project_path` parameter determines which opened project receives the
edit, and when you have two clones of the same repo (slot 2 vs main),
pointing at the wrong one silently succeeds. The replacement count comes
back as `1`, no error, no warning. I only caught it by grepping the slot
file and finding the original content unchanged. The fix is mechanical —
open the slot's sidecar as its own IntelliJ workspace — but the silent
success is a trap.

The extraction pattern probably has further to run. Groups, layout
persistence, and the tab hover flyout are all on deck for Batch 2, and
each has logic that doesn't depend on Dockview's DOM. The question is
whether the component itself starts feeling like pure wiring — imports,
maps, event listeners — with no logic of its own. That might be exactly
right for a component whose job is to bridge a third-party library to a
Lit element. Or it might mean the abstraction boundary is in the wrong
place. Worth watching as the remaining batches land.
