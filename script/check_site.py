"""Check the generated Jekyll site using only the Python standard library."""
import json
import re
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote
import xml.etree.ElementTree as ET

ROOT = Path('_site')
class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.links = []
        self.has_main = False
        self.has_title = False
        self.lang = None
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'html': self.lang = attrs.get('lang')
        if tag == 'main': self.has_main = True
        if tag == 'title': self.has_title = True
        if tag in ('a', 'link') and attrs.get('href'): self.links.append(attrs['href'])
        if tag in ('img', 'script') and attrs.get('src'): self.links.append(attrs['src'])

errors = []
pages = list(ROOT.rglob('*.html'))
for path in pages:
    # Only theme-owned pages; legacy standalone utilities retain their own markup.
    raw = path.read_text()
    if 'assets/theme.css' not in raw: continue
    page = Page(); page.feed(raw)
    if not (page.lang == 'en' and page.has_main and page.has_title): errors.append(f'{path}: missing document landmarks')
    template_markup = re.sub(r'<pre\b[^>]*>.*?</pre>', '', raw, flags=re.S)
    if '{{' in template_markup or '{%' in template_markup: errors.append(f'{path}: unrendered Liquid outside code examples')
    for link in page.links:
        url = urlsplit(link)
        if url.scheme or url.netloc or not url.path: continue
        target = ROOT / unquote(url.path).lstrip('/') if url.path.startswith('/') else path.parent / unquote(url.path)
        if not target.exists(): errors.append(f'{path}: missing {link}')
posts = json.loads((ROOT / 'search.json').read_text())
assert len(posts) >= 19, f'Expected existing archive; found {len(posts)} posts'
assert any('max_block_size' in post['text'] for post in posts), 'Article body missing from search'
assert len({post['url'] for post in posts}) == len(posts), 'Duplicate article URL'
ET.parse(ROOT / 'feed.xml')
for route in ('index.html', 'posts/index.html', 'search/index.html', 'designs/index.html', '404.html'):
    assert (ROOT / route).exists(), f'Missing {route}'
if errors: raise SystemExit('\n'.join(errors))
print(f'PASS: {len(pages)} HTML pages inspected, {len(posts)} searchable articles, local links/assets, page landmarks, and RSS XML.')
