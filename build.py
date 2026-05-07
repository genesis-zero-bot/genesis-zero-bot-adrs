#!/usr/bin/env python3
"""
Build HTML site from MADR ADR files.
Reads ADR markdown files from docs/, generates navigable HTML, outputs to _site/.
"""

import re
import json
from pathlib import Path
from datetime import datetime

DOCS_DIR = Path(__file__).parent / "docs"
SITE_DIR = Path(__file__).parent / "_site"
ASSETS_DIR = Path(__file__).parent / "assets"


def parse_frontmatter(content):
    """Parse YAML frontmatter from markdown."""
    match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
    if not match:
        return {}, content
    fm = {}
    for line in match.group(1).split('\n'):
        if ':' in line:
            key, val = line.split(':', 1)
            fm[key.strip()] = val.strip().strip('"').strip("'")
    body = content[len(match.group(0)):].strip()
    return fm, body


def extract_sections(body):
    """Split body into sections by ## headings."""
    sections = []
    current = {'title': 'Context', 'level': 2, 'content': ''}
    for line in body.split('\n'):
        m = re.match(r'^(#{1,6})\s+(.*)', line)
        if m:
            if current['content'].strip():
                sections.append(current)
            current = {'level': len(m.group(1)), 'title': m.group(2).strip(), 'content': ''}
        else:
            current['content'] += line + '\n'
    if current['content'].strip():
        sections.append(current)
    return sections


def render_markdown(text):
    """GFM-compatible markdown renderer."""
    html = text

    # --- BLOCK LEVEL (process first) ---

    # Fenced code blocks
    html = re.sub(
        r'```(\w*)\n(.*?)```',
        r'<pre><code class="language-\1">\2</code></pre>',
        html, flags=re.DOTALL
    )

    # GFM tables — collect contiguous | lines
    def render_table(rows):
        """rows = list of markdown table rows (header + body, no separator)."""
        if not rows:
            return ''
        headers = [h.strip() for h in rows[0].strip('|').split('|')]
        body_rows = []
        for row in rows[1:]:
            cells = [c.strip() for c in row.strip('|').split('|')]
            body_rows.append(cells)
        th = ''.join(f'<th>{h}</th>' for h in headers)
        tbody = ''.join(
            '<tr>' + ''.join(f'<td>{c}</td>' for c in row) + '</tr>'
            for row in body_rows
        )
        return (
            f'<table class="md-table">'
            f'<thead><tr>{th}</tr></thead>'
            f'<tbody>{tbody}</tbody>'
            f'</table>'
        )

    lines = html.split('\n')
    out, i = [], 0
    while i < len(lines):
        stripped = lines[i].strip()
        if stripped.startswith('|') and '|' in stripped:
            table_rows = []
            while i < len(lines) and lines[i].strip().startswith('|'):
                table_rows.append(lines[i])
                i += 1
            # Filter out separator lines: |---|---|
            data_rows = [
                r for r in table_rows
                if not re.match(r'^\|[\s\-:]+(\|[\s\-:]+)+\|?$', r)
            ]
            out.append(render_table(data_rows))
        else:
            out.append(lines[i])
            i += 1
    html = '\n'.join(out)

    # Horizontal rule
    html = re.sub(r'^---+$', '<hr>', html, flags=re.MULTILINE)

    # --- INLINE LEVEL ---

    # Inline code
    html = re.sub(r'`([^`]+)`', r'<code>\1</code>', html)
    # Bold
    html = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', html)
    # Italic
    html = re.sub(r'\*([^*]+)\*', r'<em>\1</em>', html)
    # Headers
    html = re.sub(r'^##### (.*)', r'<h5>\1</h5>', html, flags=re.MULTILINE)
    html = re.sub(r'^#### (.*)', r'<h4>\1</h4>', html, flags=re.MULTILINE)
    html = re.sub(r'^### (.*)', r'<h3>\1</h3>', html, flags=re.MULTILINE)
    html = re.sub(r'^## (.*)', r'<h2>\1</h2>', html, flags=re.MULTILINE)
    html = re.sub(r'^# (.*)', r'<h1>\1</h1>', html, flags=re.MULTILINE)
    # Links
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
            out.append(
                indent + '<ul>' + ''.join(f'<li>{it}</li>' for it in items) + '</ul>'
            )
            i = j
        else:
            out.append(lines[i])
            i += 1
    html = '\n'.join(out)

    # Paragraphs
    html = re.sub(r'\n{2,}', '</p><p>', html)
    html = '<p>' + html + '</p>'

    # Strip <p> around block elements
    for tag in ['h1', 'h2', 'h3', 'h4', 'h5', 'pre', 'ul', 'ol',
                'blockquote', 'hr', 'table', 'div']:
        html = re.sub(rf'<p>(<{tag}[^>]*>)', r'\1', html)
        html = re.sub(rf'(</?{tag}[^>]*>)\s*</p>', r'\1', html)
    html = re.sub(r'<p>\s*</p>', '', html)

    return html


def build_index(adrs):
    rows = []
    for adr in sorted(adrs, key=lambda x: x['number']):
        num = str(adr['number']).zfill(4)
        cls = adr.get('status', '').lower().replace(' ', '-')
        rows.append(
            f'<tr class="adr-row">'
            f'<td class="adr-num"><a href="adr-{num}.html">{num}</a></td>'
            f'<td class="adr-title"><a href="adr-{num}.html">'
            f"{adr.get('title', 'Untitled')}</a></td>"
            f'<td class="adr-status"><span class="status {cls}">'
            f"{adr.get('status', '')}</span></td>"
            f'<td class="adr-date">{adr.get('date', '')}</td>'
            f'<td class="adr-domain">{adr.get('domain', '')}</td>'
            f'</tr>'
        )
    return '\n'.join(rows)


def build_page(adr, sections):
    num = str(adr['number']).zfill(4)
    tags_html = ''
    if adr.get('tags'):
        tags_html = '<div class="adr-tags">' + ''.join(
            f'<span class="tag">{t}</span>' for t in adr.get('tags', [])
        ) + '</div>'

    sections_html = ''
    for sec in sections:
        lvl = sec['level']
        content = render_markdown(sec['content'])
        sections_html += (
            f'<div class="section">'
            f'<h{lvl}>{sec["title"]}</h{lvl}>'
            f'{content}</div>\n'
        )

    nav = (
        '<nav class="adr-nav">'
        '<a href="index.html">&#8592; All ADRs</a>'
        '</nav>'
    )

    meta_items = []
    for key, label in [('status', 'Status'), ('date', 'Date'),
                       ('domain', 'Domain'), ('level', 'Level'),
                       ('authors', 'Authors')]:
        if adr.get(key):
            meta_items.append(
                f'<span class="meta-{key}"><strong>{label}:</strong> '
                f'{adr[key]}</span>'
            )

    status_cls = adr.get('status', '').lower().replace(' ', '-')

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ADR {num}: {adr.get('title', 'Untitled')}</title>
    <link rel="stylesheet" href="assets/adr.css">
    <link rel="stylesheet" href="assets/style.css">
</head>
<body>
    <header class="site-header">
        <div class="container">
            <h1><a href="index.html">RegenTribes ADRs</a></h1>
            <p>Architecture Decision Records &mdash; MADR format, ASD-STE100</p>
        </div>
    </header>
    <main class="container">
        {nav}
        <article class="adr-article">
            <header class="adr-header">
                <h1 class="adr-title-heading">ADR {num}: {adr.get('title', 'Untitled')}</h1>
                <div class="adr-meta">
                    <span class="status {status_cls}">{adr.get('status', '')}</span>
                    {' '.join(meta_items)}
                </div>
                {tags_html}
            </header>
            {sections_html}
        </article>
        {nav}
    </main>
    <footer class="site-footer">
        <div class="container">
            <p>Generated {datetime.now().strftime('%Y-%m-%d %H:%M')}</p>
        </div>
    </footer>
</body>
</html>"""


def build_index_page(adrs):
    rows = build_index(adrs)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>RegenTribes ADR Repository</title>
    <link rel="stylesheet" href="assets/adr.css">
    <link rel="stylesheet" href="assets/style.css">
</head>
<body>
    <header class="site-header">
        <div class="container">
            <h1>RegenTribes ADRs</h1>
            <p>Architecture Decision Records &mdash; MADR format, ASD-STE100</p>
        </div>
    </header>
    <main class="container">
        <section class="adr-table-section">
            <table class="adr-table">
                <thead>
                    <tr>
                        <th>ADR</th>
                        <th>Title</th>
                        <th>Status</th>
                        <th>Date</th>
                        <th>Domain</th>
                    </tr>
                </thead>
                <tbody>
                    {rows}
                </tbody>
            </table>
        </section>
    </main>
    <footer class="site-footer">
        <div class="container">
            <p>{len(adrs)} Architecture Decision Records &mdash; Generated {datetime.now().strftime('%Y-%m-%d %H:%M')}</p>
        </div>
    </footer>
</body>
</html>"""


def main():
    SITE_DIR.mkdir(exist_ok=True)
    adrs = []

    for fpath in sorted(DOCS_DIR.glob("????-*.md")):
        content = fpath.read_text()
        fm, body = parse_frontmatter(content)

        m = re.match(r'^(\d+)', fpath.stem)
        fm['number'] = int(m.group(1)) if m else 0

        sections = extract_sections(body)
        adrs.append(fm)

        html = build_page(fm, sections)
        num = str(fm['number']).zfill(4)
        (SITE_DIR / f"adr-{num}.html").write_text(html)

    # Index page
    (SITE_DIR / "index.html").write_text(build_index_page(adrs))

    # Assets
    for asset in ASSETS_DIR.glob("*"):
        if asset.is_file():
            (SITE_DIR / asset.name).write_bytes(asset.read_bytes())

    # Manifest
    manifest = {
        'generated': datetime.now().isoformat(),
        'count': len(adrs),
        'format': 'MADR 3.0',
        'adrs': sorted([
            {
                'number': a['number'],
                'title': a.get('title', ''),
                'status': a.get('status', ''),
                'date': a.get('date', ''),
                'domain': a.get('domain', ''),
                'level': a.get('level', ''),
                'authors': a.get('authors', '').split(',') if a.get('authors') else [],
                'tags': a.get('tags', []),
            }
            for a in adrs
        ], key=lambda x: x['number'])
    }
    (SITE_DIR / "manifest.json").write_text(json.dumps(manifest, indent=2))

    print(f"Built {len(adrs)} ADRs -> {SITE_DIR}")


if __name__ == "__main__":
    main()
