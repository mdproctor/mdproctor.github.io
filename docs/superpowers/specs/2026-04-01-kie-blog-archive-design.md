# KIE Blog Archive — Design Spec

**Date:** 2026-04-01  
**Goal:** Create a local, high-fidelity, offline-capable static archive of all posts from blog.kie.org.

---

## Scope

- **Source:** https://blog.kie.org — ~1,800 posts across 173 pages
- **Content types:** Articles (1434), Releases (111), Events (89), News (79), Presentations (62), Videos (40)
- **Output:** `legacy/` folder in this repo (browsable offline, not published to GitHub Pages)
- **Raw mirror:** `kie-mirror/` folder — gitignored, HTML-only wget dump used as source for extraction

---

## Non-Goals

- Publishing the archive to GitHub Pages (future task)
- Converting posts to Markdown (future task — will use the JSON sidecars as source)
- Preserving WordPress comments (dynamically loaded via JS, not archivable)
- Preserving social share buttons or analytics scripts

---

## Folder Structure

```
kie-mirror/                        ← gitignored, raw wget HTML pages only
legacy/
  assets/
    images/
      YYYY/MM/                     ← article images, deduplicated by content hash
        <content-hash>-filename.ext
    article.css                    ← minimal offline stylesheet extracted from blog
  posts/
    <author-slug>/                 ← e.g. mark-proctor/, christopher-chianelli/
      YYYY-MM-DD-<post-slug>.html  ← standalone article HTML
      YYYY-MM-DD-<post-slug>.json  ← metadata sidecar
  index.html                       ← browsable local index grouped by author
  validation-report.json           ← post-extraction validation results
._state.json                       ← gitignored, extraction progress tracker
```

---

## Phase 1 — wget HTML Mirror

Download all post HTML pages from blog.kie.org. No assets (CSS, JS, images, fonts) — HTML only.

**Command:**
```bash
wget \
  --mirror \
  --no-parent \
  --wait=1 --random-wait \
  --tries=3 \
  --retry-connrefused \
  --user-agent="Mozilla/5.0 (compatible; KIE-Archive/1.0)" \
  --reject "*.css,*.js,*.woff,*.woff2,*.ttf,*.eot,*.png,*.jpg,*.jpeg,*.gif,*.svg,*.ico,*.json,*.xml,*.rss,*.atom" \
  --directory-prefix=kie-mirror \
  https://blog.kie.org
```

**Result:** `kie-mirror/blog.kie.org/YYYY/MM/post-slug.html` for each post, plus pagination and index pages (which are used only for post discovery and then ignored).

**Estimated size:** ~360 MB (1,800 pages × ~200 KB each).

---

## Phase 2 — Python Extractor (`scripts/extract_kie.py`)

Reads the local mirror, extracts article content, downloads article images, handles embedded content transformations, and writes the final archive.

### 2.1 Post Discovery

Walk `kie-mirror/blog.kie.org/` for files matching `YYYY/MM/*.html` where YYYY is a 4-digit year. For each file:
- Parse with BeautifulSoup
- Check for presence of `<article class="post">` (WordPress article element) — skip non-post pages (tag indexes, author pages, search results, pagination)
- Extract canonical URL from `<link rel="canonical">` meta tag

Skip any URL already recorded as `completed` in `._state.json`.

### 2.2 Metadata Extraction

From each post HTML, extract:

| Field | Source |
|---|---|
| `title` | `<h1 class="entry-title">` or `<title>` tag |
| `author` | `<span class="author">` or schema.org `author` meta |
| `author_slug` | Normalised from author name: lowercase, spaces→hyphens, accents stripped |
| `date` | `<time datetime="...">` attribute (ISO 8601) |
| `categories` | `<a rel="category tag">` elements |
| `tags` | `<a rel="tag">` elements |
| `original_url` | Canonical URL |
| `modified_date` | Schema.org `dateModified` if present |
| `excerpt` | First `<p>` of article body |

### 2.3 Content Extraction

Extract only the `<article>` element. Then strip:
- All `<script>` tags
- All `<style>` tags  
- Social share button containers (`div.addtoany_share_save_container`, `div.sharedaddy`)
- Comment section (`div#comments`, `div.wpDiscuz*`)
- Author bio boxes at article footer (`div.author-box`, `div.jp-relatedposts`)
- Navigation links within the article (prev/next post links)
- All `class`, `id`, `style`, `data-*` attributes on elements (except `src`, `href`, `alt`, `title`, `datetime`, `lang`, `class` on `<code>` and `<pre>` elements for syntax highlighting)

Keep:
- All `<img>` elements within the article body
- All `<a href>` links
- All `<pre><code>` blocks
- All `<figure>`, `<figcaption>` elements
- `<iframe>` only after transformation (see 2.4)

### 2.4 Embedded Content Transformations

**Images (`<img src="...">`):**
1. Resolve URL (may be relative to original domain, or absolute external)
2. Download image with retry (3 attempts, 2s backoff)
3. Compute SHA-256 hash of content
4. Check `._state.json` image cache — if hash already exists, reuse existing path
5. If new: save to `legacy/assets/images/YYYY/MM/<hash[:12]>-<original-filename>`
6. Rewrite `src` attribute to relative path from post file: `../../assets/images/YYYY/MM/...`
7. Preserve `alt` attribute

**YouTube iframes (`<iframe src="youtube.com/embed/VIDEO_ID">`):**
1. Extract `VIDEO_ID` from iframe src
2. Fetch thumbnail: `https://img.youtube.com/vi/VIDEO_ID/hqdefault.jpg`
3. Save thumbnail to `legacy/assets/images/youtube/VIDEO_ID.jpg`
4. Replace iframe with:
   ```html
   <figure class="video-embed">
     <a href="https://www.youtube.com/watch?v=VIDEO_ID" target="_blank" rel="noopener">
       <img src="../../assets/images/youtube/VIDEO_ID.jpg" alt="YouTube video">
       <figcaption>▶ Watch on YouTube</figcaption>
     </a>
   </figure>
   ```

**GitHub Gists (`<script src="https://gist.github.com/USER/GIST_ID.js">`):**
1. Extract `GIST_ID` from script src
2. Call GitHub Gist API: `https://api.github.com/gists/GIST_ID`
3. For each file in the gist, extract `content` and `language`
4. Replace script tag with:
   ```html
   <figure class="gist-embed">
     <figcaption>
       <a href="https://gist.github.com/USER/GIST_ID" target="_blank" rel="noopener">
         View on GitHub Gist: FILENAME
       </a>
     </figcaption>
     <pre><code class="language-LANG">CONTENT</code></pre>
   </figure>
   ```
5. If API call fails (deleted gist, rate limit): leave a visible `<p class="archive-note">` noting the original gist URL, log to validation report

**Other iframes (not YouTube):** Wrap in `<figure class="embed-note">` with a visible note: `[Embedded content from DOMAIN — requires internet connection]` and preserve the iframe as-is. Log to validation report for manual review.

### 2.5 HTML Shell

Wrap the cleaned article element in a minimal standalone HTML document:

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>POST_TITLE — KIE Blog Archive</title>
  <meta name="author" content="AUTHOR">
  <meta name="date" content="YYYY-MM-DD">
  <meta name="original-url" content="ORIGINAL_URL">
  <link rel="stylesheet" href="../../assets/article.css">
</head>
<body>
  <header class="archive-header">
    <p class="archive-note">
      Archived from <a href="ORIGINAL_URL">ORIGINAL_URL</a> on ARCHIVE_DATE.
      Original content © respective authors, licensed CC BY 3.0.
    </p>
  </header>
  ARTICLE_ELEMENT
</body>
</html>
```

### 2.6 Author Slug Normalisation

```
"Mark Proctor"           → mark-proctor
"Gonzalo Muñoz Fernández" → gonzalo-munoz-fernandez
"Jozef Marko"            → jozef-marko
```

Rules: lowercase, Unicode normalise (NFKD), strip non-ASCII, replace spaces/underscores with hyphens, collapse multiple hyphens, strip leading/trailing hyphens.

### 2.7 Output Filename Convention

Following this repo's Jekyll naming convention:

```
YYYY-MM-DD-<post-slug>.html
YYYY-MM-DD-<post-slug>.json
```

Where `post-slug` is derived from the original URL's last path segment (already slugified by WordPress), with `.html` extension stripped.

### 2.8 Metadata Sidecar JSON

```json
{
  "title": "Groupby – a new way to accumulate facts in DRL",
  "author": "Christopher Chianelli",
  "author_slug": "christopher-chianelli",
  "date": "2023-07-11",
  "modified_date": "2023-07-12",
  "categories": ["Rules"],
  "tags": ["DRL", "Drools"],
  "original_url": "https://blog.kie.org/2023/07/groupby-a-new-way-to-accumulate-facts-in-drl.html",
  "archived_date": "2026-04-01",
  "images": [
    {
      "original_url": "https://blog.kie.org/wp-content/uploads/...",
      "local_path": "../../assets/images/2023/07/abc123def456-groupby.png",
      "hash": "abc123def456..."
    }
  ],
  "embedded_videos": [],
  "embedded_gists": [],
  "other_embeds": []
}
```

### 2.9 State File (`._state.json`)

```json
{
  "completed": ["https://blog.kie.org/2023/07/groupby-...html", ...],
  "failed": [
    {"url": "...", "reason": "...", "timestamp": "..."}
  ],
  "image_cache": {
    "<sha256-hash>": "legacy/assets/images/YYYY/MM/hash-filename.ext"
  }
}
```

Re-running the extractor skips URLs in `completed`. URLs in `failed` are retried. This makes the process fully resumable.

### 2.10 Media Type Checks During Extraction

During extraction, if any of the following are encountered, pause and log to a `legacy/needs-review.json` for reporting back:
- Iframes from domains other than YouTube
- `<script>` embeds from domains other than gist.github.com
- Images with non-standard MIME types (not image/jpeg, image/png, image/gif, image/webp, image/svg+xml)
- Images that return HTTP 4xx/5xx
- Gist API failures

After each run, print a summary of needs-review items so they can be discussed before continuing.

---

## Phase 3 — Offline CSS (`scripts/extract_kie.py` — included)

Find the blog's main stylesheet URL from a `<link rel="stylesheet">` tag in any mirrored HTML file (the URL is present even though the CSS file itself was not downloaded). Make a single live network request to fetch it, extract only typography and content-width rules (strip layout, navigation, sidebar, footer rules), and save as `legacy/assets/article.css`. This makes the archive readable in a browser without any internet connection.

Fallback: if the fetch fails, write a minimal hand-crafted stylesheet covering: body font, max-width container, `pre` block styling, `figure`/`figcaption`, `code` inline, responsive images.

---

## Phase 4 — Validation Pass (`scripts/validate_kie.py`)

Run after extraction completes. For each HTML file in `legacy/posts/`:

1. **Local image check:** every `<img src>` starting with `../../assets/` must resolve to an existing file
2. **Local link check:** every `<a href>` pointing to another file in `legacy/` must resolve to an existing file
3. **External link check:** HTTP HEAD request with retry for every external `<a href>` — record status code
4. **Gist inline check:** flag any `<script src="gist.github.com">` that was not replaced (means gist transformation failed)

Output: `legacy/validation-report.json`

```json
{
  "summary": {
    "posts_checked": 1800,
    "missing_images": 3,
    "broken_local_links": 0,
    "dead_external_links": 12,
    "unreplaced_gists": 1
  },
  "issues": [
    {
      "type": "missing_image",
      "post": "legacy/posts/mark-proctor/2022-07-29-ibm-rht.html",
      "src": "../../assets/images/2022/07/abc-banner.png",
      "note": "File not found on disk"
    }
  ]
}
```

---

## Phase 5 — Index Generation (`scripts/generate_index.py`)

Generate `legacy/index.html`: a single static page, no JavaScript, no external resources.

- Posts grouped by author (alphabetical by author slug)
- Within each author: posts sorted by date descending
- Each entry shows: date, title (linked to local HTML), category badges
- Header shows total post count and archive date
- Inline CSS only (no external stylesheet dependency)

---

## Improvements Included

All of the following are incorporated into this design:

| Improvement | Where |
|---|---|
| Resumable state file | `._state.json`, Phase 2.9 |
| Metadata sidecar JSON | Phase 2.8 |
| Asset deduplication via content hash | Phase 2.4 (Images) |
| Author-slug normalisation | Phase 2.6 |
| Offline CSS snapshot | Phase 3 |
| Validation pass | Phase 4 |
| Index page | Phase 5 |
| Polite rate limiting | Phase 1 (`--wait=1 --random-wait`) |

---

## .gitignore Additions

```
kie-mirror/
._state.json
```

---

## Dependencies

Python packages required:
- `requests` — HTTP fetching
- `beautifulsoup4` — HTML parsing
- `lxml` — HTML parser backend
- `Pillow` — image MIME type validation (optional)
- `unicodedata` — stdlib, for author slug normalisation

No additional framework (Scrapy, Scrapy-Splash, etc.) required.

---

## Estimated Scale

| Item | Estimate |
|---|---|
| Posts to archive | ~1,800 |
| wget mirror size | ~360 MB |
| Article images | ~500–800 MB |
| YouTube thumbnails | ~10 MB |
| Total `legacy/` size | ~1.0–1.2 GB |
| Extraction time | 2–4 hours (network-bound on image downloads) |
