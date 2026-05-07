#!/usr/bin/env python3
"""
Build HTML site from MADR ADR files.
Reads ADR markdown files from docs/, outputs to _site/ (compatible with GitHub Actions).
Assets copied to _site/assets/.
Dark/light theme via localStorage, defaults to dark.
"""

import re, json
from pathlib import Path
from datetime import datetime

DOCS_DIR = Path(__file__).parent / "docs"
SITE_DIR = Path(__file__).parent / "_site"
ASSETS_DIR = Path(__file__).parent / "assets"

THEME_TOGGLE = (
    '<button id="theme-toggle" aria-label="Toggle theme" '
    'onclick="toggleTheme()">&#9790;</button>'
)
THEME_SCRIPT = (
    '<script>'
    'function toggleTheme(){'
    'var b=document.body,d=b.classList.contains("dark");'
    'b.classList.toggle("dark");b.classList.toggle("light");'
    'var bg=d?"#0d1117":"#ffffff";'
    'b.style.setProperty("--bg",bg);'
    'document.documentElement.style.setProperty("--bg",bg);'
    'localStorage.setItem("theme",b.classList.contains("dark")?"dark":"light");'
    '}'
    'document.addEventListener("DOMContentLoaded",function(){'
    'var s=localStorage.getItem("theme");'
    'var isDark=s==="dark"||(!s&&window.matchMedia("(prefers-color-scheme:dark)").matches);'
    'var bg=isDark?"#0d1117":"#ffffff";'
    'if(isDark){document.body.className="dark"}else{document.body.className="light"}'
    'document.body.style.setProperty("--bg",bg);'
    'document.documentElement.style.setProperty("--bg",bg);'
    '});'
    '</script>'
)


def parse_frontmatter(content):
    match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
    if not match:
        return {}, content
    fm = {}
    for line in match.group(1).split('\n'):
        if ':' in line:
            k, v = line.split(':', 1)
            fm[k.strip()] = v.strip().strip('"').strip("'")
    return fm, content[len(match.group(0)):].strip()


def extract_sections(body):
    sections, cur = [], {'title': 'Context', 'level': 2, 'content': ''}
    for line in body.split('\n'):
        m = re.match(r'^(#{1,6})\s+(.*)', line)
        if m:
            if cur['content'].strip():
                sections.append(cur)
            cur = {'level': len(m.group(1)), 'title': m.group(2).strip(), 'content': ''}
        else:
            cur['content'] += line + '\n'
    if cur['content'].strip():
        sections.append(cur)
    return sections


def render(text):
    html = text

    # Wikilinks: [[slug]] or [[slug|Display Text]] → convert to proper links
    # Target is the wiki at https://regentribes.github.io/genesis-zero-bot-wiki/
    def wikilink(m):
        full = m.group(0)
        inner = m.group(1)
        if '|' in inner:
            slug, label = inner.split('|', 1)
        else:
            slug = inner
            label = inner
        slug = slug.strip()
        label = label.strip()
        # Determine path: sources/ for .md-style source refs, concepts/ for concept refs
        if slug.startswith('sources/'):
            path = slug.replace('sources/', '')
            url = f'../wiki/sources/{path}/'
        elif slug.startswith('concepts/'):
            path = slug.replace('concepts/', '')
            url = f'../wiki/concepts/{path}/'
        elif slug.startswith('adr-'):
            url = f'#{slug}'  # internal anchor, no prefix
        elif '/' not in slug:
            # bare slug — treat as sources/
            url = f'../wiki/sources/{slug}/'
        else:
            url = f'../wiki/{slug}.html'
        return f'<a href="{url}">{label}</a>'
    html = re.sub(r'\[\[([^\]]+)\]\]', wikilink, html)

    # Fenced code blocks
    html = re.sub(r'```(\w*)\n(.*?)```',
        '<pre><code class="language-\\1">\\2</code></pre>',
        html, flags=re.DOTALL)

    # Tables
    lines = html.split('\n')
    out, i = [], 0
    while i < len(lines):
        stripped = lines[i].strip()
        if stripped.startswith('|') and '|' in stripped:
            table_lines = []
            while i < len(lines) and lines[i].strip().startswith('|'):
                table_lines.append(lines[i])
                i += 1
            # Filter separator rows
            data_rows = [
                r for r in table_lines
                if not re.match(r'^\|[\s\-:]+(\|[\s\-:]+)+\|?$', r)
            ]
            if data_rows:
                headers = [h.strip() for h in data_rows[0].strip('|').split('|')]
                body_rows = [
                    [c.strip() for c in r.strip('|').split('|')]
                    for r in data_rows[1:]
                ]
                th = ''.join(f'<th>{h}</th>' for h in headers)
                tbody = ''.join(
                    '<tr>' + ''.join(f'<td>{c}</td>' for c in row) + '</tr>'
                    for row in body_rows
                )
                out.append(
                    f'<table class="md-table">'
                    f'<thead><tr>{th}</tr></thead>'
                    f'<tbody>{tbody}</tbody></table>'
                )
        else:
            out.append(lines[i])
            i += 1
    html = '\n'.join(out)

    # HR
    html = re.sub(r'^---+$', '<hr>', html, flags=re.MULTILINE)

    # Inline
    html = re.sub(r'`([^`]+)`', r'<code>\1</code>', html)
    html = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', html)
    html = re.sub(r'\*([^*]+)\*', r'<em>\1</em>', html)
    for lvl in [1, 2, 3, 4, 5]:
        html = re.sub(r'^' + '#' * lvl + r' (.*)',
                      f'<h{lvl}>\\1</h{lvl}>',
                      html, flags=re.MULTILINE)
    html = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', html)

    # Lists
    lines = html.split('\n')
    out, i = [], 0
    while i < len(lines):
        m = re.match(r'^(\s*)([-*]) (.+)', lines[i])
        if m:
            indent, first = m.group(1), m.group(3)
            items = [first]
            j = i + 1
            while j < len(lines):
                nm = re.match(r'^(\s*)([-*]) (.+)', lines[j])
                if not nm or nm.group(1) != indent:
                    break
                items.append(nm.group(3))
                j += 1
            out.append(indent + '<ul>' + ''.join(f'<li>{it}</li>' for it in items) + '</ul>')
            i = j
        else:
            out.append(lines[i]); i += 1
    html = '\n'.join(out)

    # Paragraphs
    html = re.sub(r'\n{2,}', '</p><p>', html)
    html = '<p>' + html + '</p>'
    for tag in ['h1','h2','h3','h4','h5','pre','ul','ol','blockquote','hr','table','div']:
        html = re.sub(rf'<p>(<{tag}[^>]*>)', r'\1', html)
        html = re.sub(rf'(</?{tag}[^>]*>)\s*</p>', r'\1', html)
    html = re.sub(r'<p>\s*</p>', '', html)
    return html


def html_escape(s):
    return (s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
            .replace('"', '&quot;'))


def make_base_html(title, heading_html, subtitle, main_content, footer_note):
    return (
        '<!DOCTYPE html>\n'
        '<html lang="en">\n'
        '<head>\n'
        '<meta charset="UTF-8">\n'
        '<meta name="viewport" content="width=device-width,initial-scale=1.0">\n'
        f'<title>{html_escape(title)}</title>\n'
        '<link rel="stylesheet" href="assets/style.css">\n'
        '<link rel="stylesheet" href="assets/adr.css">\n'
        '<style>html,body{--bg:#ffffff}body.dark,body:not(.light){--bg:#0d1117}</style>\n'
        '</head>\n'
        '<body class="dark">\n'
        '<header class="site-header">\n'
        '<div class="container">\n'
        '<div class="header-row">\n'
        f'{heading_html}\n'
        f'{THEME_TOGGLE}\n'
        '</div>\n'
        f'<p>{subtitle}</p>\n'
        '</div>\n'
        '</header>\n'
        '<main class="container">\n'
        f'{main_content}\n'
        '</main>\n'
        '<footer class="site-footer">\n'
        '<div class="container">\n'
        f'<p>{footer_note}</p>\n'
        '</div>\n'
        '</footer>\n'
        f'{THEME_SCRIPT}\n'
        '</body>\n'
        '</html>'
    )


def build_index_page(adrs):
    rows = []
    for a in sorted(adrs, key=lambda x: x['number']):
        num = str(a['number']).zfill(4)
        cls = a.get('status', '').lower().replace(' ', '-')
        rows.append(
            f'<tr>'
            f'<td><a href="adr-{num}.html">{num}</a></td>'
            f'<td><a href="adr-{num}.html">{html_escape(a.get("title",""))}</a></td>'
            f'<td><span class="status {cls}">{html_escape(a.get("status",""))}</span></td>'
            f'<td>{html_escape(a.get("date",""))}</td>'
            f'<td>{html_escape(a.get("domain",""))}</td>'
            f'</tr>'
        )
    rows_html = '\n'.join(rows)
    count = len(adrs)
    main = (
        '<section class="adr-table-section">\n'
        '<table class="adr-table">\n'
        '<thead><tr>'
        '<th>ADR</th><th>Title</th><th>Status</th><th>Date</th><th>Domain</th>'
        '</tr></thead>\n'
        f'<tbody>\n{rows_html}\n</tbody>\n'
        '</table>\n'
        '</section>'
    )
    footer = f'{count} ADRs &mdash; Generated {datetime.now().strftime("%Y-%m-%d %H:%M")}'
    heading = '<h1>RegenTribes ADRs</h1>'
    return make_base_html(
        'RegenTribes ADR Repository',
        heading,
        'Architecture Decision Records \u2014 MADR format, ASD-STE100',
        main,
        footer
    )


def build_adr_page(adr, sections):
    num = str(adr['number']).zfill(4)
    title = adr.get('title', 'Untitled')

    tags_html = ''
    if adr.get('tags'):
        tags_html = '<div class="adr-tags">' + ''.join(
            f'<span class="tag">{html_escape(t)}</span>'
            for t in adr.get('tags', [])
        ) + '</div>'

    sections_html = ''
    for sec in sections:
        lvl = sec['level']
        content = render(sec['content'])
        sections_html += (
            f'<div class="section">\n'
            f'<h{lvl}>{html_escape(sec["title"])}</h{lvl}>\n'
            f'{content}\n'
            f'</div>\n'
        )

    meta_items = []
    for key, label in [('status','Status'),('date','Date'),
                       ('domain','Domain'),('level','Level'),('authors','Authors')]:
        if adr.get(key):
            meta_items.append(
                f'<span><strong>{label}:</strong> {html_escape(str(adr[key]))}</span>'
            )
    meta_html = ' '.join(meta_items)

    status_cls = adr.get('status','').lower().replace(' ','-')
    status_html = f'<span class="status {status_cls}">{html_escape(adr.get("status",""))}</span>'

    main = (
        '<nav class="adr-nav"><a href="index.html">\u2190 All ADRs</a></nav>\n'
        '<article class="adr-article">\n'
        '<header class="adr-header">\n'
        f'<h1 class="adr-title-heading">ADR {num}: {html_escape(title)}</h1>\n'
        f'<div class="adr-meta">{status_html} {meta_html}</div>\n'
        f'{tags_html}\n'
        '</header>\n'
        f'{sections_html}\n'
        '</article>\n'
        '<nav class="adr-nav"><a href="index.html">\u2190 All ADRs</a></nav>'
    )

    footer = f'Generated {datetime.now().strftime("%Y-%m-%d %H:%M")}'
    heading = f'<h1><a href="index.html">RegenTribes ADRs</a></h1>'
    return make_base_html(
        f'ADR {num}: {title}',
        heading,
        'Architecture Decision Records \u2014 MADR format, ASD-STE100',
        main,
        footer
    )


def main():
    SITE_DIR.mkdir(exist_ok=True)
    adrs = []

    for fpath in sorted(DOCS_DIR.glob("????-*.md")):
        fm, body = parse_frontmatter(fpath.read_text())
        m = re.match(r'^(\d+)', fpath.stem)
        fm['number'] = int(m.group(1)) if m else 0
        sections = extract_sections(body)
        adrs.append(fm)

        html = build_adr_page(fm, sections)
        num_s = str(fm['number']).zfill(4)
        (SITE_DIR / f"adr-{num_s}.html").write_text(html)

    # Index
    (SITE_DIR / "index.html").write_text(build_index_page(adrs))

    # Assets
    assets_dir = SITE_DIR / "assets"
    assets_dir.mkdir(exist_ok=True)
    for asset in ASSETS_DIR.glob("*"):
        if asset.is_file():
            (assets_dir / asset.name).write_bytes(asset.read_bytes())

    # Manifest
    manifest = {
        'generated': datetime.now().isoformat(),
        'count': len(adrs),
        'format': 'MADR 3.0',
        'adrs': sorted([
            {
                'number': a['number'],
                'title': a.get('title',''),
                'status': a.get('status',''),
                'date': a.get('date',''),
                'domain': a.get('domain',''),
                'level': a.get('level',''),
                'authors': a.get('authors','').split(',') if a.get('authors') else [],
                'tags': a.get('tags',[]),
            }
            for a in adrs
        ], key=lambda x: x['number'])
    }
    (SITE_DIR / "manifest.json").write_text(json.dumps(manifest, indent=2))
    print(f"Built {len(adrs)} ADRs -> {SITE_DIR}")


if __name__ == "__main__":
    main()