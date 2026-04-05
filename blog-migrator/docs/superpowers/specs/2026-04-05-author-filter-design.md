# Author Filter Design

## Goal

Allow Sparge to restrict both the API and UI to a configured author by default, while letting the user override to see all authors via a UI dropdown.

## Context

- Posts in `state.json` have an `author` field
- `config.json` already has `filter.author` (used during ingest)
- The UI's `filtered()` function already filters posts client-side by status
- `GET /api/posts` currently returns all posts with no filtering

## Architecture

### Backend — `GET /api/posts?author=X`

`_api_posts_list()` in `server.py` reads an optional `author` query parameter:
- If `?author=` is present and non-empty → filter posts to that author
- If `?author=` is absent → fall back to `cfg.get('filter', {}).get('author', '')` as default
- If default is also empty → return all posts (existing behaviour)

No other endpoints change. The author param applies only to the list endpoint.

### UI — Author dropdown in filter bar

A `<select>` dropdown added to the existing `#nav-filters` bar in `index.html`:
- Populated with "All authors" + unique authors from the returned post list
- On page load: pre-selected from `cfg.filter.author` (loaded via `/api/config`)
- On change: re-fetches `/api/posts?author=X` and re-renders the post list
- "All authors" option sends `?author=` (empty string) to override config default

The existing `filtered()` function continues to apply status filters (html-issues, staged, etc.) on top of whatever the author fetch returned.

## Data Flow

```
config.filter.author
    → default for /api/posts requests
    → pre-selects author dropdown on page load

User changes dropdown
    → fetch /api/posts?author={selection}
    → allPosts updated
    → filtered() applies status filter on top
    → renderNav() redraws list
```

## Behaviour Table

| Config `filter.author` | Dropdown | Posts returned |
|---|---|---|
| `"Mark Proctor"` | Mark Proctor (default) | Mark's posts only |
| `"Mark Proctor"` | All authors | All posts in state.json |
| *(empty)* | All authors (default) | All posts |
| *(empty)* | Specific author | That author's posts |

## Files Changed

| File | Change |
|---|---|
| `blog-migrator/server.py` | `_api_posts_list()` reads `?author` param, falls back to `cfg['filter']['author']` |
| `blog-migrator/ui/index.html` | Author `<select>` in `#nav-filters`; pre-select from config; re-fetch on change |

## What Does NOT Change

- No other API endpoints are affected
- `filtered()` logic for status filters (html-issues, staged, etc.) unchanged
- Config `filter.author` continues to control ingest scope as before
- Posts list sort order unchanged
