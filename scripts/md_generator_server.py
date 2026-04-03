#!/usr/bin/env python3
"""
Markdown generation server for the post review viewer.
Listens on port 8767. Accepts:
  GET /generate?post=YYYY-MM-DD-slug      → generates .md, returns content
  GET /status?post=YYYY-MM-DD-slug        → returns {"exists": true/false}
  GET /current                            → returns current post slug
  POST /current  body=slug               → sets current post slug
  GET /issues                             → returns full issues list
  POST /issues/flag?post=SLUG body=note  → user-flag a post as problematic
  POST /issues/resolve?post=SLUG         → mark a post resolved
  POST /issues/remove?post=SLUG          → remove from issues list
"""
import sys, json, urllib.parse
from pathlib import Path
from http.server import HTTPServer, BaseHTTPRequestHandler

ROOT = Path('/Users/mdproctor/mdproctor.github.io')
sys.path.insert(0, str(ROOT / 'scripts'))
from convert_post import convert_post
from issues_list import flag_by_user, resolve, remove, get_all

OUT_DIR = ROOT / 'mark-proctor'
LEGACY_DIR = ROOT / 'legacy/posts/mark-proctor'

current_post = {'slug': None}


class Handler(BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):
        pass  # suppress default logging

    def send_cors(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_cors()
        self.end_headers()

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        params = dict(urllib.parse.parse_qsl(parsed.query))

        if parsed.path == '/generate':
            post_slug = params.get('post', '')
            dry = params.get('dry', '') == '1'  # dry=1: return content without writing MD
            if not post_slug:
                self._json(400, {'error': 'missing post param'})
                return

            html_name = post_slug.replace('.md', '') + '.html'
            html_path = LEGACY_DIR / html_name
            md_path = OUT_DIR / (post_slug.replace('.html', '') + '.md')

            if not html_path.exists():
                self._json(404, {'error': f'HTML source not found: {html_name}'})
                return

            try:
                content = convert_post(html_path)
                if not dry:
                    md_path.write_text(content, encoding='utf-8')
                    print(f'Generated: {md_path.name}')
                else:
                    print(f'Dry-run: {md_path.name}')
                self._text(200, content)
            except Exception as e:
                self._json(500, {'error': str(e)})

        elif parsed.path == '/status':
            post_slug = params.get('post', '')
            md_path = OUT_DIR / post_slug
            self._json(200, {'exists': md_path.exists()})

        elif parsed.path == '/current':
            self._json(200, {'slug': current_post['slug']})

        elif parsed.path == '/issues':
            self._json(200, {'issues': get_all()})

        elif parsed.path == '/list':
            # Return ordered list of all mark-proctor HTML files
            posts = sorted(p.stem for p in LEGACY_DIR.glob('*.html'))
            self._json(200, {'posts': posts})

        else:
            self._json(404, {'error': 'unknown endpoint'})

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        params = dict(urllib.parse.parse_qsl(parsed.query))
        length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(length).decode('utf-8')

        if parsed.path == '/save':
            post_slug = params.get('post', '').strip()
            if not post_slug:
                self._json(400, {'error': 'missing post param'})
                return
            md_path = OUT_DIR / (post_slug.replace('.html', '') + '.md')
            md_path.write_text(body, encoding='utf-8')
            print(f'Saved: {md_path.name}')
            self._json(200, {'saved': True})

        elif parsed.path == '/current':
            body = body.strip()
            current_post['slug'] = body
            print(f'Current post: {body}')
            self._json(200, {'slug': body})

        elif parsed.path == '/issues/flag':
            slug = params.get('post', '')
            # Get title from sidecar if available
            sidecar = LEGACY_DIR / (slug + '.json')
            title = ''
            if sidecar.exists():
                import json as _j
                title = _j.loads(sidecar.read_text()).get('title', slug)
            flag_by_user(slug, title, body)
            print(f'User flagged: {slug}')
            self._json(200, {'slug': slug, 'flagged': True})

        elif parsed.path == '/issues/resolve':
            slug = params.get('post', body.strip())
            resolve(slug)
            self._json(200, {'slug': slug, 'status': 'resolved'})

        elif parsed.path == '/issues/remove':
            slug = params.get('post', body.strip())
            remove(slug)
            self._json(200, {'slug': slug, 'removed': True})

        else:
            self._json(404, {'error': 'unknown endpoint'})

    def _json(self, code, data):
        payload = json.dumps(data).encode()
        self.send_response(code)
        self.send_cors()
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', len(payload))
        self.end_headers()
        self.wfile.write(payload)

    def _text(self, code, text):
        payload = text.encode('utf-8')
        self.send_response(code)
        self.send_cors()
        self.send_header('Content-Type', 'text/markdown; charset=utf-8')
        self.send_header('Content-Length', len(payload))
        self.end_headers()
        self.wfile.write(payload)


if __name__ == '__main__':
    port = 8767
    server = HTTPServer(('localhost', port), Handler)
    print(f'Generator server running on http://localhost:{port}')
    server.serve_forever()
