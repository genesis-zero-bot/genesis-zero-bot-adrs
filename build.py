#!/usr/bin/env python3
"""
Build HTML site from MADR ADR files.
Reads ADR markdown files from docs/, generates navigable HTML, outputs to _site/.
"""

import os
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
    """Very simple markdown renderer."""
    html = text
    # code blocks
    html = re.sub(r'```(\w*)\n(.*?)```', r'<pre><code class="\1">\2</code></pre>', html, flags=re.DOTALL)
    # inline code
    html = re.sub(r'`([^`]+)`', r'<code>\1</code>', html)
    # bold
    html = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', html)
    # italic
    html = re.sub(r'\*([^*]+)\*', r'<em>\1</em>', html)
    # headers
    html = re.sub(r'^#### (.*)', r'<h4>\1</h4>', html, flags=re.MULTILINE)
    html = re.sub(r'^### (.*)', r'<h3>\1</h3>', html, flags=re.MULTILINE)
    html = re.sub(r'^## (.*)', r'<h2>\1</h2>', html, flags=re.MULTILINE)
    # hr
    html = re.sub(r'^---$', '<hr>', html, flags=re.MULTILINE)
    # tables
    html = re.sub(r'\|([^|\n]+)\|\s*\|([\^v])\s*\|', r'<span class="status-arrow">\2</span>', html)
    # blockquotes
    html = re.sub(r'^> (.+)', r'<blockquote>\1</blockquote>', html, flags=re.MULTILINE)
    # links
    html = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', html)
    # lists
    lines = html.split('\n')
    result = []
    in_list = False
    for line in lines:
        if re.match(r'^[-*] ', line):
            if not in_list:
                result.append('<ul>')
                in_list = True
            result.append('<li>' + re.sub(r'^[-*] ', '', line) + '</li>')
        else:
            if in_list:
                result.append('</ul>')
                in_list = False
            result.append(line)
    html = '\n'.join(result)
    if in_list:
        html += '</ul>'
    # wrap paragraphs
    html = re.sub(r'\n\n+', '</p><p>', html)
    html = '<p>' + html + '</p>'
    html = re.sub(r'<p>\s*</p>', '', html)
    html = re.sub(r'<p>(<h[1-6]>)', r'\1', html)
    html = re.sub(r'(</h[1-6]>)\s*</p>', r'\1', html)
    html = re.sub(r'<p>(<pre>)', r'\1', html)
    html = re.sub(r'(</pre>)\s*</p>', r'\1', html)
    html = re.sub(r'<p>(<ul>)', r'\1', html)
    html = re.sub(r'(</ul>)\s*</p>', r'\1', html)
    html = re.sub(r'<p>(<blockquote>)', r'\1', html)
    html = re.sub(r'(</blockquote>)\s*</p>', r'\1', html)
    return html

def build_index(adrs):
    """Build index page with all ADRs."""
    rows = []
    for adr in sorted(adrs, key=lambda x: x['number']):
        num = str(adr['number']).zfill(4)
        status_class = adr['status'].lower()
        rows.append(f"""<tr class="adr-row">
            <td class="adr-num"><a href="adr-{num}.html">{num}</a></td>
            <td class="adr-title"><a href="adr-{num}.html">{adr.get('title', 'Untitled')}</a></td>
            <td class="adr-status"><span class="status {status_class}">{adr['status']}</span></td>
            <td class="adr-date">{adr.get('date', '')}</td>
            <td class="adr-domain">{adr.get('domain', '')}</td>
        </tr>""")
    return '\n'.join(rows)

def build_page(adr, sections):
    """Build single ADR page."""
    num = str(adr['number']).zfill(4)
    tags_html = ''
    if adr.get('tags'):
        tags_html = '<div class="adr-tags">'
        for tag in adr.get('tags', []):
            tags_html += f'<span class="tag">{tag}</span>'
        tags_html += '</div>'
    
    sections_html = ''
    for sec in sections:
        lvl = sec['level']
        title = sec['title']
        content = render_markdown(sec['content'])
        sections_html += f'<div class="section"><h{lvl}>{title}</h{lvl}>{content}</div>\n'
    
    nav = f"""<nav class="adr-nav">
        <a href="index.html">← All ADRs</a>
    </nav>"""
    
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
            <p>Architecture Decision Records — MADR format, ASD-STE100</p>
        </div>
    </header>
    <main class="container">
        {nav}
        <article class="adr-article">
            <header class="adr-header">
                <h1>ADR {num}: {adr.get('title', 'Untitled')}</h1>
                <div class="adr-meta">
                    <span class="status {adr.get('status', '').lower()}">{adr.get('status', '')}</span>
                    <span class="meta-date">{adr.get('date', '')}</span>
                    <span class="meta-domain">{adr.get('domain', '')}</span>
                    <span class="meta-level">level: {adr.get('level', '')}</span>
                </div>
                {tags_html}
            </header>
            {sections_html}
        </article>
        {nav}
    </main>
    <footer class="site-footer">
        <div class="container">
            <p>Generated {datetime.now().strftime('%Y-%m-%d')}</p>
        </div>
    </footer>
</body>
</html>"""

def main():
    SITE_DIR.mkdir(exist_ok=True)
    
    adrs = []
    doc_files = sorted(DOCS_DIR.glob("????-*.md"))
    
    for fpath in doc_files:
        content = fpath.read_text()
        fm, body = parse_frontmatter(content)
        
        if 'number' in fm:
            fm['number'] = int(fm['number'])
        else:
            m = re.match(r'^(\d+)', fpath.stem)
            fm['number'] = int(m.group(1)) if m else 0
        
        sections = extract_sections(body)
        adrs.append(fm)
        
        html = build_page(fm, sections)
        num = str(fm['number']).zfill(4)
        (SITE_DIR / f"adr-{num}.html").write_text(html)
    
    # Build index
    index_html = f"""<!DOCTYPE html>
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
            <p>Architecture Decision Records — MADR format, ASD-STE100</p>
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
                    {build_index(adrs)}
                </tbody>
            </table>
        </section>
    </main>
    <footer class="site-footer">
        <div class="container">
            <p>{len(adrs)} Architecture Decision Records — Generated {datetime.now().strftime('%Y-%m-%d')}</p>
        </div>
    </footer>
</body>
</html>"""
    
    (SITE_DIR / "index.html").write_text(index_html)
    
    # Copy assets
    for asset in ASSETS_DIR.glob("*"):
        if asset.is_file():
            (SITE_DIR / asset.name).write_bytes(asset.read_bytes())
    
    # Build manifest
    manifest = {
        'generated': datetime.now().isoformat(),
        'count': len(adrs),
        'adrs': [
            {
                'number': a['number'],
                'title': a.get('title', ''),
                'status': a.get('status', ''),
                'date': a.get('date', ''),
                'domain': a.get('domain', ''),
                'level': a.get('level', ''),
                'authors': a.get('authors', '').split(',') if a.get('authors') else [],
                'tags': a.get('tags', [])
            }
            for a in sorted(adrs, key=lambda x: x['number'])
        ]
    }
    (SITE_DIR / "manifest.json").write_text(json.dumps(manifest, indent=2))
    
    print(f"Built {len(adrs)} ADRs -> {SITE_DIR}")

if __name__ == "__main__":
    main()