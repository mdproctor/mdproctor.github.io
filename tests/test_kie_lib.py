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
