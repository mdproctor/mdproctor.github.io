# HANDOFF.md

**Date:** 2026-05-06  
**Repo:** mdproctor/mdproctor.github.io  
**Live site:** https://mdproctor.github.io

## What Was Done This Session

Full site build-out from near-scratch:

- **Nav**: Articles · Notes | CaseHub QuarkMind … — hierarchy, baseline alignment, equidistant spacing, active state per project on post pages. CSS override for Minima's `margin-right: 20px` on `.page-link:not(:last-child)`.
- **rustkyll**: Tried, benchmarked (<0.5s saving, no `jekyll-titles-from-headings`), reverted. Back on Jekyll `serve --livereload --incremental`.
- **Articles**: Series TOC auto-generated from `series:` frontmatter. `Guide:` / `Part N:` / `Companion:` prefixes from `series_part`. `order:` field for stable same-date sort. Cross-references audited. Part 4 timeline image found in `sparge/docs/` and restored.
- **Notes migrated**: 100 CaseHub (pre-existing) + 31 QuarkMind + 32 Permuplate + 15 Sparge + 4 Hortara = **182 total**. All standardised frontmatter, images in `assets/<project>/`.
- **Blog routing**: `~/.claude/blog-routing.yaml` created — `entry_type: note → _notes/`, `entry_type: article → _articles/`.
- **CLAUDE.md**: Updated to reflect collections, frontmatter schema, serve.sh, blog routing.

## State

- All content pushed to `origin/main` — GitHub Pages deploying
- Jekyll server running locally at http://localhost:4000

## Immediate Next Step

Commit the CLAUDE.md update:
```bash
git add CLAUDE.md
git commit -m "docs: update CLAUDE.md — collections, frontmatter schema, serve.sh, blog routing"
git push origin main
```

## Key Files

| Path | Purpose |
|------|---------|
| `_notes/` | All 182 project diary entries |
| `_articles/when-the-machine-codes/` | 8-part series + images |
| `css/override.css` | All custom styles |
| `_includes/series-toc.html` | Auto series TOC |
| `~/.claude/blog-routing.yaml` | Personal routing config (not in repo) |
| `serve.sh` | Local dev — Jekyll with livereload + incremental |

## Known Gaps

- Part 5 of "When the Machine Codes" is a published placeholder — intentionally forthcoming
- Project sites (sparge, quarkmind, permuplate etc.) still run separately — syndication on hold, may revisit later
