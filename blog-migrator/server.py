#!/usr/bin/env python3
"""
Blog Migrator — unified server.

Serves static files from serve_root AND the UI, plus a JSON API.

Endpoints
─────────
GET  /                              → redirect to /ui/
GET  /ui/                           → ui/index.html
GET  /api/config                    → current config (public fields)
POST /api/config                    → update config fields and reload
GET  /api/posts                     → all posts with state (JSON array)
GET  /api/posts/{slug}              → single post state
PATCH /api/posts/{slug}             → update flagged / user_note / reviewed
POST /api/posts/{slug}/generate-md  → generate (or regenerate) Markdown
POST /api/posts/{slug}/generate-md?dry=1 → dry-run: return content, no write
POST /api/posts/{slug}/validate-md  → run MD validator
POST /api/posts/{slug}/scan-html    → scan HTML for issues
POST /api/posts/{slug}/scan-assets  → scan image/asset localisation for this post
POST /api/posts/{slug}/stage        → body=md content → write .md.staged, mark staged
GET  /api/posts/{slug}/staged       → return content of .md.staged file
POST /api/posts/{slug}/accept-staged → promote .md.staged → .md
POST /api/posts/{slug}/reject-staged → delete .md.staged, clear staged flag
GET  /*                             → static file from serve_root
"""
import json
import mimetypes
import sys
import urllib.parse
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

# ── Bootstrap path so scripts/ is importable ──────────────────────────────────
ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT))

from scripts.config import cfg, load as reload_cfg, save as save_cfg
from scripts import state as State
from scripts.state import stage as state_stage, accept_staged, reject_staged

SERVE_ROOT = cfg['_root']
UI_DIR     = ROOT / 'ui'
POSTS_DIR  = cfg['_posts_dir']
MD_DIR     = cfg['_md_dir']

# Pre-import MD tools from parent scripts/ if available
_parent_scripts = ROOT.parent / 'scripts'
sys.path.insert(0, str(_parent_scripts))
try:
    from convert_post import convert_post
    _can_generate = True
except ImportError:
    _can_generate = False

try:
    from md_validator import validate as validate_md
    _can_validate = True
except ImportError:
    _can_validate = False

# scan_html lives in our own scripts/
sys.path.insert(0, str(ROOT / 'scripts'))
try:
    from scan_html import scan_post as _scan_post
    _can_scan = True
except ImportError:
    _can_scan = False

try:
    from scan_assets import scan_assets as _scan_assets
    _can_scan_assets = True
except ImportError:
    _can_scan_assets = False


# ── Handler ────────────────────────────────────────────────────────────────────

class Handler(BaseHTTPRequestHandler):

    def log_message(self, fmt, *args):
        print(f'  {self.command} {self.path}')

    def send_cors(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PATCH, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_cors()
        self.end_headers()

    # ── Routing ────────────────────────────────────────────────────────────────

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path   = parsed.path.rstrip('/')

        if path == '':
            self._redirect('/ui/')
        elif path == '/ui' or path.startswith('/ui/'):
            self._serve_ui(path)
        elif path == '/api/config':
            self._api_config_get()
        elif path == '/api/posts':
            self._api_posts_list()
        elif path.startswith('/api/posts/'):
            rest = path[len('/api/posts/'):]
            if rest.endswith('/staged'):
                self._api_staged_get(rest[:-len('/staged')])
            else:
                self._api_post_get(rest)
        else:
            self._serve_static(parsed.path)

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        params = dict(urllib.parse.parse_qsl(parsed.query))
        path   = parsed.path.rstrip('/')
        body   = self._read_body()

        if path == '/api/config':
            self._api_config_post(body)
        elif path.startswith('/api/posts/'):
            rest = path[len('/api/posts/'):]
            if rest.endswith('/generate-md'):
                dry = params.get('dry') == '1'
                self._api_generate_md(rest[:-len('/generate-md')], dry=dry)
            elif rest.endswith('/validate-md'):
                self._api_validate_md(rest[:-len('/validate-md')])
            elif rest.endswith('/scan-html'):
                self._api_scan_html(rest[:-len('/scan-html')])
            elif rest.endswith('/scan-assets'):
                self._api_scan_assets(rest[:-len('/scan-assets')])
            elif rest.endswith('/stage'):
                self._api_stage(rest[:-len('/stage')], body)
            elif rest.endswith('/save-md'):
                self._api_save_md(rest[:-len('/save-md')], body)
            elif rest.endswith('/accept-staged'):
                self._api_accept_staged(rest[:-len('/accept-staged')])
            elif rest.endswith('/reject-staged'):
                self._api_reject_staged(rest[:-len('/reject-staged')])
            else:
                self._json(404, {'error': 'unknown endpoint'})
        else:
            self._json(404, {'error': 'unknown endpoint'})

    def do_PATCH(self):
        parsed = urllib.parse.urlparse(self.path)
        path   = parsed.path.rstrip('/')
        body   = self._read_body()

        if path.startswith('/api/posts/'):
            slug = path[len('/api/posts/'):]
            self._api_post_patch(slug, body)
        else:
            self._json(404, {'error': 'unknown endpoint'})

    # ── API handlers ───────────────────────────────────────────────────────────

    def _api_config_get(self):
        public = {k: v for k, v in cfg.items() if not k.startswith('_')}
        self._json(200, public)

    def _api_config_post(self, body: str):
        try:
            patch = json.loads(body)
        except json.JSONDecodeError:
            self._json(400, {'error': 'invalid JSON'})
            return
        cfg.update(patch)
        save_cfg(cfg)
        self._json(200, {'saved': True})

    def _api_posts_list(self):
        posts = State.get_all()
        # Sort by date then slug
        posts.sort(key=lambda p: (p.get('date', ''), p.get('slug', '')))
        self._json(200, posts)

    def _api_post_get(self, slug: str):
        post = State.get(slug)
        if post is None:
            self._json(404, {'error': f'unknown slug: {slug}'})
            return
        self._json(200, post)

    def _api_post_patch(self, slug: str, body: str):
        try:
            patch = json.loads(body)
        except json.JSONDecodeError:
            self._json(400, {'error': 'invalid JSON'})
            return
        # Only allow safe top-level fields
        allowed = {'flagged', 'user_note', 'reviewed'}
        safe = {k: v for k, v in patch.items() if k in allowed}
        State.update(slug, safe)
        self._json(200, State.get(slug))

    def _api_generate_md(self, slug: str, dry: bool = False):
        if not _can_generate:
            self._json(503, {'error': 'convert_post not available'})
            return
        html_path = POSTS_DIR / (slug + '.html')
        if not html_path.exists():
            self._json(404, {'error': f'HTML not found: {slug}'})
            return
        md_path = MD_DIR / (slug + '.md')
        try:
            content = convert_post(html_path)
            if dry:
                # Return generated content without writing anything
                print(f'Dry-run: {slug}.md')
                self._text(200, content)
                return
            md_path.write_text(content, encoding='utf-8')
            State.mark_md_generated(slug)
            if _can_validate:
                issues = validate_md(content, slug, html_path)
                State.set_md_issues(slug, [
                    {'check': i.check, 'level': i.level,
                     'detail': i.detail, 'selector': None}
                    for i in issues
                ])
            print(f'Generated: {slug}.md')
            self._json(200, State.get(slug))
        except Exception as e:
            self._json(500, {'error': str(e)})

    def _api_validate_md(self, slug: str):
        if not _can_validate:
            self._json(503, {'error': 'md_validator not available'})
            return
        md_path   = MD_DIR / (slug + '.md')
        html_path = POSTS_DIR / (slug + '.html')
        if not md_path.exists():
            self._json(404, {'error': 'MD not generated yet'})
            return
        content = md_path.read_text(errors='replace')
        issues  = validate_md(content, slug,
                              html_path if html_path.exists() else None)
        State.set_md_issues(slug, [
            {'check': i.check, 'level': i.level,
             'detail': i.detail, 'selector': None}
            for i in issues
        ])
        self._json(200, State.get(slug))

    def _api_scan_html(self, slug: str):
        html_path = POSTS_DIR / (slug + '.html')
        if not html_path.exists():
            self._json(404, {'error': f'HTML not found: {slug}'})
            return
        if not _can_scan:
            self._json(503, {'error': 'scan_html not available'})
            return
        try:
            raw_issues = _scan_post(html_path)
            # Convert to state-compatible format
            issues = [
                {'type': i['type'], 'level': i['level'],
                 'check': i['type'],  # alias for MD-validator compatibility
                 'detail': i['detail'], 'selector': i.get('selector')}
                for i in raw_issues
            ]
            State.set_html_issues(slug, issues)
            errors = sum(1 for i in issues if i['level'] == 'ERROR')
            warns  = sum(1 for i in issues if i['level'] == 'WARN')
            print(f'Scanned: {slug} — {errors}E {warns}W')
            self._json(200, State.get(slug))
        except Exception as e:
            self._json(500, {'error': str(e)})

    def _api_scan_assets(self, slug: str):
        html_path = POSTS_DIR / (slug + '.html')
        if not html_path.exists():
            self._json(404, {'error': f'HTML not found: {slug}'})
            return
        if not _can_scan_assets:
            self._json(503, {'error': 'scan_assets not available'})
            return
        try:
            from datetime import datetime, timezone
            result = _scan_assets(html_path)
            now = datetime.now(timezone.utc).isoformat()
            assets = {
                'total':     result['total'],
                'localised': result['localised'],
                'broken':    result['broken'],
                'checked_at': now,
            }
            State.update(slug, {'assets': assets})
            print(f'Assets: {slug} — {result["localised"]}/{result["total"]} localised, {result["broken"]} broken')
            self._json(200, State.get(slug))
        except Exception as e:
            self._json(500, {'error': str(e)})

    def _api_save_md(self, slug: str, content: str):
        """Write manually-edited MD content directly to SLUG.md and re-validate."""
        md_path = MD_DIR / (slug + '.md')
        try:
            md_path.write_text(content, encoding='utf-8')
            # Mark as generated from current HTML hash (manual edit doesn't change staleness)
            State.mark_md_generated(slug)
            # Re-validate immediately
            html_path = POSTS_DIR / (slug + '.html')
            if _can_validate:
                issues = validate_md(content, slug,
                                     html_path if html_path.exists() else None)
                State.set_md_issues(slug, [
                    {'check': i.check, 'level': i.level,
                     'detail': i.detail, 'selector': None}
                    for i in issues
                ])
            print(f'Saved (manual edit): {slug}.md')
            self._json(200, State.get(slug))
        except Exception as e:
            self._json(500, {'error': str(e)})

    # ── Staged workflow endpoints ──────────────────────────────────────────────────

    def _api_staged_get(self, slug: str):
        """Return the content of the staged MD file."""
        staged_path = MD_DIR / (slug + '.md.staged')
        if not staged_path.exists():
            self._json(404, {'error': 'no staged version'})
            return
        self._text(200, staged_path.read_text(encoding='utf-8'))

    def _api_stage(self, slug: str, content: str):
        """Write content to SLUG.md.staged and mark post as staged."""
        staged_path = MD_DIR / (slug + '.md.staged')
        try:
            staged_path.write_text(content, encoding='utf-8')
            state_stage(slug)
            print(f'Staged: {slug}')
            self._json(200, State.get(slug))
        except Exception as e:
            self._json(500, {'error': str(e)})

    def _api_accept_staged(self, slug: str):
        """Promote SLUG.md.staged → SLUG.md, run validation, update state."""
        ok = accept_staged(slug)
        if not ok:
            self._json(404, {'error': 'no staged version to accept'})
            return
        md_path   = MD_DIR / (slug + '.md')
        html_path = POSTS_DIR / (slug + '.html')
        if _can_validate and md_path.exists():
            content = md_path.read_text(errors='replace')
            issues  = validate_md(content, slug,
                                  html_path if html_path.exists() else None)
            State.set_md_issues(slug, [
                {'check': i.check, 'level': i.level,
                 'detail': i.detail, 'selector': None}
                for i in issues
            ])
        print(f'Accepted staged: {slug}')
        self._json(200, State.get(slug))

    def _api_reject_staged(self, slug: str):
        """Delete SLUG.md.staged, clear staged flag."""
        reject_staged(slug)
        print(f'Rejected staged: {slug}')
        self._json(200, State.get(slug))

    # ── Static file serving ────────────────────────────────────────────────────

    def _serve_ui(self, url_path: str):
        if url_path in ('/ui', '/ui/'):
            file_path = UI_DIR / 'index.html'
        else:
            rel = url_path[len('/ui/'):]
            file_path = UI_DIR / rel
        self._serve_file(file_path)

    def _serve_static(self, url_path: str):
        # Decode percent-encoding and strip leading slash
        rel = urllib.parse.unquote(url_path.lstrip('/'))
        self._serve_file(SERVE_ROOT / rel)

    def _serve_file(self, file_path: Path):
        try:
            file_path = file_path.resolve()
            data = file_path.read_bytes()
        except (FileNotFoundError, IsADirectoryError, PermissionError):
            self._json(404, {'error': str(file_path)})
            return
        mime = mimetypes.guess_type(str(file_path))[0] or 'application/octet-stream'
        self.send_response(200)
        self.send_cors()
        self.send_header('Content-Type', mime)
        self.send_header('Content-Length', len(data))
        self.end_headers()
        self.wfile.write(data)

    # ── Helpers ────────────────────────────────────────────────────────────────

    def _redirect(self, location: str):
        self.send_response(302)
        self.send_header('Location', location)
        self.end_headers()

    def _json(self, code: int, data):
        payload = json.dumps(data, ensure_ascii=False).encode()
        self.send_response(code)
        self.send_cors()
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', len(payload))
        self.end_headers()
        self.wfile.write(payload)

    def _read_body(self) -> str:
        length = int(self.headers.get('Content-Length', 0))
        return self.rfile.read(length).decode('utf-8')


# ── Entry point ────────────────────────────────────────────────────────────────

if __name__ == '__main__':
    print('Initialising state from source posts…')
    added = State.init_from_source()
    print(f'  {added} new posts added to state')

    total = len(State.get_all())
    port  = cfg['server']['port']
    print(f'  {total} posts tracked')
    print(f'\nBlog Migrator running → http://localhost:{port}/ui/')
    print(f'Project: {cfg["project_name"]}')

    HTTPServer(('localhost', port), Handler).serve_forever()
