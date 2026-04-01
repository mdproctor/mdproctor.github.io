import sys
import json
from pathlib import Path
sys.path.insert(0, 'scripts')
from generate_index import load_all_sidecars, group_by_author, render_index


def _write_sidecar(directory, filename, data):
    p = directory / filename
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(data))
    return p


SIDECAR_A = {
    'title': 'Post A', 'author': 'Mark Proctor', 'author_slug': 'mark-proctor',
    'date': '2022-07-29', 'categories': ['Rules'], 'tags': [],
    'original_url': 'https://blog.kie.org/2022/07/post-a.html',
}
SIDECAR_B = {
    'title': 'Post B', 'author': 'Mark Proctor', 'author_slug': 'mark-proctor',
    'date': '2023-01-10', 'categories': ['AI'], 'tags': [],
    'original_url': 'https://blog.kie.org/2023/01/post-b.html',
}
SIDECAR_C = {
    'title': 'Post C', 'author': 'Jane Smith', 'author_slug': 'jane-smith',
    'date': '2023-05-01', 'categories': ['Tools'], 'tags': [],
    'original_url': 'https://blog.kie.org/2023/05/post-c.html',
}


def test_load_all_sidecars(tmp_path):
    posts_dir = tmp_path / 'posts'
    _write_sidecar(posts_dir / 'mark-proctor', '2022-07-29-post-a.json', SIDECAR_A)
    _write_sidecar(posts_dir / 'jane-smith', '2023-05-01-post-c.json', SIDECAR_C)
    sidecars = load_all_sidecars(tmp_path)
    assert len(sidecars) == 2


def test_group_by_author_keys():
    grouped = group_by_author([SIDECAR_A, SIDECAR_B, SIDECAR_C])
    assert 'mark-proctor' in grouped
    assert 'jane-smith' in grouped


def test_group_by_author_sorted_by_date_desc():
    grouped = group_by_author([SIDECAR_A, SIDECAR_B])
    proctor_posts = grouped['mark-proctor']
    assert proctor_posts[0]['date'] > proctor_posts[1]['date']


def test_render_index_contains_authors():
    grouped = group_by_author([SIDECAR_A, SIDECAR_B, SIDECAR_C])
    html = render_index(grouped, total=3, archived_date='2026-04-01')
    assert 'Mark Proctor' in html
    assert 'Jane Smith' in html


def test_render_index_contains_titles():
    grouped = group_by_author([SIDECAR_A])
    html = render_index(grouped, total=1, archived_date='2026-04-01')
    assert 'Post A' in html


def test_render_index_no_external_resources():
    grouped = group_by_author([SIDECAR_A])
    html = render_index(grouped, total=1, archived_date='2026-04-01')
    assert 'cdn.' not in html
    assert 'googleapis' not in html
    assert '<script' not in html
