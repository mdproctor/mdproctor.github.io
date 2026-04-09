# CLAUDE.md

## Project Type

**Type:** blog

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

This is a Jekyll blog hosted on GitHub Pages. Pushing to `main` triggers an automatic build and deploy — there is no CI/CD pipeline or build scripts. The live site is at `mdproctor.github.io`.

## Local Development

No `Gemfile` is committed, so local Jekyll must be installed separately. Standard commands once Jekyll is available:

```bash
bundle exec jekyll serve        # Serve locally at http://localhost:4000
bundle exec jekyll serve --drafts  # Include draft posts
```

## Writing Posts

Posts live in `_posts/` and must follow the filename convention: `YYYY-MM-DD-post-title.md`.

Front matter format:
```yaml
---
tags:
  - TagName
author: Author Name
date: YYYY-MM-DD
---
```

- The post title is auto-derived from the first `##` heading (via `jekyll-titles-from-headings`), or falls back to the filename.
- All posts default to tag `Other` if no tag is specified (`_config.yml` defaults).
- A template is available at `_posts/post_template.md`.

## Architecture

- **Theme**: Minima (GitHub Pages built-in), customized via `_includes/` overrides.
- **Layouts**: `_layouts/post.html` extends Minima's default post layout, adding prev/next navigation and social share links.
- **Includes**: `head.html` loads highlight.js for syntax highlighting (Kramdown's built-in highlighter is disabled). `navlinks.html` handles prev/next post navigation. `sharelinks.html` provides social share buttons.
- **Syntax highlighting**: highlight.js (in `js/highlightjs/`), not Rouge/Kramdown. Supported languages bundled: T-SQL, PowerShell, Plaintext.
- **Archive**: `archive.md` groups all posts by tag using Liquid templating.
- **Plugins**: `jekyll-feed` (RSS), `jekyll-sitemap`, `jekyll-titles-from-headings` — all provided by GitHub Pages gem, no local installation needed.
- **CSS**: `css/override.css` contains the only custom styles (post navigation flexbox layout).

## Key Config (`_config.yml`)

Social links, site title, author, and description are all placeholder values — update these when personalizing the site. Google Analytics is supported but commented out in `head.html`.

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
