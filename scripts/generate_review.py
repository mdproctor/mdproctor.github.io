#!/usr/bin/env python3
"""
Generate legacy/review-issues.html — single-page reviewer for posts with issues.
Features: sidebar grouped by author, iframe viewer, prev/next nav,
          injected visual highlights in post, issue detail panel below post.

Usage:
    python3 scripts/generate_review.py
"""
import html as html_module
import json
import sys
from pathlib import Path
from bs4 import BeautifulSoup

sys.path.insert(0, str(Path(__file__).parent))

LEGACY_DIR = Path("legacy")


def scan_issues(legacy_dir: Path) -> list[dict]:
    posts_dir = legacy_dir / "posts"
    results = []
    for html_path in sorted(posts_dir.rglob("*.html")):
        try:
            soup = BeautifulSoup(html_path.read_text(errors="replace"), "lxml")
        except Exception:
            continue
        issues = []

        # Live external images (not in noscript)
        noscript_imgs = set(id(i) for ns in soup.find_all("noscript") for i in ns.find_all("img"))
        ext_imgs = [
            i["src"] for i in soup.find_all("img", src=True)
            if i["src"].startswith("http") and id(i) not in noscript_imgs
        ]

        # Lazy-loaded images whose data-src was stripped — the noscript fallback
        # tells us the real URL. The browser renders these as blank 1x1 pixels.
        lazy_imgs = [
            i["src"] for ns in soup.find_all("noscript")
            for i in ns.find_all("img", src=True)
            if i["src"].startswith("http")
        ]
        if ext_imgs:
            issues.append({"type": "external_images", "count": len(ext_imgs), "urls": ext_imgs[:5]})
        if lazy_imgs:
            issues.append({"type": "lazy_stripped", "count": len(lazy_imgs), "urls": lazy_imgs[:5]})

        empty_iframes = [f for f in soup.find_all("iframe") if not f.get("src", "").strip()]
        if empty_iframes:
            issues.append({"type": "empty_iframe", "count": len(empty_iframes)})

        live_embeds = soup.find_all("figure", class_="embed-recovered")
        if live_embeds:
            issues.append({"type": "live_embed", "count": len(live_embeds)})

        if not issues:
            continue

        sidecar = html_path.with_suffix(".json")
        meta = {}
        if sidecar.exists():
            try:
                meta = json.loads(sidecar.read_text())
            except Exception:
                pass

        total = sum(i["count"] for i in issues)
        rel = str(html_path.relative_to(legacy_dir))
        results.append({
            "path": rel,
            "title": meta.get("title", html_path.stem)[:90],
            "author": meta.get("author", "Unknown"),
            "author_slug": meta.get("author_slug", "unknown"),
            "date": meta.get("date", ""),
            "issues": issues,
            "total_issues": total,
        })
    return results


def issue_badges(issues: list[dict]) -> str:
    badges = []
    for issue in issues:
        t, n = issue["type"], issue["count"]
        if t == "external_images":
            badges.append(f'<span class="badge img" title="{n} external image(s)">📷 {n}</span>')
        elif t == "lazy_stripped":
            badges.append(f'<span class="badge img" title="{n} lazy-loaded image(s) missing">🖼 {n}</span>')
        elif t == "empty_iframe":
            badges.append(f'<span class="badge iframe" title="{n} unresolved embed(s)">⬜ {n}</span>')
        elif t == "live_embed":
            badges.append(f'<span class="badge live" title="{n} live embed(s)">🌐 {n}</span>')
    return "".join(badges)


def build_html(posts: list[dict]) -> str:
    by_author: dict[str, list] = {}
    for p in posts:
        by_author.setdefault(p["author_slug"], []).append(p)
    by_author = dict(sorted(by_author.items()))

    posts_js = json.dumps([
        {
            "path": p["path"],
            "title": p["title"],
            "author": p["author"],
            "author_slug": p["author_slug"],
            "date": p["date"],
            "issues": p["issues"],
            "total": p["total_issues"],
        }
        for p in posts
    ], ensure_ascii=False)

    sidebar_items = []
    idx = 0
    for author_slug, author_posts in by_author.items():
        author_name = html_module.escape(author_posts[0]["author"])
        safe_slug = html_module.escape(author_slug)
        sidebar_items.append(
            f'<div class="author-group" id="group-{safe_slug}">'
            f'<div class="author-name">{author_name} '
            f'<span class="author-count">({len(author_posts)})</span></div>'
        )
        for p in author_posts:
            badges = issue_badges(p["issues"])
            safe_title = html_module.escape(p["title"])
            safe_date = html_module.escape(p["date"][:10] if p["date"] else "")
            total = p["total_issues"]
            sidebar_items.append(
                f'<div class="post-item" data-idx="{idx}" onclick="loadPost({idx})" id="item-{idx}">'
                f'<div class="post-meta">'
                f'<span class="post-date">{safe_date}</span>'
                f'<span class="post-errors">⚠ {total}</span>'
                f'</div>'
                f'<span class="post-title">{safe_title}</span>'
                f'<div class="badges">{badges}</div>'
                f'</div>'
            )
            idx += 1
        sidebar_items.append("</div>")

    sidebar_html = "\n".join(sidebar_items)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>KIE Archive — Issue Review ({len(posts)} posts)</title>
  <style>
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{ font-family: sans-serif; display: flex; flex-direction: column; height: 100vh; overflow: hidden; background: #1a1a2e; color: #eee; }}

    /* Top nav */
    #topbar {{
      display: flex; align-items: center; gap: 10px; padding: 8px 14px;
      background: #16213e; border-bottom: 2px solid #0f3460; flex-shrink: 0;
    }}
    #topbar button {{
      background: #0f3460; color: #eee; border: 1px solid #e94560;
      padding: 5px 14px; border-radius: 4px; cursor: pointer; font-size: 13px;
    }}
    #topbar button:hover {{ background: #e94560; }}
    #topbar button:disabled {{ opacity: 0.3; cursor: default; }}
    #post-counter {{ color: #888; font-size: 12px; white-space: nowrap; }}
    #post-title-display {{
      flex: 1; font-size: 13px; font-weight: 600; color: #e2e2e2;
      overflow: hidden; text-overflow: ellipsis; white-space: nowrap;
    }}
    #topbar-badges {{ display: flex; gap: 5px; flex-shrink: 0; }}

    /* Layout */
    #layout {{ display: flex; flex: 1; overflow: hidden; }}

    /* Sidebar */
    #sidebar {{
      width: 290px; flex-shrink: 0; overflow-y: auto;
      background: #16213e; border-right: 1px solid #0f3460;
      display: flex; flex-direction: column;
    }}
    #sidebar-header {{
      padding: 8px 12px; font-size: 11px; color: #888; text-transform: uppercase;
      letter-spacing: 0.05em; border-bottom: 1px solid #0f3460;
      position: sticky; top: 0; background: #16213e; z-index: 2; flex-shrink: 0;
    }}
    .author-group {{ border-bottom: 1px solid #0f3460; }}
    .author-name {{
      padding: 7px 12px; font-size: 11px; font-weight: 700; color: #e94560;
      text-transform: uppercase; letter-spacing: 0.04em; background: #0d1b36;
      position: sticky; top: 33px; z-index: 1;
    }}
    .author-count {{ font-weight: normal; color: #555; }}
    .post-item {{
      padding: 6px 10px 6px 14px; cursor: pointer;
      border-bottom: 1px solid #0a1628; transition: background 0.1s;
    }}
    .post-item:hover {{ background: #1e3a5f; }}
    .post-item.active {{
      background: #0f3460; border-left: 3px solid #e94560; padding-left: 11px;
    }}
    .post-meta {{ display: flex; justify-content: space-between; margin-bottom: 2px; }}
    .post-date {{ font-size: 10px; color: #555; }}
    .post-errors {{ font-size: 10px; color: #e94560; font-weight: 700; }}
    .post-item.active .post-errors {{ color: #ff8888; }}
    .post-title {{ display: block; font-size: 11px; color: #bbb; line-height: 1.4; }}
    .post-item.active .post-title {{ color: #fff; }}
    .badges {{ margin-top: 3px; display: flex; gap: 3px; flex-wrap: wrap; }}
    .badge {{ font-size: 10px; padding: 1px 4px; border-radius: 2px; }}
    .badge.img {{ background: #3a1a1a; color: #ff6b6b; }}
    .badge.iframe {{ background: #1a1a3a; color: #6b9eff; }}
    .badge.live {{ background: #1a3a1a; color: #6bff9e; }}

    /* Viewer */
    #viewer {{ flex: 1; display: flex; flex-direction: column; overflow: hidden; min-width: 0; }}
    #post-frame {{ flex: 1; border: none; background: #fff; display: none; }}
    #no-selection {{
      flex: 1; display: flex; align-items: center; justify-content: center;
      color: #444; font-size: 16px;
    }}

    /* Issue panel */
    #issue-panel {{
      flex-shrink: 0; background: #0d1b36; border-top: 2px solid #0f3460;
      padding: 10px 16px; min-height: 110px; max-height: 160px; overflow-y: auto;
      display: none;
    }}
    #issue-panel h3 {{
      font-size: 12px; text-transform: uppercase; letter-spacing: 0.05em;
      color: #888; margin-bottom: 8px;
    }}
    .issue-group {{ margin-bottom: 8px; }}
    .issue-type-header {{
      font-size: 12px; font-weight: 700; margin-bottom: 4px; display: flex; align-items: center; gap: 6px;
    }}
    .issue-type-header.img {{ color: #ff6b6b; }}
    .issue-type-header.iframe {{ color: #6b9eff; }}
    .issue-type-header.live {{ color: #6bff9e; }}
    .issue-detail {{
      font-size: 11px; color: #888; padding: 2px 0 2px 16px;
      overflow: hidden; text-overflow: ellipsis; white-space: nowrap;
    }}
    .issue-count-pill {{
      background: #e94560; color: white; font-size: 10px; padding: 1px 6px;
      border-radius: 10px; font-weight: 700;
    }}
    .issue-row {{
      display: flex; align-items: center; gap: 8px; padding: 5px 8px;
      border-radius: 4px; cursor: pointer; margin-bottom: 3px;
      border: 1px solid transparent; transition: all 0.15s;
    }}
    .issue-row:hover {{ border-color: #ff2222; background: #1a0000; }}
    .issue-row.img {{ background: #200a0a; }}
    .issue-row.iframe {{ background: #0a0a20; }}
    .issue-row.live {{ background: #0a1a0a; }}
    .issue-num {{ color: #555; font-size: 10px; width: 16px; text-align: right; flex-shrink: 0; }}
    .issue-icon {{ flex-shrink: 0; }}
    .issue-text {{ flex: 1; font-size: 11px; color: #ccc; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }}
    .issue-row:hover .issue-text {{ color: #fff; }}
    .issue-goto {{
      flex-shrink: 0; font-size: 10px; color: #ff4444; font-weight: 700;
      opacity: 0; transition: opacity 0.1s;
    }}
    .issue-row:hover .issue-goto {{ opacity: 1; }}

    /* Scrollbar */
    #sidebar::-webkit-scrollbar, #issue-panel::-webkit-scrollbar {{ width: 5px; }}
    #sidebar::-webkit-scrollbar-track, #issue-panel::-webkit-scrollbar-track {{ background: #16213e; }}
    #sidebar::-webkit-scrollbar-thumb, #issue-panel::-webkit-scrollbar-thumb {{ background: #0f3460; border-radius: 3px; }}
  </style>
</head>
<body>

<div id="topbar">
  <button id="btn-prev" onclick="navigate(-1)" disabled>&#8592; Prev</button>
  <button id="btn-next" onclick="navigate(1)" disabled>Next &#8594;</button>
  <span id="post-counter">— / {len(posts)}</span>
  <span id="post-title-display">Select a post from the sidebar</span>
  <span id="topbar-badges"></span>
</div>

<div id="layout">
  <div id="sidebar">
    <div id="sidebar-header">&#9888; {len(posts)} posts · {len(by_author)} authors</div>
    {sidebar_html}
  </div>
  <div id="viewer">
    <div id="no-selection">&#8592; Select a post to review</div>
    <iframe id="post-frame"></iframe>
    <div id="issue-panel">
      <h3>Issues in this post</h3>
      <div id="issue-details"></div>
    </div>
  </div>
</div>

<script>
const POSTS = {posts_js};
let current = -1;

// Inject visual highlights into the iframe. Returns array of issue objects with IDs for scrolling.
function injectHighlights(frameDoc) {{
  const style = frameDoc.createElement('style');
  style.textContent = `
    .kie-issue {{
      outline: 5px solid #ff2222 !important;
      outline-offset: 4px;
    }}
    .kie-issue-label {{
      display: block;
      font-family: sans-serif;
      font-size: 12px;
      font-weight: 700;
      background: #ff2222;
      color: #fff;
      padding: 4px 10px;
      margin: 6px 0;
      border-radius: 3px;
      letter-spacing: 0.02em;
    }}
    .kie-issue-iframe {{
      display: block !important;
      min-height: 60px !important;
      width: 100% !important;
      background: #fff0f0;
    }}
    /* Broken/external images get a large red placeholder box */
    img.kie-issue {{
      min-width: 200px !important;
      min-height: 80px !important;
      display: inline-block !important;
      background: #ff22221a !important;
    }}
  `;
  frameDoc.head.appendChild(style);

  const issues = [];
  let n = 0;

  // Lazy-loaded images where data-src was stripped — detected via noscript sibling.
  // With JS enabled, noscript content is raw TEXT (not parsed HTML), so use regex.
  // Pattern: <img src="data:gif..."><noscript><img src="real-url"></noscript>
  frameDoc.querySelectorAll('img').forEach(img => {{
    const src = img.getAttribute('src') || '';
    if (!src.startsWith('data:')) return;
    const next = img.nextElementSibling;
    if (!next || next.tagName !== 'NOSCRIPT') return;
    // noscript.textContent is the raw HTML text — parse with regex
    const noscriptText = next.textContent || '';
    const match = noscriptText.match(/src=["'](https?:\/\/[^"']+)["']/);
    if (!match) return;
    const realSrc = match[1];

    const id = 'kie-' + (n++);
    img.id = id;
    img.classList.add('kie-issue');
    img.style.cssText += 'min-width:200px!important;min-height:80px!important;display:block!important;background:#ff22221a!important;';
    const fname = realSrc.split('/').pop().split('?')[0].slice(0, 60) || realSrc.slice(0, 60);
    const label = frameDoc.createElement('div');
    label.className = 'kie-issue-label';
    label.textContent = '🖼 Missing lazy image — ' + fname;
    img.insertAdjacentElement('afterend', label);
    issues.push({{ id, icon: '🖼', text: 'Lazy-loaded image (blank): ' + fname, type: 'lazy_stripped' }});
  }});

  // External / missing images (live in DOM, not in noscript)
  frameDoc.querySelectorAll('img').forEach(img => {{
    const src = img.getAttribute('src') || '';
    if (!src.startsWith('http')) return;
    const id = 'kie-' + (n++);
    img.id = id;
    img.classList.add('kie-issue');
    const fname = src.split('/').pop().split('?')[0].slice(0, 60) || src.slice(0, 60);
    const label = frameDoc.createElement('div');
    label.className = 'kie-issue-label';
    label.textContent = '📷 Missing image — ' + fname;
    img.insertAdjacentElement('afterend', label);
    issues.push({{ id, icon: '📷', text: 'Missing image: ' + fname, type: 'external_images' }});
  }});

  // Empty-src iframes (unresolved embeds)
  frameDoc.querySelectorAll('iframe').forEach(iframe => {{
    if ((iframe.getAttribute('src') || '').trim()) return;
    const id = 'kie-' + (n++);
    iframe.id = id;
    iframe.classList.add('kie-issue', 'kie-issue-iframe');
    const label = frameDoc.createElement('div');
    label.className = 'kie-issue-label';
    label.textContent = '⬜ Unresolved embed — src set by JavaScript, not captured statically';
    iframe.insertAdjacentElement('beforebegin', label);
    issues.push({{ id, icon: '⬜', text: 'Unresolved embed (empty src)', type: 'empty_iframe' }});
  }});

  // Live embeds needing internet
  frameDoc.querySelectorAll('figure.embed-recovered').forEach(fig => {{
    const id = 'kie-' + (n++);
    fig.id = id;
    fig.classList.add('kie-issue');
    const iframe = fig.querySelector('iframe');
    const src = iframe ? (iframe.getAttribute('src') || '') : '';
    let domain = 'unknown';
    try {{
      if (src) domain = new URL(src.startsWith('//') ? 'https:' + src : src).hostname;
    }} catch(e) {{ domain = src.slice(0, 30); }}
    const label = frameDoc.createElement('div');
    label.className = 'kie-issue-label';
    label.textContent = '🌐 Live embed (' + domain + ') — requires internet';
    fig.prepend(label);
    issues.push({{ id, icon: '🌐', text: 'Live embed from ' + domain, type: 'live_embed' }});
  }});

  return issues;
}}

// Scroll the iframe to a specific highlighted element and flash it
function scrollToIssue(id) {{
  try {{
    const frame = document.getElementById('post-frame');
    const el = frame.contentDocument.getElementById(id);
    if (!el) return;
    el.scrollIntoView({{ behavior: 'smooth', block: 'center' }});
    // Yellow flash then back to red
    el.style.outlineColor = '#ffdd00';
    el.style.outlineWidth = '6px';
    setTimeout(() => {{
      el.style.outlineColor = '#ff2222';
      el.style.outlineWidth = '5px';
    }}, 600);
  }} catch(e) {{ console.warn('scrollToIssue:', e); }}
}}

function updateIssuePanel(post, liveIssues) {{
  const panel = document.getElementById('issue-panel');
  const details = document.getElementById('issue-details');
  panel.style.display = 'block';

  if (liveIssues) {{
    // We have real injected elements — render each as a clickable row
    if (liveIssues.length === 0) {{
      details.innerHTML = '<div class="issue-detail" style="color:#666">No highlightable issues found in rendered content.</div>';
      return;
    }}
    const rows = liveIssues.map((issue, i) => {{
      const typeClass = issue.type === 'external_images' ? 'img' : issue.type === 'empty_iframe' ? 'iframe' : 'live';
      return `<div class="issue-row ${{typeClass}}" onclick="scrollToIssue('${{issue.id}}')" title="Click to scroll to this issue in the post">
        <span class="issue-num">${{i + 1}}</span>
        <span class="issue-icon">${{issue.icon}}</span>
        <span class="issue-text">${{issue.text}}</span>
        <span class="issue-goto">↑ scroll</span>
      </div>`;
    }});
    details.innerHTML = rows.join('');
  }} else {{
    // Frame not loaded yet — show static summary from JSON data
    const rows = post.issues.map(issue => {{
      const t = issue.type;
      const n = issue.count;
      const typeClass = t === 'external_images' ? 'img' : t === 'empty_iframe' ? 'iframe' : 'live';
      const icon = t === 'external_images' ? '📷' : t === 'empty_iframe' ? '⬜' : '🌐';
      const label = t === 'external_images' ? `Missing images` : t === 'empty_iframe' ? 'Unresolved embeds' : 'Live embeds';
      return `<div class="issue-group">
        <div class="issue-type-header ${{typeClass}}">${{icon}} ${{label}} <span class="issue-count-pill">${{n}}</span></div>
        <div class="issue-detail">Loading post… click will scroll when ready.</div>
      </div>`;
    }});
    details.innerHTML = rows.join('');
  }}
}}

function loadPost(idx) {{
  if (idx < 0 || idx >= POSTS.length) return;

  // Sidebar highlight
  if (current >= 0) {{
    const old = document.getElementById('item-' + current);
    if (old) old.classList.remove('active');
  }}
  current = idx;
  const item = document.getElementById('item-' + idx);
  if (item) {{
    item.classList.add('active');
    item.scrollIntoView({{ block: 'nearest', behavior: 'smooth' }});
  }}

  const post = POSTS[idx];
  const frame = document.getElementById('post-frame');
  const noSel = document.getElementById('no-selection');

  // Show frame
  frame.style.display = 'block';
  noSel.style.display = 'none';

  // Show panel immediately with static summary while frame loads
  updateIssuePanel(post, null);

  // Load frame — inject highlights when ready
  frame.onload = function() {{
    try {{
      const doc = frame.contentDocument || frame.contentWindow.document;
      if (!doc || !doc.body) {{
        document.getElementById('issue-details').innerHTML =
          '<div class="issue-detail" style="color:#f66">Could not access frame content. Try refreshing.</div>';
        return;
      }}
      const liveIssues = injectHighlights(doc);
      updateIssuePanel(post, liveIssues);
    }} catch(e) {{
      document.getElementById('issue-details').innerHTML =
        '<div class="issue-detail" style="color:#f66">Highlight injection failed: ' + e.message + '</div>';
      console.warn('Could not inject highlights:', e);
    }}
  }};
  frame.src = post.path;

  // Topbar
  document.getElementById('post-title-display').textContent = post.title;
  document.getElementById('post-counter').textContent = (idx + 1) + ' / ' + POSTS.length;

  const badgeMap = {{ external_images: '📷', lazy_stripped: '🖼', empty_iframe: '⬜', live_embed: '🌐' }};
  const total = post.total || post.issues.reduce((s, i) => s + (i.count || 1), 0);
  document.getElementById('topbar-badges').textContent =
    '⚠ ' + total + ' · ' + post.issues.map(i => badgeMap[i.type]).join(' ');

  document.getElementById('btn-prev').disabled = (idx === 0);
  document.getElementById('btn-next').disabled = (idx === POSTS.length - 1);

  location.hash = idx;
}}

function navigate(delta) {{ loadPost(current + delta); }}

document.addEventListener('keydown', e => {{
  if (document.activeElement && document.activeElement.tagName === 'IFRAME') return;
  if (e.key === 'ArrowRight' || e.key === 'ArrowDown') navigate(1);
  if (e.key === 'ArrowLeft' || e.key === 'ArrowUp') navigate(-1);
}});

window.addEventListener('load', () => {{
  const hash = parseInt(location.hash.replace('#',''));
  if (!isNaN(hash) && hash >= 0 && hash < POSTS.length) loadPost(hash);
}});
</script>
</body>
</html>"""


def main():
    print("Scanning for posts with issues...")
    posts = scan_issues(LEGACY_DIR)
    by_author = set(p["author_slug"] for p in posts)
    print(f"Found {len(posts)} posts with issues across {len(by_author)} authors")

    html_out = build_html(posts)
    out_path = LEGACY_DIR / "review-issues.html"
    out_path.write_text(html_out, encoding="utf-8")
    print(f"Written to {out_path}")


if __name__ == "__main__":
    main()
