# Retrospective Issue Mapping — mdproctor/mdproctor.github.io

Generated: 2026-04-09
Covers: 2026-02-06 → 2026-04-06 (110 commits)

---

## Epic 1: Build KIE blog archive mirror — #1

**Label:** `epic, enhancement`
**Date range:** 2026-04-01 → 2026-04-02

### Overview
Archive the full KIE blog (blog.kie.org) as a self-contained static HTML mirror,
extracting content, images, YouTube thumbnails, and Gist embeds for 577+ posts.
Image recovery via Wayback Machine CDX and multiple mirror strategies preserves
post fidelity after the original CDN was shut down.

### Child Issues

#### #2 — Build KIE archive extraction pipeline

**Label:** `enhancement`
**Date range:** 2026-04-01

**Key commits:**
- `006ebf1` Add KIE blog archive design spec
- `c45bedf` Add KIE blog archive implementation plan
- `33a63c3` chore: scaffold KIE archive scripts and gitignore
- `58acf33` chore: document lxml 5.x version rationale (Python 3.13 compat)
- `5589df6` feat: author slug and post slug normalisation
- `14dd4ec` feat: resumable state file load/save
- `c7058a2` feat: metadata extraction from WordPress HTML
- `3b15863` fix: move BS4 import to top, handle corrupt state JSON
- `8b3efdb` feat: image download with SHA-256 deduplication
- `1b0ef19` feat: YouTube iframe extraction and thumbnail replacement
- `663947e` feat: GitHub Gist detection, API fetch, and inline code replacement
- `f77c9e3` fix: HTML-escape YouTube/Gist values in generated HTML
- `3a1befc` feat: article content cleaning, attribute stripping
- `887c50c` feat: standalone HTML shell wrapper with archive metadata
- `e27113c` fix: HTML-escape date and archived_date in make_html_shell
- `8636bf9` feat: main extraction orchestrator (images, YouTube, Gists, HTML shell)
- `8186afe` fix: remove unused state param, add post-navigation CSS skip, add logging config
- `e398148` feat: validation pass for images, links, and unreplaced gists
- `871972b` feat: index generator — browsable HTML index grouped by author
- `86fbe31` fix: author selector for real KIE blog markup, add REST API mirror script
- `68482eb` fix: strip URL fragments in check_local_links, guard against IsADirectoryError
- `d7bf8f7` fix: strip trailing slashes in url_to_mirror_path
- `edc618a` fix: filter directories from discover_posts
- `894645a` fix: skip .html directories in process_post

**What:** Build all extraction scripts: metadata parsing, image deduplication, YouTube thumbnail replacement, Gist inlining, content cleaning, HTML shell generation, validation, and a browsable index.

#### #3 — Recover broken images via Wayback Machine and mirroring

**Label:** `enhancement`
**Date range:** 2026-04-01

**Key commits:**
- `b8a2169` feat: add Wayback Machine image recovery and Playwright iframe recovery scripts
- `c1fd464` feat: lazy image recovery — wire 4,632 already-cached images to placeholders
- `47404e9` fix: add Wayback fallback to lazy image recovery
- `afda37a` feat: comprehensive 5-approach image recovery (data-src mirror, Wayback CDX, archive.today, cross-posts)
- `d657ceb` feat: comprehensive image recovery — Wayback CDX date-targeted, ederign.me URL remapping, optaplanner.io mirrors, YouTube/Vimeo iframe fixes, tracking pixel cleanup

**What:** Recover post images that were broken after CDN shutdown — lazy image recovery (wiring cached copies), Wayback Machine CDX API with date targeting, ederign.me/optaplanner.io mirror remapping, and a five-approach orchestrator.

---

## Standalones — April 2–3

#### #4 — Attempt bulk MD conversion from KIE HTML (reverted in favour of manual review)

**Label:** `enhancement`
**Date range:** 2026-04-02

**Key commits:**
- `53917a6` feat: convert all 578 Mark Proctor posts to Jekyll Markdown
- `e3833bd` chore: remove auto-converted mark-proctor posts — starting over with manual review process

**What:** Generated MD for all 578 posts automatically, then reverted — the bulk output was insufficiently accurate, so the approach was replaced with a tool-assisted manual review process.

#### #5 — Build blog review tool (App 1 HTML reviewer + App 2 MD conversion reviewer)

**Label:** `enhancement`
**Date range:** 2026-04-03

**Key commits:**
- `6f99863` feat: complete App 1 (HTML archive reviewer) + App 2 (MD conversion reviewer)
- `8992315` feat: complete blog migration review tool

**What:** Two browser-based review UIs — App 1 for inspecting raw HTML archive posts, App 2 for reviewing auto-generated Markdown with side-by-side comparison.

---

## Epic 2: Build Sparge blog migration app — #6

**Label:** `epic, enhancement`
**Date range:** 2026-04-04 → 2026-04-06

### Overview
Sparge (originally "blog-migrator") is a local web app for reviewing, enriching, and publishing migrated KIE blog posts. It evolved from a single-project script into a multi-project architecture with CodeMirror editors, a full edit mode, and an HTML enrichment pipeline.

### Child Issues

#### #7 — Build blog-migrator multi-project app with ingestion, review, and bulk operations

**Label:** `enhancement`
**Date range:** 2026-04-04

**Key commits:**
- `3996256` feat(blog-migrator): asset scanning and issue highlighting
- `ec5e2d7` feat(blog-migrator): validate scope, bulk staged ops, manual MD editing
- `1960370` feat(blog-migrator): ingestion pipeline + bulk ops + manual MD editing
- `3c0fee5` feat(blog-migrator): multi-project architecture with projects landing page
- `9f6bd6a` feat(blog-migrator): test suite + security fixes + navigation bug fix
- `5db43ed` fix(blog-migrator): clean up project dirs created by API tests
- `6a54038` fix(blog-migrator): merge Scan HTML + Scan Assets into single Scan action
- `7f8db8` brand: rename Blog Migrator → Sparge

**What:** Full rewrite of the review tool as a multi-project server app: ingestion pipeline, asset scanning, issue highlighting, bulk staged operations, manual MD editing, a projects landing page, and initial test suite. Renamed to Sparge at end of this phase.

#### #8 — Add ~/.sparge config, project storage migration, and author filter

**Label:** `enhancement`
**Date range:** 2026-04-05

**Key commits:**
- `ef8f8b7` feat(sparge-home): read ~/.sparge/config.json for projects_dir
- `71b9491` feat(sparge-home): auto-migrate projects from blog-migrator/projects/ on first run
- `e387e11` feat(server): use PROJECTS_DIR from ~/.sparge/config.json; auto-migrate on startup
- `7fd655d` feat(server): GET /api/posts?author=X filters by author; falls back to config
- `0b47d85` feat(ui): author filter dropdown — pre-selected from config, re-fetches on change
- `27671122` fix(ui): avoid double fetch on startup — use pre-loaded cfg for initial author filter
- `aba527e` chore: remove one-off migration code from sparge_home and server
- `8db3c84` test(config): verify github_token round-trips through _resolve

**What:** Move project storage to `~/.sparge/config.json` with automatic migration from the old `blog-migrator/projects/` path. Add author filter endpoint and UI dropdown.

#### #9 — Add HTML enrichment pipeline (YouTube, Gist, brush normalisation, live-embed)

**Label:** `enhancement`
**Date range:** 2026-04-05

**Key commits:**
- `5f3feff` docs: pipeline spec and content-fidelity implementation plan
- `b6b96d2` docs(pipeline): fix Stage 2a fix table and mark implemented items as Done
- `6ff65e2` docs: add ADRs 0001-0004 for pipeline, storage, author filter, and enrichment stage
- `3a40d27` feat(enrich): YouTube iframe → thumbnail figure replacement
- `2dd0991` feat(enrich): Gist script tag → inlined code figure
- `8a9db9e` feat(enrich): brush:X class normalisation + language detection heuristics
- `75cd4ab` feat(enrich): unknown iframe/object/embed → live-embed fallback figure
- `45db233` feat(enrich): enrich_post() orchestrator — full pipeline
- `518b571` feat(state): add mark_enriched() for enrichment stats tracking
- `cad3494` feat(server): enriched HTML pipeline — scan enriches first, generate-md prefers enriched
- `274d471` fix(server): validate-md cross-checks also prefer enriched HTML
- `ce99926` fix(enrich): fix orchestrator test mock + remove stale brush tokens after normalisation

**What:** Per-post enrichment pipeline: YouTube iframes → thumbnail figures, Gist script tags → inlined code, `brush:X` class normalisation, and a live-embed fallback for unknown embeds. Server routes updated to prefer enriched HTML copies.

#### #10 — Add CodeMirror editors for HTML and Markdown editing

**Label:** `enhancement`
**Date range:** 2026-04-05

**Key commits:**
- `7765b09` docs: CodeMirror editors design spec
- `6fac4d1` docs: CodeMirror editors implementation plan
- `9d40c58` feat(ui): load CodeMirror 5 from CDN with markdown and htmlmixed modes
- `fe94522` feat(ui): upgrade MD editor from textarea to CodeMirror markdown mode
- `7d02a19` feat(ui): add CodeMirror HTML editor for enriched HTML copy
- `377a27d` feat(server): POST /api/posts/{slug}/save-html writes to enriched copy
- `1b59655` feat(server): GET /api/posts/{slug}/html returns raw HTML source
- `bc2c19d` fix(tests): cleanup project dirs from ~/sparge-projects/ not old repo path

**What:** Replace textarea editors with CodeMirror 5 for both Markdown (markdown mode) and HTML (htmlmixed mode). Add server endpoints for HTML source retrieval and save.

#### #11 — Build edit mode — three-partition layout, live preview, scroll sync, exit flows

**Label:** `enhancement`
**Date range:** 2026-04-05

**Key commits:**
- `1d1c5a6` docs: edit mode redesign spec — three-partition layout with live preview
- `5f03563` docs: edit mode redesign implementation plan
- `f142e27` feat(ui): refactor editState/editDirty + pure scroll helpers + JS unit tests
- `7d6f8dc` feat(ui): add marked.js CDN and #md-preview div for live MD preview
- `bc0883a` fix(ui): remove duplicate marked.min.js CDN tag
- `89b8029` feat(ui): add #edit-sidebar HTML and CSS
- `120319a` feat(ui): unified enterEditMode(mode) — nav→sidebar, middle→editor, right→preview
- `da60adf` feat(ui): debounced live preview — HTML iframe srcdoc + MD marked.parse
- `91d6220` feat(ui): edit mode scroll sync — editor↔preview with loop guard
- `e80c37a` feat(ui): exitEditMode, saveEditContent, discardEdit — complete exit flows
- `8f0080c` feat(ui): styled unsaved-changes modal + selectPost navigation guard
- `df37ad2` test(edit-flow): integration tests for HTML/MD save/retrieve cycle
- `707b127` fix(ui): address code review — double-slash URL, duplicate marked.js, scroll accumulation, async toggles, modal consistency
- `f5847dc` test(edit-mode): comprehensive unit + integration tests — cancel/save flows, panel visibility, 20-post mock blog, cross-author isolation

**What:** Full edit mode rework: three-partition layout (nav sidebar → editor → preview), debounced live preview for both HTML and Markdown, scroll sync with loop guard, unsaved-changes modal, and navigation guard. All save/cancel flows implemented and tested.

#### #12 — Add HTML pretty-print to editor view (with lxml encoding fix)

**Label:** `enhancement`
**Date range:** 2026-04-05

**Key commits:**
- `39a81cf` feat(server): pretty-print HTML in editor view — cosmetic only, original untouched
- `b5a8cd6` fix(server): use html.parser not lxml for prettify — lxml double-encodes non-ASCII via meta charset
- `1f237b6` test(prettify): 19 tests — unit, happy path on real posts, integration via /html endpoint
- `a5c7728` test(prettify): regression guard for parser choice + runtime garbling detection in server

**What:** BeautifulSoup `prettify()` for the HTML editor view (cosmetic only — source unchanged). Fixed an lxml double-encoding bug that garbled em dashes and curly quotes across all 577 posts; switched to `html.parser`.

---

## Standalones — April 6

#### #13 — Write Sparge blog series (5 retrospective entries with screenshots)

**Label:** `documentation`
**Date range:** 2026-04-06

**Key commits:**
- `b27b169` docs: Sparge blog entries 1-2 + two-panel reviewer screenshot
- `ae313f6` docs: Sparge blog series — all 5 entries with screenshots
- `7e52492` fix(blog): style guide compliance — register heading, two long sentences

**What:** Five retrospective blog entries written to `docs/blog/`, covering Sparge's evolution from extraction scripts through the review UI, enrichment pipeline, and CodeMirror edit mode. Playwright-generated UI screenshots included.

#### #14 — Consolidate Sparge — integrate asset_store, remove blog-migrator/

**Label:** `refactor`
**Date range:** 2026-04-06

**Key commits:**
- `00f9890` feat(sparge): integrate asset_store + consolidate from original sparge — Option A additive integration
- `d7a6ca3` chore: remove Sparge project docs now living in ~/claude/sparge
- `5888263` chore: remove blog-migrator/ — Sparge now lives at ~/claude/sparge

**What:** Merged `asset_store.py` and `consolidate.py` from the original Sparge proof-of-concept into the main codebase. Deleted `blog-migrator/` from the Jekyll repo — all Sparge code now lives at `~/claude/sparge`.

---

## Excluded Commits (trivial — no ticket)

| Hash | Date | Subject | Reason |
|------|------|---------|--------|
| `6e9f5f3` | 2026-02-06 | Initial commit | Initial scaffold |
| `2e93aa7` | 2026-02-06 | sample blog | Initial scaffold |
| `bc43b73` | 2026-02-06 | sample blog | Initial scaffold |
| `c1e5ff5` | 2026-04-01 | chore: gitignore __pycache__ and wget log | Gitignore only |
| `8582753` | 2026-04-01 | chore: remove __pycache__ from git tracking | Gitignore only |
| `38dd178` | 2026-04-05 | chore: ignore .worktrees/ directory | Gitignore only |
| `73e08f4` | 2026-04-05 | chore: ignore .superpowers/ brainstorm directory | Gitignore only |
| `b87378a` | 2026-04-04 | chore(blog-migrator): remove test project artifacts | Test cleanup |
| `b79e150` | 2026-04-05 | docs: add design snapshot 2026-04-05 | Session artifact |
| `a9f0437` | 2026-04-05 | docs: session handover 2026-04-05 | Session artifact |
| `57470f5` | 2026-04-06 | docs: add design snapshot 2026-04-06 | Session artifact |
| `137283e` | 2026-04-06 | docs: session handover 2026-04-06 | Session artifact |
