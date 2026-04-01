import pytest
import sys
sys.path.insert(0, 'scripts')
from kie_lib import make_author_slug, make_post_slug


def test_make_author_slug_simple():
    assert make_author_slug("Mark Proctor") == "mark-proctor"


def test_make_author_slug_accents():
    assert make_author_slug("Gonzalo Muñoz Fernández") == "gonzalo-munoz-fernandez"


def test_make_author_slug_multiple_spaces():
    assert make_author_slug("John  Doe") == "john-doe"


def test_make_author_slug_already_ascii():
    assert make_author_slug("Jozef Marko") == "jozef-marko"


def test_make_author_slug_single_name():
    assert make_author_slug("Trilobite") == "trilobite"


def test_make_post_slug_standard():
    assert make_post_slug("https://blog.kie.org/2023/07/groupby-a-new-way.html") == "groupby-a-new-way"


def test_make_post_slug_no_html_extension():
    assert make_post_slug("https://blog.kie.org/2023/07/some-post") == "some-post"


def test_make_post_slug_trailing_slash():
    assert make_post_slug("https://blog.kie.org/2023/07/some-post/") == "some-post"


import json
import tempfile
from pathlib import Path
from kie_lib import load_state, save_state


def test_load_state_missing_file():
    with tempfile.TemporaryDirectory() as d:
        state = load_state(Path(d) / '._state.json')
    assert state == {'completed': [], 'failed': [], 'image_cache': {}}


def test_load_state_existing_file():
    with tempfile.TemporaryDirectory() as d:
        p = Path(d) / '._state.json'
        p.write_text(json.dumps({'completed': ['http://a.com'], 'failed': [], 'image_cache': {}}))
        state = load_state(p)
    assert state['completed'] == ['http://a.com']


def test_save_state_roundtrip():
    with tempfile.TemporaryDirectory() as d:
        p = Path(d) / '._state.json'
        original = {'completed': ['http://x.com'], 'failed': [], 'image_cache': {'abc': 'path'}}
        save_state(original, p)
        loaded = load_state(p)
    assert loaded == original


def test_save_state_atomic(tmp_path):
    p = tmp_path / '._state.json'
    save_state({'completed': [], 'failed': [], 'image_cache': {}}, p)
    assert p.exists()
    assert not (tmp_path / '._state.tmp').exists()
