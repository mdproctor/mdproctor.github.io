# CLAUDE.md

## Project Type

**Type:** blog

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

This is a Jekyll blog hosted on GitHub Pages. Pushing to `main` triggers an automatic build and deploy — there is no CI/CD pipeline or build scripts. The live site is at `mdproctor.github.io`.

## Local Development

`Gemfile` is committed. Start the local server via:

```bash
./serve.sh    # Serves at http://localhost:4000 with livereload
```

Or manually:
```bash
bundle exec jekyll serve --livereload --incremental --port 4000
```

**Caveat:** `--incremental` only rebuilds content files. Changes to `_layouts/`, `_includes/`, or `_config.yml` require a full restart (`Ctrl-C`, then re-run).

## Content Structure

Two collections, both in `_config.yml` with `output: true`:

**Notes** (`_notes/`) — project diary entries. Published at `/notes/:title/`. Filename: `YYYY-MM-DD-<slug>.md`.

**Articles** (`_articles/`) — long-form polished pieces. Published at `/articles/:path/`. Series articles live in `_articles/<series-name>/`.

**Frontmatter schema (notes):**
```yaml
---
layout: post
title: "Entry Title"
date: YYYY-MM-DD
entry_type: note
subtype: diary
projects: [casehub, casehub-engine]   # project tags, controls nav routing
tags: [tag1, tag2]
excerpt: "One sentence shown in the card list."
---
```

**Frontmatter schema (articles):**
```yaml
---
layout: post
title: "Article Title"
date: YYYY-MM-DD
entry_type: article
series: "Series Name"       # optional
series_part: 1              # optional; 0=guide, "companion"=technical companion
order: 2                    # controls sort order within same date
tags: [tag1, tag2]
excerpt: "One sentence shown in the card list."
---
```

Title is displayed from the `title:` frontmatter field. `jekyll-titles-from-headings` with `strip_title: true` strips the matching H1 from article body on GitHub Pages.

**Projects:** Notes are tagged with project identifiers (`casehub`, `quarkmind`, `permuplate`, `hortara`, `sparge`). The nav and project pages filter by these.

## Architecture

- **Theme**: Minima gem files copied locally into `_layouts/`, `_includes/`, `_sass/`, `assets/` — not loaded from gem. Allows local builds without gem-based theme support.
- **Layouts**: `_layouts/post.html` — shared by notes and articles. Shows series TOC automatically when `series:` frontmatter is present. Hides layout `<h1>` for articles (content H1 serves as title).
- **Includes**: `header.html` (custom nav), `casehub-subnav.html` (CaseHub sub-nav), `note-list.html` (card list with pagination + read-more), `series-toc.html` (auto-generated series table of contents), `navlinks.html` (prev/next), `sharelinks.html`.
- **CSS**: `css/override.css` — all custom styles (nav hierarchy, card layout, tags, series TOC, pagination).
- **Syntax highlighting**: highlight.js (`js/highlightjs/`). Languages bundled: Markdown, T-SQL, PowerShell, Plaintext.
- **Plugins**: `jekyll-feed`, `jekyll-sitemap`, `jekyll-seo-tag`, `jekyll-titles-from-headings`.

## Blog Routing

New notes/articles are written in project workspaces and published here via `~/.claude/blog-routing.yaml`:
- `entry_type: note` → `_notes/`
- `entry_type: article` → `_articles/`

Run `/publish-blog` from any project workspace to route entries.

## Pre-Publish Checklist

**Before committing any article or note:**
- All referenced images exist under `assets/<project>/`
- `excerpt:` is populated
- `projects:` tags are set correctly (notes only)

## Work Tracking

**Issue tracking:** enabled
**GitHub repo:** mdproctor/mdproctor.github.io
**Changelog:** GitHub Releases (run `gh release create --generate-notes` at milestones)

**Automatic behaviours (Claude follows these at all times in this project):**
- **Before implementation begins** — when the user says "implement", "start coding",
  "execute the plan", "let's build", or similar: check if an active issue or epic
  exists. If not, run issue-workflow Phase 1 to create one **before writing any code**.
- **Before writing any code** — check if an issue exists for what's about to be
  implemented. If not, draft one and assess epic placement (issue-workflow Phase 2)
  before starting. Also check if the work spans multiple concerns.
- **Before any commit** — run issue-workflow Phase 3 (via git-commit) to confirm
  issue linkage and check for split candidates. This is a fallback — the issue
  should already exist from before implementation began.
- **All commits should reference an issue** — `Refs #N` (ongoing) or `Closes #N` (done).
  If the user explicitly says to skip ("commit as is", "no issue"), ask once to confirm
  before proceeding — it must be a deliberate choice, not a default.
