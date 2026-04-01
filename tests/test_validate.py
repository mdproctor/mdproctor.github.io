import sys
import json
from pathlib import Path
sys.path.insert(0, 'scripts')
from validate_kie import check_local_images, check_unreplaced_gists
from bs4 import BeautifulSoup


def _write(path, content):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content)


def test_check_local_images_all_present(tmp_path):
    img_path = tmp_path / 'assets' / 'images' / '2023' / '07' / 'abc-img.png'
    img_path.parent.mkdir(parents=True, exist_ok=True)
    img_path.write_bytes(b'fake')

    html = '<html><body><img src="../../assets/images/2023/07/abc-img.png"></body></html>'
    post_path = tmp_path / 'posts' / 'author' / '2023-07-01-post.html'
    _write(post_path, html)

    issues = check_local_images(post_path, tmp_path)
    assert issues == []


def test_check_local_images_missing(tmp_path):
    html = '<html><body><img src="../../assets/images/2023/07/missing.png"></body></html>'
    post_path = tmp_path / 'posts' / 'author' / '2023-07-01-post.html'
    _write(post_path, html)

    issues = check_local_images(post_path, tmp_path)
    assert len(issues) == 1
    assert issues[0]['type'] == 'missing_image'


def test_check_unreplaced_gists_clean(tmp_path):
    html = '<html><body><pre><code>code here</code></pre></body></html>'
    post_path = tmp_path / 'posts' / 'author' / '2023-07-01-post.html'
    _write(post_path, html)
    assert check_unreplaced_gists(post_path) == []


def test_check_unreplaced_gists_found(tmp_path):
    html = '<html><body><script src="https://gist.github.com/user/abc.js"></script></body></html>'
    post_path = tmp_path / 'posts' / 'author' / '2023-07-01-post.html'
    _write(post_path, html)
    issues = check_unreplaced_gists(post_path)
    assert len(issues) == 1
    assert issues[0]['type'] == 'unreplaced_gist'
