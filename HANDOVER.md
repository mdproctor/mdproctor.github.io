# Handover — 2026-04-05

**Head commit:** `6ff65e2` — docs: add ADRs 0001-0004 for pipeline, storage, author filter, and enrichment stage
**Previous handover:** none (first handover this project)

## What Changed This Session

- Built and merged **content fidelity pipeline** (Sub-project 1): `enrich.py` with YouTube thumbnails, Gist inlining, brush:X normalisation, language detection, embed fallbacks. Scan now enriches first; Generate MD prefers enriched HTML.
- Built and merged **storage migration**: `~/.sparge/config.json` → `~/sparge-projects/`. Project data migrated from `blog-migrator/projects/`. Migration code removed after use.
- Built and merged **author filter**: `GET /api/posts?author=X` + UI dropdown pre-selected from config.
- Created `~/claude-workspace/` private GitHub repo with `writing-styles/blog-technical.md` (style guide from 577-post corpus analysis) and `ideas/idea-log.md`.
- Created `write-blog-post` skill; `PERSONAL_WRITING_STYLES_PATH` env var in `~/.claude/settings.json`.
- Froze design state: design snapshot + 4 ADRs committed.

## State Right Now

- 576/577 posts clean in `kie-mark-proctor` project (state.json). 1 post has MD issues.
- All 577 posts pre-date the enrichment pipeline — need bulk re-scan to apply YouTube/Gist/brush fixes.
- `blog-migrator/projects/` still exists (stale — live data is in `~/sparge-projects/`). Safe to delete.
- Two leftover untracked test dirs: `blog-migrator/projects/delete-me-50f616/`, `blog-migrator/projects/test-project-5652be/` — safe to delete.
- 241 tests passing, 1 skipped (server API author filter test — needs running server).

## Immediate Next Step

Write a bulk re-scan script: iterate all slugs in `~/sparge-projects/kie-mark-proctor/state.json`, call `POST http://localhost:9000/api/posts/{slug}/scan` for each. Run after starting `python3 blog-migrator/server.py`. This applies enrichment (YouTube/Gist/brush) to all 577 existing posts.

## Open Questions / Blockers

- Should `enriched/` files be committed to git or gitignored? Currently untracked.
- Full 1,801-post KIE archive: one multi-author Sparge project, or keep author-scoped?
- `scripts/` legacy tools — delete now Sparge supersedes them, or migrate image recovery first?
- Sub-project 2 (image recovery) not yet started.

## References

| Context | Where | Retrieve with |
|---|---|---|
| Design state | `blog-migrator/docs/design-snapshots/2026-04-05-sparge-pipeline-and-storage.md` | `cat` |
| Pipeline reference | `blog-migrator/docs/pipeline.md` | `cat` |
| ADRs 0001-0004 | `blog-migrator/docs/adr/` | `ls` then `cat` as needed |
| Writing style guide | `~/claude-workspace/writing-styles/blog-technical.md` | `cat` |
| Garden submission | `~/claude/knowledge-garden/submissions/2026-04-05-claude-code-settings-json-custom-keys.md` | pending merge |

## Environment

- Sparge server: `python3 blog-migrator/server.py` (port 9000)
- Project data: `~/sparge-projects/kie-mark-proctor/`
- `PERSONAL_WRITING_STYLES_PATH=~/claude-workspace/writing-styles` in `~/.claude/settings.json` env block
- `~/claude-workspace` → private GitHub: `mdproctor/claude-workspace`
