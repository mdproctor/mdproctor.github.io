#!/usr/bin/env python3
"""
Persistent issues list for the Mark Proctor post review tool.
Stores validation errors and user-flagged problems as a JSON file.
"""
import json, time
from pathlib import Path
from typing import List, Optional

ROOT = Path('/Users/mdproctor/mdproctor.github.io')
ISSUES_FILE = ROOT / 'mark-proctor' / '.issues.json'


def load() -> dict:
    if ISSUES_FILE.exists():
        return json.loads(ISSUES_FILE.read_text())
    return {'posts': {}}


def save(data: dict):
    tmp = ISSUES_FILE.with_suffix('.tmp')
    tmp.write_text(json.dumps(data, indent=2))
    tmp.rename(ISSUES_FILE)


def add_validation_issues(slug: str, title: str, issues: list):
    """Called by the validator after each conversion run."""
    if not issues:
        return
    data = load()
    errors = [{'level': i.level, 'check': i.check, 'detail': i.detail} for i in issues]
    # Merge with existing entry if present
    existing = data['posts'].get(slug, {})
    data['posts'][slug] = {
        'slug': slug,
        'title': title,
        'issues': errors,
        'flagged_by_user': existing.get('flagged_by_user', False),
        'user_note': existing.get('user_note', ''),
        'last_checked': time.strftime('%Y-%m-%d'),
        'status': 'open',
    }
    save(data)


def flag_by_user(slug: str, title: str, note: str = ''):
    """Called when the user manually flags a post as having a problem."""
    data = load()
    existing = data['posts'].get(slug, {})
    data['posts'][slug] = {
        'slug': slug,
        'title': title or existing.get('title', slug),
        'issues': existing.get('issues', []),
        'flagged_by_user': True,
        'user_note': note,
        'last_checked': time.strftime('%Y-%m-%d'),
        'status': 'open',
    }
    save(data)


def resolve(slug: str):
    """Mark a post as resolved (keep in list but mark done)."""
    data = load()
    if slug in data['posts']:
        data['posts'][slug]['status'] = 'resolved'
        save(data)


def remove(slug: str):
    """Remove a post from the issues list entirely."""
    data = load()
    data['posts'].pop(slug, None)
    save(data)


def get_all() -> List[dict]:
    data = load()
    return sorted(data['posts'].values(),
                  key=lambda p: (p.get('status','open') == 'resolved', p.get('slug','')))


def has_errors(issues: list) -> bool:
    return any(i.get('level') == 'ERROR' or (hasattr(i, 'level') and i.level == 'ERROR')
               for i in issues)
