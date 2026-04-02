#!/usr/bin/env python3
import requests, re, sys, json, time
sys.path.insert(0, '/Users/mdproctor/mdproctor.github.io/scripts')
import kie_lib as lib
from pathlib import Path
from bs4 import BeautifulSoup, Tag

ROOT = Path('/Users/mdproctor/mdproctor.github.io')
LEGACY = ROOT / 'legacy'
state = lib.load_state(ROOT / '._state.json')
session = requests.Session()
session.headers['User-Agent'] = 'Mozilla/5.0'

def embed_to_page_url(embed_url, session):
    try:
        resp = session.get(embed_url, timeout=15, allow_redirects=True)
        if 'slideshare.net' in resp.url and 'embed_code' not in resp.url:
            return resp.url
        # Look for canonical or og:url
        for pat in [r'<link rel="canonical" href="(https://[^"]+)"',
                    r'"og:url"[^>]+content="(https://[^"]+)"',
                    r'content="(https://www\.slideshare\.net/[^"]+)"']:
            m = re.search(pat, resp.text)
            if m and 'slideshare.net' in m.group(1):
                return m.group(1)
    except:
        pass
    return None

def get_thumbnail(page_url, session):
    try:
        resp = session.get(page_url, timeout=15)
        # Match full thumbnail URL including query string
        m = re.search(r'https://cdn\.slidesharecdn\.com/ss_thumbnails/[^"\'<>\s]+', resp.text)
        if m:
            return m.group(0).replace('&amp;', '&')
        # Also try og:image
        m = re.search(r'property="og:image"[^>]+content="([^"]+)"', resp.text)
        if not m:
            m = re.search(r'content="([^"]+cdn\.slidesharecdn[^"]+)"', resp.text)
        if m:
            return m.group(1).replace('&amp;', '&')
    except:
        pass
    return None

embeds = {
    'https://www.slideshare.net/slideshow/embed_code/9697846':
        '2011-10-18-slides-from-jboss-one-day-talk-2011',
    'https://www.slideshare.net/slideshow/embed_code/26379987':
        '2013-10-03-jbpm-empowers-magnolia-cms-2',
    'https://www.slideshare.net/slideshow/embed_code/27575097':
        '2013-10-25-results-drools-jbpm-workshops-london',
    'https://www.slideshare.net/slideshow/embed_code/key/xn8Wh1hNnXJ9HZ':
        '2015-04-23-jboss-bpm-suite-v6-1-available',
}
known_pages = {
    'https://www.slideshare.net/slideshow/embed_code/27575097':
        'https://www.slideshare.net/slideshow/drools-j-bpm-workshop/27575097',
}

fixed = 0
for embed_url, stem in embeds.items():
    posts = list(LEGACY.rglob(f'posts/**/*{stem}*.html'))
    if not posts:
        print(f'Post not found: {stem}')
        continue
    post_path = posts[0]
    sidecar = post_path.with_suffix('.json')
    post_date = json.loads(sidecar.read_text()).get('date','2013-01-01') if sidecar.exists() else '2013-01-01'

    page_url = known_pages.get(embed_url) or embed_to_page_url(embed_url, session)
    print(f'[{stem[-20:]}]')
    print(f'  page: {page_url}')

    if not page_url:
        print(f'  Could not resolve')
        continue

    thumb_url = get_thumbnail(page_url, session)
    print(f'  thumb: {thumb_url[:60] if thumb_url else None}')
    if not thumb_url:
        continue

    content = lib.download_image(thumb_url, session)
    if not content or len(content) < 500:
        print(f'  Download failed')
        continue

    h = lib.compute_image_hash(content)
    if h not in state['image_cache']:
        rel = lib.get_local_image_path(thumb_url, h, post_date)
        p = LEGACY / 'assets' / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(content)
        state['image_cache'][h] = rel
    local = f'../../assets/{state["image_cache"][h]}'

    repl_html = (
        f'<figure class="video-embed">'
        f'<a href="{page_url}" target="_blank" rel="noopener">'
        f'<img src="{local}" alt="SlideShare presentation" style="max-width:100%">'
        f'<figcaption>&#128202; View on SlideShare</figcaption>'
        f'</a></figure>'
    )

    soup = BeautifulSoup(post_path.read_text(errors='replace'), 'lxml')
    changed = False
    for iframe in soup.find_all('iframe'):
        if not isinstance(iframe, Tag):
            continue
        src = (iframe.get('src', '') or '').strip()
        # Fix both empty iframes AND iframes with SlideShare embed src
        if src and 'slideshare' not in src.lower():
            continue
        repl = BeautifulSoup(repl_html, 'lxml').body.next
        parent = iframe.parent
        if isinstance(parent, Tag) and parent.name == 'figure':
            parent.replace_with(repl)
        else:
            iframe.replace_with(repl)
        changed = True

    if changed:
        out = str(soup)
        if not out.startswith('<!DOCTYPE'):
            out = '<!DOCTYPE html>\n' + out
        post_path.write_text(out, encoding='utf-8')
        print(f'  FIXED: {post_path.name}')
        fixed += 1
    time.sleep(1)

lib.save_state(state, ROOT / '._state.json')
print(f'\nFixed {fixed}/4 SlideShare embeds')
