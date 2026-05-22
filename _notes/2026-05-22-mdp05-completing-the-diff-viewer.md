---
layout: post
title: "The last piece of the diff viewer was the hardest"
date: 2026-05-22
type: phase-update
entry_type: note
subtype: diary
projects: [md-compare]
tags: [diff, dom, javascript, electron]
---

Swap panels, next/prev navigation, diff summary — those went in cleanly over a couple of sessions. The word-level diff took more thought.

The question was where to do the diff. One option was to diff the raw markdown source and feed highlights into the marked.js renderer. Another was to diff the rendered HTML text and patch the DOM. I wanted inline formatting preserved — if a word inside a `<strong>` element changes, the bold should survive the highlight. That rules out the naive approach of replacing `innerHTML` with flat highlighted text.

We went with DOM-walking: diff `el.textContent` to get changed character ranges, then walk the element's text nodes with `TreeWalker`, split them at range boundaries, and replace the changed portions with `<mark>` elements. Element nodes (`<strong>`, `<em>`, `<code>`, `<a>`) are never touched — only text nodes get split. Inline formatting survives.

The tricky part is ordering. When you replace a text node with a `DocumentFragment`, the surrounding DOM shifts — but your offset table was built before that mutation. Process forward and by the time you reach node three, the positions you recorded for it are wrong. Process in reverse and the mutations only affect nodes you've already handled.

The word diff itself reuses the LCS algorithm already in the codebase for the line diff, adapted to word tokens. Not the most glamorous code, but the duplication is deliberate: the algorithm is the same, the inputs are different.

```js
function applyWordHighlights(el, changedRanges, markClass) {
  const walker = document.createTreeWalker(el, 4); // NodeFilter.SHOW_TEXT
  const nodes = [];
  let node, off = 0;
  while ((node = walker.nextNode())) {
    if (node.parentNode.tagName === 'CODE') { off += node.length; continue; }
    nodes.push({ node, start: off, end: off + node.length });
    off += node.length;
  }
  for (let i = nodes.length - 1; i >= 0; i--) {
    // split and wrap in reverse order
  }
}
```

The `CODE` guard deserves a note: inline code spans inside paragraphs are skipped for word highlighting, but their character length is still counted so the surrounding ranges stay correctly aligned. Took a moment to realise why that matters.

The code review caught something I'd missed. `updateDiffMap` is called by a `ResizeObserver` watching the panel divider — not just when files load. The file-load path resets `innerHTML` first, clearing all marks before re-annotating. The resize path does not. Every divider drag was adding another nesting layer of `<mark>` elements on top of the existing ones, inflating the highlighted text on each resize.

Fix was one line at the top of `annotateWordDiffs`:

```js
document.querySelectorAll('mark.diff-word-a, mark.diff-word-b').forEach(m => {
  m.replaceWith(document.createTextNode(m.textContent));
});
```

Unwrap existing marks before re-marking. The kind of thing invisible during development, obvious the first time someone resizes a panel.

The diff viewer is now complete. Swap, navigate, count, highlight words. What I want to look at next is the scroll sync — still pure percentage-based, drifts badly on documents with different densities. Heading anchors would fix that.
