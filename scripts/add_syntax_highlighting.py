#!/usr/bin/env python3
"""
Add syntax highlighting to all Mark Proctor HTML posts.
- Downloads/uses local highlight.js
- Detects languages from class names or code content
- Backs up every modified post
- Keeps a change log
- Validates post text content is unchanged
- Regenerates stale .md files

Usage: python3 scripts/add_syntax_highlighting.py [--dry-run]
"""
import re, sys, json, time, shutil
from pathlib import Path
from bs4 import BeautifulSoup, Tag, Comment

ROOT = Path('/Users/mdproctor/mdproctor.github.io')
LEGACY = ROOT / 'legacy/posts/mark-proctor'
BACKUP_DIR = ROOT / 'legacy/posts/mark-proctor/.syntax-backups'
CHANGE_LOG = ROOT / 'legacy/posts/mark-proctor/.syntax-changes.json'
MD_DIR = ROOT / 'mark-proctor'

DRY_RUN = '--dry-run' in sys.argv

# Relative paths from post file to assets
HLJS_JS  = '../../assets/js/highlight.min.js'
HLJS_CSS = '../../assets/css/highlight-github.min.css'

# Custom DRL language init snippet (inline JS)
DRL_LANG_DEF = """
hljs.registerLanguage('drl', function(hljs) {
  return {
    keywords: {
      keyword: 'rule when then end import package declare extends implements ' +
               'salience agenda-group ruleflow-group lock-on-active no-loop ' +
               'auto-focus activation-group date-effective date-expires enabled ' +
               'duration timer query function global eval not and or exists ' +
               'forall accumulate collect from entry-point over window ' +
               'attributes modify update insert retract delete assert',
      literal: 'true false null'
    },
    contains: [
      hljs.C_LINE_COMMENT_MODE,
      hljs.C_BLOCK_COMMENT_MODE,
      hljs.APOS_STRING_MODE,
      hljs.QUOTE_STRING_MODE,
      hljs.C_NUMBER_MODE,
      { begin: '"', end: '"', className: 'string' }
    ]
  };
});
"""

# Language detection heuristics for unlabelled code blocks
LANG_PATTERNS = [
    ('drl',        re.compile(r'\b(rule\s+"[^"]+"|when\s*\n|salience\s+\d|declare\s+\w|end\s*$)', re.M)),
    ('java',       re.compile(r'\b(public\s+(class|interface|enum)|import\s+java|@Override|System\.out|void\s+\w+\s*\()', re.M)),
    ('python',     re.compile(r'\bdef\s+\w+\s*\(|^\s*import\s+\w|print\(|self\.|:\s*$', re.M)),
    ('typescript', re.compile(r'\binterface\s+\w|\btype\s+\w+\s*=|:\s*(string|number|boolean|void)\b|async\s+\w+', re.M)),
    ('javascript', re.compile(r'\b(const|let|var)\s+\w|\bfunction\s+\w|\bconsole\.(log|error)|\.\s*then\s*\(|=>\s*\{', re.M)),
    ('json',       re.compile(r'^\s*\{[\s\S]*"[^"]+"\s*:\s*("|true|false|\d|\[|\{)', re.M)),
    ('yaml',       re.compile(r'^[a-zA-Z_][a-zA-Z0-9_]*:\s*\S|^\s*-\s+\w', re.M)),
    ('xml',        re.compile(r'<[a-zA-Z][a-zA-Z0-9]*(\s+[a-zA-Z]+=".+")?\s*(/?>|>[\s\S]*</)', re.M)),
    ('sql',        re.compile(r'\b(SELECT|INSERT|UPDATE|DELETE|FROM|WHERE|CREATE TABLE)\b', re.I)),
    ('bash',       re.compile(r'^#!.*(bash|sh)|^\$\s+\w|mvn\s+|wget\s+|curl\s+', re.M)),
]

CLASS_TO_LANG = {
    'brush: java':        'java',
    'brush: python':      'python',
    'brush: javascript':  'javascript',
    'brush: js':          'javascript',
    'brush: xml':         'xml',
    'brush: sql':         'sql',
    'brush: bash':        'bash',
    'brush: shell':       'bash',
    'language-java':      'java',
    'language-python':    'python',
    'language-javascript':'javascript',
    'language-typescript':'typescript',
    'language-xml':       'xml',
    'language-json':      'json',
    'language-yaml':      'yaml',
    'language-drl':       'drl',
    'language-sql':       'sql',
    'language-bash':      'bash',
}


def detect_language(code_text: str) -> str | None:
    for lang, pattern in LANG_PATTERNS:
        if pattern.search(code_text):
            return lang
    return None


def normalize_class(cls_list: list) -> str | None:
    cls_str = ' '.join(cls_list).lower()
    for pattern, lang in CLASS_TO_LANG.items():
        if pattern in cls_str:
            return lang
    # Direct language-X class
    for c in cls_list:
        m = re.match(r'language-(\w+)', c)
        if m: return m.group(1)
    return None


def get_text_fingerprint(soup) -> str:
    """Extract just text content for change validation."""
    article = soup.find('article') or soup.find('body')
    if not article: return ''
    # Remove script/style tags for comparison
    for tag in article.find_all(['script', 'style', 'link']): tag.extract()
    return re.sub(r'\s+', ' ', article.get_text()).strip()


def process_post(html_path: Path, backup_dir: Path, dry_run: bool) -> dict:
    result = {'path': str(html_path), 'changed': False, 'langs': [], 'blocks': 0}

    text = html_path.read_text(errors='replace')
    if '<pre' not in text and '<code' not in text:
        return result

    soup = BeautifulSoup(text, 'lxml')
    before_fp = get_text_fingerprint(BeautifulSoup(text, 'lxml'))

    # Remove old/existing highlight.js scripts and styles so we standardise
    removed_old = False
    for tag in list(soup.find_all(['script', 'link'])):
        if not isinstance(tag, Tag): continue
        src = tag.get('src', '') or tag.get('href', '')
        if 'highlight' in src.lower() or 'syntaxhighlighter' in src.lower() or 'prettify' in src.lower():
            tag.decompose(); removed_old = True
    # Remove old brush: classes from pre/code, replace with language-X
    for tag in soup.find_all(['pre', 'code']):
        if not isinstance(tag, Tag): continue
        classes = tag.get('class', [])
        lang = normalize_class(classes)
        if lang:
            tag['class'] = [f'language-{lang}']
        elif any('brush:' in c or 'prettyprint' in c for c in classes):
            tag['class'] = []

    # Find and label all code blocks
    changed_any = False
    for pre in soup.find_all('pre'):
        if not isinstance(pre, Tag): continue
        code = pre.find('code') if pre.find('code') else None
        target = code if code else pre

        classes = target.get('class', [])
        lang = normalize_class(classes)

        if not lang:
            code_text = target.get_text()
            if len(code_text.strip()) > 20:
                lang = detect_language(code_text)

        if lang:
            target['class'] = [f'language-{lang}']
            result['langs'].append(lang)
            changed_any = True
            result['blocks'] += 1

    # Also handle inline code blocks that are standalone (not in pre)
    for code in soup.find_all('code'):
        if not isinstance(code, Tag): continue
        if code.find_parent('pre'): continue  # already handled
        classes = code.get('class', [])
        lang = normalize_class(classes)
        if lang:
            code['class'] = [f'language-{lang}']
            changed_any = True

    if not changed_any and not removed_old:
        return result

    # Add highlight.js to head
    head = soup.find('head')
    if head:
        # Add CSS
        css_link = soup.new_tag('link', rel='stylesheet', href=HLJS_CSS)
        head.append(css_link)
        # Add JS
        js_script = soup.new_tag('script', src=HLJS_JS)
        head.append(js_script)

    # Wrap bare <pre class="language-X"> (no nested <code>) with <code>
    for pre in soup.find_all('pre'):
        if not isinstance(pre, Tag): continue
        if pre.find('code'): continue  # already has code child
        classes = pre.get('class', [])
        lang_cls = [c for c in classes if c.startswith('language-')]
        if not lang_cls: continue
        # Wrap inner content with <code class="language-X">
        inner_html = pre.decode_contents()
        pre.clear()
        code = soup.new_tag('code', **{'class': lang_cls})
        code.append(BeautifulSoup(inner_html, 'lxml').body or '')
        # Actually use string content
        code.string = BeautifulSoup(inner_html, 'lxml').get_text()
        pre['class'] = []
        pre.append(code)

    # Add init script at end of body
    body = soup.find('body')
    if body:
        init_script = soup.new_tag('script')
        init_script.string = DRL_LANG_DEF + '\nhljs.highlightAll();'
        body.append(init_script)

    # Validate text content unchanged
    after_fp = get_text_fingerprint(soup)
    # Allow small differences (whitespace normalisation)
    if len(before_fp) > 0 and len(after_fp) < len(before_fp) * 0.8:
        result['error'] = f'Text shrunk too much: {len(before_fp)} -> {len(after_fp)}'
        return result

    if not dry_run:
        # Backup
        backup_dir.mkdir(parents=True, exist_ok=True)
        shutil.copy2(html_path, backup_dir / html_path.name)

        # Write updated HTML
        out = str(soup)
        if not out.startswith('<!DOCTYPE'): out = '<!DOCTYPE html>\n' + out
        html_path.write_text(out, encoding='utf-8')

    result['changed'] = True
    return result


def main():
    print(f'{"DRY RUN - " if DRY_RUN else ""}Processing Mark Proctor posts for syntax highlighting...', flush=True)

    backup_dir = BACKUP_DIR
    posts = sorted(LEGACY.glob('*.html'))
    posts = [p for p in posts if p.suffix == '.html' and not p.name.endswith('.bak')]

    changed_posts = []
    errors = []

    for i, html_path in enumerate(posts, 1):
        result = process_post(html_path, backup_dir, DRY_RUN)
        if result.get('error'):
            errors.append(result)
            print(f'  ERROR: {html_path.name}: {result["error"]}', flush=True)
        elif result['changed']:
            changed_posts.append(result)
            langs_str = ','.join(set(result['langs']))
            print(f'  ✓ {html_path.name} [{langs_str}] ({result["blocks"]} blocks)', flush=True)

        if i % 50 == 0:
            print(f'  Progress: {i}/{len(posts)}', flush=True)

    # Save change log
    log = {
        'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
        'dry_run': DRY_RUN,
        'total_posts': len(posts),
        'changed': len(changed_posts),
        'errors': len(errors),
        'changed_posts': changed_posts,
        'error_posts': errors,
    }
    if not DRY_RUN:
        CHANGE_LOG.write_text(json.dumps(log, indent=2))

    print(f'\n{"[DRY RUN] " if DRY_RUN else ""}Done.')
    print(f'  Changed: {len(changed_posts)} posts')
    print(f'  Errors:  {len(errors)} posts')
    print(f'  Backups: {backup_dir}')

    # Regenerate stale MD files
    if not DRY_RUN and changed_posts:
        print(f'\nRegenerating MD for {len(changed_posts)} changed posts...', flush=True)
        sys.path.insert(0, str(ROOT / 'scripts'))
        from convert_post import convert_post
        regen_count = 0
        for r in changed_posts:
            hp = Path(r['path'])
            md_path = MD_DIR / (hp.stem + '.md')
            if md_path.exists():
                try:
                    md = convert_post(hp)
                    md_path.write_text(md, encoding='utf-8')
                    regen_count += 1
                except Exception as e:
                    print(f'  MD regen failed for {hp.name}: {e}', flush=True)
        print(f'  Regenerated {regen_count} MD files')


if __name__ == '__main__':
    main()
