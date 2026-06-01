---
layout: post
title: "The detection that never fired"
date: 2026-06-01
type: phase-update
entry_type: note
subtype: diary
projects: [cc-praxis]
tags: [claude-code, skills, debugging]
---

I opened the session convinced CLAUDE.md had a re-bloat problem — 15KB, and I was sure it had been smaller after the extraction work done a week earlier. I brought Claude in to check. Together we pulled up the git history and tracked the file size across every commit.

It hadn't grown back. The file was 15,231 bytes the day of the extraction commit, and 15,254 bytes now — a Name field added in a follow-up. Twenty-three bytes of drift over a week. The 51KB → 15KB reduction from May 25 was fully intact.

So the question changed: not "why did it grow back" but "will it stay down?"

Claude traced through the `update-claude-md` skill to find the answer. Step 1a — the step that detects whether a project uses a modular CLAUDE.md structure — calls `python scripts/document_discovery.py CLAUDE.md`. That script doesn't exist. It was never created. The invocation fails silently, the skill falls through to single-file mode, and all the modular routing logic is bypassed. New gotchas would go into CLAUDE.md directly rather than routing to `docs/GOTCHAS.md`. Flyway notes, same. The extraction was holding only because it had been done manually, outside the skill entirely.

The fix: replace the Python dependency with three bash file-presence checks, and add an explicit routing table in a new Step 4e:

```bash
[ -f "docs/GOTCHAS.md" ] && echo "gotchas: yes" || echo "gotchas: no"
[ -f "docs/FLYWAY.md" ]  && echo "flyway: yes"  || echo "flyway: no"
[ -f "scripts/README.md" ] && echo "scripts-readme: yes" || echo "scripts-readme: no"
```

Gotchas route to GOTCHAS.md. Flyway notes to FLYWAY.md. Operational rules stay in CLAUDE.md.

What I found interesting was how long the bug had been there unnoticed. The skill only uses modular detection opportunistically — when it fails, it silently continues in single-file mode. No error, no warning, just incorrect routing on every subsequent commit. The symptom (CLAUDE.md gradually growing) would only become visible over many sessions, and would look exactly like normal documentation drift. `modular-handling.md` had the same problem — Python imports from scripts that were also never written. The whole modular infrastructure had been scaffolded against a missing foundation.

Going forward the routing should hold.
