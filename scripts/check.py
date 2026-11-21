#!/usr/bin/env python3
"""Check the deployable site using only Python's standard library."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote
import json

ROOT=Path(__file__).resolve().parents[1]
PUBLIC=ROOT/'public'
class Page(HTMLParser):
    def __init__(self, path):
        super().__init__(); self.path=path; self.ids=set(); self.refs=[]; self.h1=0; self.lang=''; self.title=False; self.desc=False
        self.feed(path.read_text())
    def handle_starttag(self, tag, attrs):
        a=dict(attrs)
        if a.get('id'): self.ids.add(a['id'])
        if tag=='html': self.lang=a.get('lang')
        if tag=='h1': self.h1+=1
        if tag=='title': self.title=True
        if tag=='meta' and a.get('name')=='description': self.desc=bool(a.get('content'))
        if tag=='img':
            assert 'alt' in a and a.get('width') and a.get('height'), (self.path,'Image accessibility/dimensions')
        for key in ['href','src']:
            if a.get(key): self.refs.append(a[key])
        if tag=='meta' and a.get('property')=='og:image': self.refs.append(a['content'])

pages={p.resolve():Page(p) for p in PUBLIC.rglob('*.html')}
assert len(pages)==6
for path,page in pages.items():
    assert page.h1==1 and page.title and page.desc,(path,'Headings/metadata')
    assert page.lang==('en' if 'en' in path.relative_to(PUBLIC).parts else 'zh-CN'),path
    for ref in page.refs:
        url=urlsplit(ref)
        if url.scheme or url.netloc: continue
        target=(PUBLIC/unquote(url.path.lstrip('/'))) if url.path.startswith('/') else path.parent/unquote(url.path)
        if not url.path: target=path
        if target.is_dir(): target=target/'index.html'
        assert target.is_file(),(path,ref,'Missing target')
        if url.fragment: assert url.fragment in pages[target.resolve()].ids,(path,ref,'Missing anchor')
    html=path.read_text()
    config=json.loads((ROOT/'site.config.json').read_text())
    if not config['contact_email'] or not config['contact_email_verified']: assert 'mailto:' not in html,path
    if 'cases' in path.parts:
        assert ('方案示意' if page.lang=='zh-CN' else 'Proposed workflow') in html
        assert ('非客户样衣' if page.lang=='zh-CN' else 'not a client sample') in html
print(f'PASS: {len(pages)} pages; languages, H1, metadata, local links, anchors, images, contact visibility, and case labels.')
