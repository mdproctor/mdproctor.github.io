"""
Test suite for md_validator.py
Each test documents the exact failure mode it guards against.
Run: python3 -m pytest tests/test_md_validator.py -v
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / 'scripts'))

from md_validator import validate, MD_CHECKS, CROSS_CHECKS, Issue

# ── Helpers ───────────────────────────────────────────────────────────────────

MINIMAL_FRONT_MATTER = """---
layout: post
title: "Test Post"
date: 2011-01-01
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2011/01/test.html
---

"""

def make_md(body: str) -> str:
    return MINIMAL_FRONT_MATTER + body


def make_html(body: str) -> str:
    return f'<html><body><article>{body}</article></body></html>'


def issues_of(md: str, html: str = None, check: str = None):
    """Run validate and return issues, optionally filtered by check name."""
    html_path = None
    if html:
        import tempfile, os
        with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False) as f:
            f.write(html)
            html_path = Path(f.name)
    try:
        all_issues = validate(md, 'test-slug', html_path)
        if check:
            return [i for i in all_issues if i.check == check]
        return all_issues
    finally:
        if html_path and html_path.exists():
            html_path.unlink()


def has_error(issues, check):
    return any(i.level == 'ERROR' and i.check == check for i in issues)


def has_warn(issues, check):
    return any(i.level == 'WARN' and i.check == check for i in issues)


def is_clean(issues, check):
    return not any(i.check == check for i in issues)


# ══════════════════════════════════════════════════════════════════════════════
# MD-ONLY CHECKS
# ══════════════════════════════════════════════════════════════════════════════

class TestOrphanedPlaceholders:
    """LESSON: Code block placeholders left unreplaced appear as raw text."""

    def test_catches_new_format(self):
        md = make_md("Here is some code:\n\n@@CODEBLOCK_000@@\n\nMore text.")
        assert has_error(issues_of(md), 'orphaned_placeholder')

    def test_catches_old_format(self):
        md = make_md("Code:\n\nCODEBLOCK_FENCE_1\n\nMore.")
        assert has_error(issues_of(md), 'orphaned_placeholder')

    def test_clean_passes(self):
        md = make_md("```java\nint x = 1;\n```")
        assert is_clean(issues_of(md), 'orphaned_placeholder')


class TestStrayDigitAfterFence:
    """LESSON: Partial str.replace('FENCE_1',...) on 'FENCE_10' leaves '0' after ```."""

    def test_catches_digit_after_closing_fence(self):
        md = make_md("```java\ncode\n```0\n\nMore text.")
        assert has_error(issues_of(md), 'stray_digit_after_fence')

    def test_catches_double_digit(self):
        md = make_md("```java\ncode\n```10\n\nMore text.")
        assert has_error(issues_of(md), 'stray_digit_after_fence')

    def test_clean_numbered_list_after_fence(self):
        # A numbered list item after a code block is NOT a stray digit
        md = make_md("```java\ncode\n```\n\n1. First item")
        assert is_clean(issues_of(md), 'stray_digit_after_fence')

    def test_clean_passes(self):
        md = make_md("```java\nint x = 1;\n```\n\nNormal text after.")
        assert is_clean(issues_of(md), 'stray_digit_after_fence')


class TestBalancedFences:
    """LESSON: Unclosed ``` block causes everything after it to render as code."""

    def test_catches_unclosed_block(self):
        md = make_md("```java\nint x = 1;\n```\n\n```python\nprint('hello')\n")
        assert has_error(issues_of(md), 'unbalanced_fences')

    def test_catches_single_fence(self):
        md = make_md("```java\ncode here")
        assert has_error(issues_of(md), 'unbalanced_fences')

    def test_clean_two_blocks(self):
        md = make_md("```java\ncode\n```\n\n```xml\n<tag/>\n```")
        assert is_clean(issues_of(md), 'unbalanced_fences')

    def test_clean_no_code(self):
        md = make_md("Just plain text here, no code blocks at all.")
        assert is_clean(issues_of(md), 'unbalanced_fences')


class TestEmptyCodeBlocks:
    """LESSON: Empty ``` ``` blocks add noise and indicate conversion failure."""

    def test_catches_empty_block(self):
        md = make_md("Text before.\n\n```\n```\n\nText after.")
        assert has_warn(issues_of(md), 'empty_code_blocks')

    def test_catches_empty_with_lang(self):
        md = make_md("```java\n```")
        assert has_warn(issues_of(md), 'empty_code_blocks')

    def test_clean_non_empty(self):
        md = make_md("```java\nint x = 1;\n```")
        assert is_clean(issues_of(md), 'empty_code_blocks')


class TestFrontMatter:
    """LESSON: Missing front matter causes Jekyll to skip the post entirely."""

    def test_catches_no_front_matter(self):
        md = "Just a plain post without front matter."
        assert has_error(issues_of(md), 'missing_front_matter')

    def test_catches_unclosed_front_matter(self):
        md = "---\ntitle: Test\ndate: 2011-01-01\nauthor: Mark Proctor\n"
        assert has_error(issues_of(md), 'unclosed_front_matter')

    def test_catches_missing_title(self):
        md = "---\ndate: 2011-01-01\nauthor: Mark Proctor\n---\n\nBody text here."
        assert has_error(issues_of(md), 'missing_fm_field')

    def test_catches_bad_date_format(self):
        md = "---\ntitle: \"Test\"\ndate: 01/01/2011\nauthor: Mark Proctor\n---\n\nBody."
        assert has_warn(issues_of(md), 'bad_date_format')

    def test_clean_valid_front_matter(self):
        md = make_md("Valid body content here with enough words.")
        fm_issues = [i for i in issues_of(md)
                     if i.check in ('missing_front_matter','unclosed_front_matter','missing_fm_field','bad_date_format')]
        assert not fm_issues


class TestEmptyBody:
    """LESSON: Over-aggressive converter cleaning can strip all content."""

    def test_catches_empty_body(self):
        md = "---\ntitle: \"Test\"\ndate: 2011-01-01\nauthor: Mark Proctor\n---\n\n  "
        assert has_error(issues_of(md), 'empty_body')

    def test_catches_near_empty_body(self):
        md = "---\ntitle: \"Test\"\ndate: 2011-01-01\nauthor: Mark Proctor\n---\n\nHi."
        assert has_error(issues_of(md), 'empty_body')

    def test_clean_substantial_body(self):
        md = make_md("This is a valid post with enough content to pass the check.")
        assert is_clean(issues_of(md), 'empty_body')


class TestWordpressJunk:
    """LESSON: WordPress metadata lines must be stripped by the converter."""

    def test_catches_byline(self):
        md = make_md("by Mark Proctor\n\nActual content here.")
        assert has_warn(issues_of(md), 'wordpress_junk')

    def test_catches_view_all_posts(self):
        md = make_md("Content.\n\n[View all posts](https://blog.kie.org)\n\nMore content.")
        assert has_warn(issues_of(md), 'wordpress_junk')

    def test_catches_post_comment_link(self):
        md = make_md("[Post Comment](https://blogger.com/comment)")
        assert has_warn(issues_of(md), 'wordpress_junk')

    def test_clean_normal_content(self):
        md = make_md("Drools is a rule engine. Here is how it works.")
        assert is_clean(issues_of(md), 'wordpress_junk')


class TestHtmlEntities:
    """LESSON: Raw HTML entities like &amp; should be decoded, not left as-is."""

    def test_catches_amp_entities(self):
        body = " ".join(["This &amp; that &amp; the other &amp; more &amp; even more &amp; another"] * 3)
        md = make_md(body)
        assert has_warn(issues_of(md), 'html_entities_in_body')

    def test_clean_normal_ampersand(self):
        md = make_md("Rules & regulations. This & that.")
        assert is_clean(issues_of(md), 'html_entities_in_body')

    def test_entities_in_code_ok(self):
        # Entities inside code blocks should not trigger
        md = make_md("```xml\n<root>&amp;</root>\n```")
        assert is_clean(issues_of(md), 'html_entities_in_body')


class TestBrokenLinks:
    """LESSON: [text]() with empty href = broken link in the post."""

    def test_catches_empty_href(self):
        md = make_md("Click [here]() for more information.")
        assert has_warn(issues_of(md), 'broken_links')

    def test_clean_valid_link(self):
        md = make_md("Click [here](https://drools.org) for more.")
        assert is_clean(issues_of(md), 'broken_links')


class TestDuplicateParagraphs:
    """LESSON: Double-processing can cause the same paragraph to appear twice.

    Key is 120 chars — must be long enough to distinguish code blocks sharing
    a package prefix (e.g. 'package com.example;import java.util.Arr' would
    match ArrayList vs Arrays at 60 chars).
    """

    def test_catches_duplicate(self):
        long_para = ("This is a long paragraph about Drools rule engines and how they work in "
                     "practice with real-world examples and complex rule sets.")
        md = make_md(f"{long_para}\n\nSome middle content.\n\n{long_para}")
        assert has_error(issues_of(md), 'duplicate_paragraph')

    def test_clean_no_duplicates(self):
        md = make_md("First paragraph.\n\nSecond paragraph.\n\nThird paragraph.")
        assert is_clean(issues_of(md), 'duplicate_paragraph')

    def test_clean_similar_code_blocks_different_content(self):
        # Two code blocks sharing a long common prefix but with different full content
        # (e.g. Spring XML configs with same <?xml...><beans...> preamble)
        shared = "<?xml version=\"1.0\"?><beans><drools:kbase id=\"kbase\"><drools:resources><drools:resource type=\"DRL\"/>"
        block1 = f"```xml\n{shared}</drools:resources></drools:kbase></beans>\n```"
        block2 = f"```xml\n{shared}</drools:resources></drools:kbase><bean id=\"extra\"/></beans>\n```"
        md = make_md(f"{block1}\n\nSome text between.\n\n{block2}")
        assert is_clean(issues_of(md), 'duplicate_paragraph')


class TestCodeFenceLanguage:
    """LESSON: Unknown language tags produce unstyled code blocks on GitHub."""

    def test_catches_unknown_language(self):
        md = make_md("```droolsrulefile\nrule x when then end\n```")
        assert has_warn(issues_of(md), 'unknown_fence_language')

    def test_clean_known_languages(self):
        md = make_md("```java\ncode\n```\n\n```drl\nrule x end\n```\n\n```xml\n<x/>\n```")
        assert is_clean(issues_of(md), 'unknown_fence_language')

    def test_clean_no_lang_tag(self):
        md = make_md("```\ngeneric code\n```")
        assert is_clean(issues_of(md), 'unknown_fence_language')


# ══════════════════════════════════════════════════════════════════════════════
# CROSS-VALIDATION CHECKS
# ══════════════════════════════════════════════════════════════════════════════

class TestCodeBlockCount:
    """LESSON: Every <pre> in HTML should produce a fenced block in MD."""

    def test_catches_code_blocks_dropped(self):
        html = make_html('<pre><code class="language-java">int x = 1;</code></pre>')
        md = make_md("Text but no code block.")
        assert has_error(issues_of(md, html), 'code_blocks_dropped')

    def test_clean_matching_count(self):
        html = make_html('<p>Code:</p><pre><code class="language-java">int x = 1;</code></pre>')
        md = make_md("Code:\n\n```java\nint x = 1;\n```")
        assert is_clean(issues_of(md, html), 'code_blocks_dropped')

    def test_clean_no_code_in_html(self):
        html = make_html('<p>Just text, no code.</p>')
        md = make_md("Just text, no code.")
        assert is_clean(issues_of(md, html), 'code_blocks_dropped')


class TestCodeContentIntegrity:
    """LESSON: Code content must fully match — first and last lines checked."""

    def test_catches_missing_code_start(self):
        html = make_html('<pre><code class="language-java">package com.example; public class Foo {}</code></pre>')
        md = make_md("```java\nsome completely different code\n```")
        assert has_error(issues_of(md, html), 'code_content_missing')

    def test_clean_matching_code(self):
        code = "package com.example; public class Foo {}"
        html = make_html(f'<pre><code class="language-java">{code}</code></pre>')
        md = make_md(f"```java\n{code}\n```")
        assert is_clean(issues_of(md, html), 'code_content_missing')


class TestLanguageTags:
    """LESSON: language-X class in HTML must produce matching ```X fence."""

    def test_catches_missing_language(self):
        html = make_html('<pre><code class="language-drl">rule x end</code></pre>')
        md = make_md("```java\nrule x end\n```")  # wrong language
        assert has_warn(issues_of(md, html), 'language_tag_missing')

    def test_clean_matching_language(self):
        html = make_html('<pre><code class="language-drl">rule x end</code></pre>')
        md = make_md("```drl\nrule x end\n```")
        assert is_clean(issues_of(md, html), 'language_tag_missing')


class TestWordCount:
    """LESSON: MD word count < 35% of HTML = content loss from over-stripping."""

    def test_catches_low_word_count(self):
        long_html = make_html('<p>' + ' '.join(['word'] * 500) + '</p>')
        short_md = make_md("Just a tiny bit of content here.")
        assert has_warn(issues_of(short_md, long_html), 'word_count_low')

    def test_clean_adequate_word_count(self):
        text = ' '.join(['word'] * 100)
        html = make_html(f'<p>{text}</p>')
        md = make_md(text)
        assert is_clean(issues_of(md, html), 'word_count_low')


class TestHeadingMatch:
    """LESSON: h2/h3 text from HTML must appear in MD — missing = section dropped."""

    def test_catches_missing_heading(self):
        html = make_html('<h2>Advanced Configuration</h2><p>Some content.</p>')
        md = make_md("Some content but no heading.")
        assert has_warn(issues_of(md, html), 'heading_missing')

    def test_clean_matching_heading(self):
        html = make_html('<h2>Advanced Configuration</h2><p>Some content.</p>')
        md = make_md("## Advanced Configuration\n\nSome content.")
        assert is_clean(issues_of(md, html), 'heading_missing')

    def test_ignores_author_heading(self):
        # "Author" h2 is WordPress chrome, not content — should be stripped
        html = make_html('<h2>Author</h2><p>Mark Proctor</p>')
        md = make_md("Content without author section.")
        # "Author" is too short (<5 chars) to be checked, so no false positive
        assert is_clean(issues_of(md, html), 'heading_missing')


class TestListPreservation:
    """LESSON: <ul>/<ol> lists in HTML should produce list items in MD."""

    def test_catches_lists_dropped(self):
        html = make_html('<ul><li>Item one</li><li>Item two</li><li>Item three</li></ul>')
        md = make_md("Item one. Item two. Item three.")
        assert has_warn(issues_of(md, html), 'lists_dropped')

    def test_clean_lists_present(self):
        html = make_html('<ul><li>Item one</li><li>Item two</li></ul>')
        md = make_md("- Item one\n- Item two")
        assert is_clean(issues_of(md, html), 'lists_dropped')


class TestLinkCount:
    """LESSON: External links in MD should be comparable to HTML — big drop = loss."""

    def test_catches_links_dropped(self):
        links = ' '.join(f'<a href="https://example{i}.com">Link {i}</a>' for i in range(10))
        html = make_html(f'<p>{links}</p>')
        md = make_md("Text with no links at all.")
        assert has_warn(issues_of(md, html), 'links_dropped')

    def test_clean_links_present(self):
        html = make_html('<a href="https://drools.org">Drools</a> is great.')
        md = make_md("This is [Drools](https://drools.org) and it is great.")
        assert is_clean(issues_of(md, html), 'links_dropped')

    def test_clean_few_html_links(self):
        # Less than 5 links — threshold not triggered
        html = make_html('<p><a href="https://a.com">A</a> and <a href="https://b.com">B</a>.</p>')
        md = make_md("A and B.")
        assert is_clean(issues_of(md, html), 'links_dropped')

    def test_clean_angle_bracket_links(self):
        # html2text produces ](<https://...>) angle-bracket format — must count as links
        links = ' '.join(f'<a href="https://example{i}.com">Link {i}</a>' for i in range(10))
        html = make_html(f'<p>{links}</p>')
        md = make_md(' '.join(f'[Link {i}](<https://example{i}.com>)' for i in range(10)))
        assert is_clean(issues_of(md, html), 'links_dropped')


class TestLastSectionPresent:
    """LESSON: Last paragraph of HTML should appear in MD — detects end truncation."""

    def test_catches_truncation(self):
        html = make_html(
            '<p>Middle content here for a while.</p>'
            '<p>This is the final conclusion paragraph that should definitely appear.</p>'
        )
        md = make_md("Middle content here for a while.")
        assert has_warn(issues_of(md, html), 'truncated_at_end')

    def test_clean_full_content(self):
        conclusion = "This is the final conclusion paragraph that should definitely appear."
        html = make_html(f'<p>Middle content.</p><p>{conclusion}</p>')
        md = make_md(f"Middle content.\n\n{conclusion}")
        assert is_clean(issues_of(md, html), 'truncated_at_end')


class TestImageCount:
    """LESSON: Content images in HTML must have representation in MD."""

    def test_catches_images_dropped(self):
        imgs = ''.join(f'<img src="/assets/images/2011/01/img{i}.png" alt="img{i}">'
                       for i in range(4))
        html = make_html(f'<p>{imgs}</p>')
        md = make_md("Content with no images mentioned at all.")
        assert has_warn(issues_of(md, html), 'images_dropped')

    def test_clean_images_present(self):
        html = make_html('<img src="/assets/images/2011/01/img1.png" alt="diagram">')
        md = make_md("![diagram](/legacy/assets/images/2011/01/img1.png)")
        assert is_clean(issues_of(md, html), 'images_dropped')

    def test_clean_missing_placeholder_counts(self):
        html = make_html('<img src="/assets/images/2011/01/img1.png" alt="img">'
                         '<img src="/assets/2011/01/img2.png" alt="img">'
                         '<img src="/assets/2011/01/img3.png" alt="img">'
                         '<img src="/assets/2011/01/img4.png" alt="img">')
        md = make_md("> **📷 Missing image** — img1\n\n> **📷 Missing image** — img2\n\n"
                     "> **📷 Missing image** — img3\n\n> **📷 Missing image** — img4")
        assert is_clean(issues_of(md, html), 'images_dropped')


class TestTechnicalTerms:
    """LESSON: Key KIE/Drools technical terms from HTML must appear in MD."""

    def test_catches_drools_missing(self):
        html = make_html('<p>Drools is a powerful rule engine framework.</p>')
        md = make_md("It is a powerful framework for processing rules.")
        assert has_warn(issues_of(md, html), 'technical_terms_missing')

    def test_clean_term_present(self):
        html = make_html('<p>Drools uses the Rete algorithm.</p>')
        md = make_md("Drools uses the Rete algorithm.")
        assert is_clean(issues_of(md, html), 'technical_terms_missing')

    def test_clean_no_terms_in_html(self):
        # Post not about KIE topics — no terms to check
        html = make_html('<p>This is about general programming concepts.</p>')
        md = make_md("This is about general programming concepts.")
        assert is_clean(issues_of(md, html), 'technical_terms_missing')


# ══════════════════════════════════════════════════════════════════════════════
# META: Verify the validator structure itself
# ══════════════════════════════════════════════════════════════════════════════

class TestValidatorStructure:
    """Ensure the validator is well-formed and all checks are registered."""

    def test_md_checks_are_callable(self):
        from md_validator import MD_CHECKS
        for fn in MD_CHECKS:
            assert callable(fn), f'{fn} is not callable'

    def test_cross_checks_are_callable(self):
        from md_validator import CROSS_CHECKS
        for fn in CROSS_CHECKS:
            assert callable(fn), f'{fn} is not callable'

    def test_all_checks_return_list(self):
        md = make_md("Some valid content here for testing.")
        from md_validator import MD_CHECKS
        for fn in MD_CHECKS:
            result = fn(md, 'test')
            assert isinstance(result, list), f'{fn.__name__} did not return a list'

    def test_clean_post_has_no_errors(self):
        """A well-formed post with no issues should pass all MD checks cleanly."""
        md = make_md(
            "Drools is a [rule engine](https://drools.org) from the KIE community.\n\n"
            "## How it works\n\n"
            "The Rete algorithm processes rules efficiently:\n\n"
            "```java\nKieSession session = kieContainer.newKieSession();\n"
            "session.insert(new Fact());\nsession.fireAllRules();\n```\n\n"
            "- Feature one\n- Feature two\n- Feature three\n\n"
            "For more information visit the [KIE website](https://kie.org)."
        )
        errors = [i for i in issues_of(md) if i.level == 'ERROR']
        assert not errors, f'Clean post has errors: {errors}'
