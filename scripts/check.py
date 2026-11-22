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
assert len(pages)==12
for path,page in pages.items():
    assert page.h1==1 and page.title and page.desc,(path,'Headings/metadata')
    assert page.lang==('zh-CN' if 'zh' in path.relative_to(PUBLIC).parts else 'en'),path
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
    if not config['contact_email'] or not config['contact_email_enabled']: assert 'mailto:' not in html,path
    if 'about' in path.parts:
        assert 'tel:' not in html,path
        assert 'mailto:'+config['contact_email'] in html,path
        assert config['contact_wechat'] in html,path
        if config['contact_wechat_status'] == 'planned':
            assert ('待开通' if page.lang=='zh-CN' else 'Planned') in html,path
        assert 'Forward Deployed Engineer' in html,path
        assert ('/about/' if page.lang=='zh-CN' else '/zh/about/') in page.refs,path
    if 'cases' in path.parts:
        assert '/assets/polo-pattern-sheet.webp' in page.refs,path
        assert ('实物针织小样' if page.lang=='zh-CN' else 'knitted swatches') in html,path
        assert not any(ref.startswith('/assets/knit-') for ref in page.refs),path
print(f'PASS: {len(pages)} pages; languages, H1, metadata, local links, anchors, images, contact visibility, and case labels.')

assert pages[(PUBLIC/'index.html').resolve()].lang == 'en'
assert pages[(PUBLIC/'zh/index.html').resolve()].lang == 'zh-CN'
for prefix in ['', 'zh/', 'en/']:
    home = pages[(PUBLIC/prefix/'index.html').resolve()]
    assert ('/zh/about/' if prefix=='zh/' else '/about/') in home.refs
    assert ('/zh/cases/shengxuerong/' if prefix=='zh/' else '/cases/shengxuerong/') in home.refs
print('PASS: English default, About routes, language counterparts, email, proposed WeChat status, and FDE content.')
