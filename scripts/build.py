#!/usr/bin/env python3
"""Build bilingual, dependency-free static pages. Run from any directory."""
from pathlib import Path
from html import escape
import json
import hashlib

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / 'public'
CONFIG = json.loads((ROOT / 'site.config.json').read_text())
EMAIL = CONFIG.get('contact_email', '') if CONFIG.get('contact_email_enabled') is True else ''
if EMAIL and (EMAIL.count('@') != 1 or any(c.isspace() for c in EMAIL) or any(c in EMAIL for c in '<>\"?&')):
    raise ValueError('Provide a valid contact email, or leave it empty.')

def write(path, text):
    p = PUBLIC / path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding='utf-8')

def sweater(color, edge):
    shape = 'M157 49 L119 61 L84 81 L30 196 L77 219 L111 153 L111 298 Q200 311 289 298 L289 153 L323 219 L370 196 L316 81 L281 61 L243 49 Q200 81 157 49Z'
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="400" height="340" viewBox="0 0 400 340" fill="none">
<defs><linearGradient id="yarn" x1="70" y1="90" x2="330" y2="290" gradientUnits="userSpaceOnUse"><stop stop-color="{color}"/><stop offset="1" stop-color="{edge}"/></linearGradient>
<pattern id="knit" width="8" height="10" patternUnits="userSpaceOnUse"><path d="M1 1L4 5L7 1M1 6L4 10L7 6" stroke="{edge}" opacity=".34" stroke-width=".7"/></pattern>
<pattern id="rib" width="5" height="7" patternUnits="userSpaceOnUse"><path d="M2 0V7" stroke="{edge}" stroke-width="1.3" opacity=".6"/></pattern>
<clipPath id="body"><path d="{shape}"/></clipPath></defs>
<ellipse cx="200" cy="319" rx="112" ry="7" fill="#19212A" opacity=".045"/>
<path d="{shape}" fill="url(#yarn)" stroke="{edge}" stroke-width="1.5" stroke-linejoin="round"/>
<g clip-path="url(#body)"><path d="{shape}" fill="url(#knit)"/>
<path d="M111 275Q200 288 289 275V306H111Z" fill="url(#rib)"/>
<g stroke="{edge}" stroke-width="1.5" opacity=".6">{''.join(f'<path d="M{x} 81 Q{x-10} 92 {x} 104 T{x} 127 T{x} 150 T{x} 173 T{x} 196 T{x} 219 T{x} 242 T{x} 265"/><path d="M{x+7} 81 Q{x+17} 92 {x+7} 104 T{x+7} 127 T{x+7} 150 T{x+7} 173 T{x+7} 196 T{x+7} 219 T{x+7} 242 T{x+7} 265"/>' for x in (137,173,216,252))}</g>
<path d="M119 62Q124 106 111 153M281 62Q276 106 289 153" stroke="{edge}" opacity=".7"/>
<path d="M30 196L77 219L85 203L38 180ZM323 219L370 196L362 180L315 203Z" fill="url(#rib)"/>
</g><path d="M157 49Q200 81 243 49L239 68Q200 101 161 68Z" fill="url(#rib)" stroke="{edge}" stroke-width="1.3"/>
<path d="M165 52Q200 75 235 52" stroke="{edge}" stroke-width="3" opacity=".7"/></svg>'''
for name, color, edge in [('base','#bbc7c3','#8a9d96'),('oat','#e4dac6','#bcad93'),('navy','#3d536a','#243a50')]:
    write(f'assets/knit-{name}.svg', sweater(color,edge))
write('assets/favicon.svg','<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="13" fill="#245C94"/><path d="M13 19L22 46L32 24L42 46L51 19" fill="none" stroke="white" stroke-width="5" stroke-linejoin="round"/></svg>')
write('assets/share-cover.svg','<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="630"><rect width="1200" height="630" fill="#f1f5f7"/><path d="M770 0V630M820 0V630M870 0V630M920 0V630M970 0V630M1020 0V630M1070 0V630M1120 0V630M720 100H1200M720 150H1200M720 200H1200M720 250H1200M720 300H1200M720 350H1200M720 400H1200M720 450H1200M720 500H1200" stroke="#cbd9e3"/><text x="80" y="270" font-family="Arial,sans-serif" font-size="88" font-weight="700" fill="#19212a">WeftWorks</text><text x="85" y="335" font-family="Arial,sans-serif" font-size="28" fill="#245c94">AI and digital transformation</text><text x="85" y="380" font-family="Arial,sans-serif" font-size="28" fill="#245c94">for apparel manufacturers and exporters</text></svg>')

COPY = {
'zh': {
'lang':'zh-CN','home':'/zh/','case':'/zh/cases/shengxuerong/','services':'服务','cases':'案例','approach':'合作方式','about':'关于我们','skip':'跳到正文','other':'English','otherlang':'en','studio':'面向服装制造与外贸出口企业','title':'服装制造与外贸出口企业的 AI 应用与数字化转型','heading':'服装企业的 AI 与<br><span>数字化转型</span>','intro':'WeftWorks 帮助服装工厂和外贸出口公司把 AI 用进日常业务。我们把买家邮件、样衣修改记录和生产进度按订单串起来，让业务员、跟单员和工厂从询盘到出货都能查到同一版要求。','cta':'看款式预览案例','secondary':'了解我们的服务','board':'款式预览示意','base':'基础款 · 雾绿','oat':'燕麦色','navy':'藏青色','keep':'同一版型，两种配色','note':'原创款式示意，非客户样衣','serviceTitle':'从买家询盘到装箱出货','serviceIntro':'围绕一张订单，看 AI 能帮团队整理哪些信息，哪些环节需要业务人员拍板。','servicesData':[('询盘与报价', '报价前，还要向买家确认什么？', 'AI 从买家邮件中提取数量、面料要求和交期，列出缺失的信息。业务员确认后，再交给核价同事。'),
 ('打样与改版', '下一版样衣到底要改哪里？', '把买家批注和参考图按款号整理成改版单，区分要改的细节和要保留的做法。设计师确认后，样衣房按同一版要求打样。'),
 ('生产跟单', '今天哪几张订单需要追进度？', '按订单对齐面辅料到货记录和工厂回报的进度，标出已过期但未完成的节点，方便跟单员和工厂商量下一步。'),
 ('出口单证', '出货前，装箱单和发票对得上吗？', '把订单、装箱单与发票草稿放在一起核对，标出款号、数量和箱数的差异，由单证员复核后出单。')],
'example':'业务场景示例','caseTitle':'圣雪绒｜从买家意见到打样要求','caseIntro':'在这套拟议方案中，AI 助手把海外买家的改色意见整理成改版单。业务员和设计师对照两种配色，再决定下一版样衣怎么做。','caseLink':'查看方案示意','badge':'外贸服装 · 方案示意','approachTitle':'从一张真实的<br>外贸订单开始','approachText':'我们跟着业务员、跟单员和工厂走完一张订单，找出哪些资料在反复录入、哪些修改容易漏传。先用你们手头的单据做小范围试用，跑通后再接入现有系统。','phases':['梳理交接环节', '用真实单据试跑', '接入现有流程'],'aboutTitle':'和做这张订单的人一起开发','aboutText':'Weft 是织物的纬线。我们的工程师和业务员、样衣房、生产计划员一起工作，把买家的第一封询盘邮件、工厂的进度表和出货时的装箱单按订单关联起来。','footer':'为服装制造与外贸出口企业提供 AI 应用和数字化转型服务。','contact':'聊聊你的流程','back':'首页 / 案例','caseH1':'圣雪绒｜把买家的改色意见变成款式预览','caseLead':'这套为圣雪绒规划的方案，聚焦外贸跟单中的一个决定：下一版样衣打哪个颜色？我们用一件示例针织衫，展示 AI 助手如何整理买家要求，以及业务员和设计师如何复核后再交给样衣房。','copy':'复制本页链接','copied':'链接已复制','copyFail':'请从浏览器地址栏复制本页链接。','step1':'接需求','step1text':'业务员选底稿，附上买家原话。','messageLabel':'示例买家留言','quote':'“领口和纹路照旧。想看看燕麦色和藏青色，下次对款时一起比较。”','step2':'拆要求','step2text':'Agent 提取要改和要保留的部分；信息不足时列出待问项。','sheet':'款式修改单','change':'修改','changeText':'颜色：燕麦色、藏青色','preserve':'保留','preserveText':'领口、针织纹路与版型','pending':'待确认','pendingText':'两种配色的确切色号','step3':'做预览','step3text':'按修改单，为同一版型准备两个候选配色，供下一次对款时比较。','a':'候选方案 A','b':'候选方案 B','step4':'人工复核','step4text':'设计师核对版型和纹路，业务员补齐色号，再决定发哪版。','designer':'设计师','designerText':'核对领口、版型与针织纹路。','sales':'业务员','salesText':'补齐确切色号，确认要发送的候选方案。','caution':'待确认：色号与最终方案。实物颜色以色卡或样衣为准。','boundary':'本页展示拟议流程和预先制作的示意图，不代表已上线系统或实际客户样衣。','returnServices':'了解其他业务场景','notfound':'这个页面还没有织好','notfoundText':'链接可能已更改。回到首页，从一项具体的工作开始。','homeLink':'返回首页'},
'en': {
'lang':'en','home':'/','case':'/cases/shengxuerong/','services':'Services','cases':'Case study','approach':'Our approach','about':'About','skip':'Skip to content','other':'中文','otherlang':'zh-CN','studio':'For apparel manufacturers and exporters','title':'AI and digital transformation for apparel manufacturers and exporters','heading':'AI and digital<br><span>transformation.</span>','intro':'We help garment factories and apparel exporters build AI into everyday operations. We connect buyer emails, sample revisions and production records so sales, sourcing and factory teams can follow the same order from inquiry to shipment.','cta':'Explore the style preview','secondary':'Explore our services','board':'Style preview concept','base':'Base style · Sage','oat':'Oatmeal','navy':'Navy','keep':'One silhouette. Two colorways.','note':'Original illustration, not a client sample','serviceTitle':'From inquiry to shipment','serviceIntro':'Four places where AI and better-connected records can help an apparel order move forward.','servicesData':[('Inquiries & costing',
  'What is missing from the buyer’s brief?',
  'AI extracts quantities, fabrics and delivery dates from buyer emails. Sales checks the open questions before costing the order.'),
 ('Sampling & revisions',
  'Which changes go into the next sample?',
  'Turn buyer comments and marked-up photos into a revision sheet for each style. The designer signs off on the changes before the sample room starts.'),
 ('Production tracking',
  'Which orders need a merchandiser’s attention?',
  'Match material arrivals and factory updates to each order. Flag missed milestones so the merchandiser can agree on next steps with the factory.'),
 ('Export documentation',
  'Do the shipment records match?',
  'Compare style numbers, quantities and carton counts across orders, packing lists and invoice drafts. The export team resolves differences before issuing the '
  'documents.')],
'example':'Illustrative business scenarios','caseTitle':'From buyer feedback to a sample brief','caseIntro':'Ningxia St.Edenweiss International Enterprises Group Co., Ltd. makes and exports cashmere apparel. In this proposed workflow, an AI assistant turns an overseas buyer’s color request into a revision sheet. Sales and design review two colorways before the next sample.','caseLink':'Explore the proposed workflow','badge':'Apparel export · Proposed workflow','approachTitle':'Start with one<br>export order.','approachText':'We follow an order with your merchandisers and factory team. Together we identify where details are retyped or lost, test a small tool on your own records, and connect it to the systems your team uses once the pilot works.','phases':['Map the handoffs', 'Pilot with real records', 'Connect the workflow'],'aboutTitle':'Built with the people behind each order','aboutText':'Weft is the crosswise thread in woven fabric. Our engineers work with merchandisers, sample rooms and factory planners to connect the records they rely on, from the buyer’s first email to the final packing list.','footer':'AI and digital transformation for apparel manufacturing and export.','contact':'Tell us about your workflow','back':'Home / Case study','caseH1':'St.Edenweiss Group | From a buyer’s color request to a style preview','caseLead':'We use a cashmere export scenario for Ningxia St.Edenweiss International Enterprises Group Co., Ltd. to illustrate one sampling decision: which colorway should the sample room make next? An AI assistant extracts the buyer’s instructions, then sales and design review what should go to the sample room.','copy':'Copy page link','copied':'Link copied','copyFail':'Please copy this page’s link from your browser’s address bar.','step1':'Receive the request','step1text':'The sales representative selects the base style and attaches the buyer’s original message.','messageLabel':'Illustrative buyer message','quote':'“Keep the neckline and knit pattern as they are. Could we see oatmeal and navy so we can compare them at our next style review?”','step2':'Clarify the changes','step2text':'The agent identifies what to change and what to preserve, then lists questions where information is missing.','sheet':'Style change sheet','change':'Change','changeText':'Color: oatmeal and navy','preserve':'Preserve','preserveText':'Neckline, knit pattern, and silhouette','pending':'To confirm','pendingText':'Exact color codes for both options','step3':'Prepare the previews','step3text':'Following the change sheet, prepare two color options in the same silhouette for the next review.','a':'Candidate A','b':'Candidate B','step4':'Review with the team','step4text':'The designer checks the silhouette and knit pattern. The sales representative confirms the color codes before deciding which version to send.','designer':'Designer','designerText':'Check the neckline, silhouette, and knit pattern.','sales':'Sales representative','salesText':'Confirm the exact color codes and the candidate to send.','caution':'Still to confirm: color codes and the final option. Refer to a physical color card or sample for the actual color.','boundary':'This page shows a proposed workflow and prepared illustrations. It does not represent a deployed system or actual client samples.','returnServices':'Explore other business scenarios','notfound':'This thread leads to a missing page','notfoundText':'The link may have changed. Return home and start with a task you know.','homeLink':'Back to home'}
}


# English is the default; explicit Chinese routes keep shared links predictable.
COPY['en'].update({
    'aboutPath':'/about/', 'aboutPageTitle':'About WeftWorks', 'menu':'Menu',
    'aboutH1':'An AI partner for<br><span>factories and exporters.</span>',
    'aboutLead':'WeftWorks is an independent AI and digital transformation studio for apparel manufacturers and export companies. We work alongside the people who quote, sample, make and ship each order.',
    'aboutMore':'Meet the studio', 'emailLabel':'Email', 'wechatLabel':'WeChat', 'wechatPending':'Planned · Please email us for now', 'contactTitle':'Where does an order slow down?',
    'contactText':'Bring a buyer inquiry, a sample revision or a production tracker. We’ll trace one handoff with you and identify what a first pilot could cover.',
    'conversation':'A direct conversation', 'principleTitle':'The people doing the work shape the tool.',
    'principles':[('Follow the order',
  'Sit with sales, merchandising and production as one order changes hands. Together we trace where information is entered twice or a buyer’s update gets missed.'),
 ('Use the records you have',
  'Start with buyer emails, style sheets and production trackers. Agree on the order and style numbers that connect them before choosing what to automate.'),
 ('Keep approvals explicit',
  'Let AI draft a revision sheet or flag conflicting quantities. Your designer approves the sample, and your export team signs off on the shipment documents.')],
    'fdeLabel':'Our approach to working together', 'fdeTitle':'Forward Deployed Engineering',
    'fdeText':'A Forward Deployed Engineer (FDE) works inside a customer’s workflow. For an apparel exporter, that could mean following a buyer’s revision from the merchandiser to the sample room, testing a tool on past orders, and refining it with the people who use it.',
    'fdeSteps':[
        ('Understand the work','Follow a real task with your team. Map the inputs, handoffs, and decisions that matter.'),
        ('Build alongside you','Turn one concrete need into a small tool. Review it with the people who will use it.'),
        ('Connect and refine','Decide what to integrate, document the workflow, and improve it as the team puts it to work.')],
    'deliverables':['A brief ready for costing', 'Approved sample revisions', 'An order exception list', 'A shipment discrepancy report']
})
COPY['zh'].update({
    'aboutPath':'/zh/about/', 'aboutPageTitle':'关于 WeftWorks', 'menu':'菜单',
    'aboutH1':'服装工厂与外贸企业的<br><span>AI 合作伙伴</span>',
    'aboutLead':'WeftWorks 是一家专注服装制造与外贸出口的 AI 与数字化转型工作室。我们和负责报价、打样、生产、出货的人一起梳理流程，把 AI 用在具体的业务环节里。',
    'aboutMore':'进一步了解我们', 'emailLabel':'电子邮箱', 'wechatLabel':'微信', 'wechatPending':'待开通 · 请先通过邮箱联系', 'contactTitle':'你们的订单，最常卡在哪一步？',
    'contactText':'可以从一封询盘邮件、一张改版单或一份生产进度表聊起。我们一起看一次交接，就能判断第一步值得试什么。',
    'conversation':'直接和做开发的人聊', 'principleTitle':'每天做这项工作的人，决定工具该怎么做。',
    'principles':[('跟着订单走', '和业务、跟单、生产同事一起走一遍订单，找出哪些资料要填两遍，买家后补的要求又是在哪一次交接时漏掉的。'),
 ('用好手头的资料', '从买家邮件、款式资料和生产进度表开始，先按订单号和款号理清对应关系，再决定哪些步骤适合自动化。'),
 ('把确认权留给团队', 'AI 可以起草改版单、标出数量差异。样衣由设计师确认，出货单证由单证员核对后签发。')],
    'fdeLabel':'我们的合作思路', 'fdeTitle':'FDE：把工程师带到业务现场',
    'fdeText':'FDE 是 Forward Deployed Engineer，即前线部署工程师。在服装外贸场景里，工程师会跟着一条买家修改意见，从跟单员走到样衣房，用历史订单试做工具，再和每天开单、打样的人一起调整。',
    'fdeSteps':[
        ('一起理解业务','跟完一笔真实工作，弄清资料从哪里来、交给谁，以及哪些判断最关键。'),
        ('一起做出工具','围绕一个具体需求做出小版本，让每天使用它的人参与试用与调整。'),
        ('一起接入与改进','确定需要接入的系统，留下清楚的流程说明，再随着实际使用继续完善。')],
    'deliverables':['可用于核价的询盘单', '经设计师确认的改版单', '需要跟进的订单清单', '出货单证差异清单']
})
WECHAT = CONFIG.get('contact_wechat', '')
WECHAT_PLANNED = CONFIG.get('contact_wechat_status') != 'active'

def image(name, alt, lazy=True):
    return f'<img src="/assets/knit-{name}.svg" width="400" height="340" alt="{escape(alt)}"{(" loading=\"lazy\"" if lazy else " fetchpriority=\"high\"")} decoding="async">'

def shell(c, kind, body):
    zh = c['lang']=='zh-CN'
    home, case = c['home'], c['case']
    alternate = COPY['en' if zh else 'zh']
    route_key = {'home':'home', 'case':'case', 'about':'aboutPath'}.get(kind, 'home')
    other = alternate[route_key]
    title = c['caseH1'] if kind=='case' else c['aboutPageTitle'] if kind=='about' else c['title']
    desc = c['caseLead'] if kind=='case' else c['aboutLead'] if kind=='about' else c['intro']
    css_version = hashlib.sha256((PUBLIC / 'assets/site.css').read_bytes()).hexdigest()[:10]
    js_version = hashlib.sha256((PUBLIC / 'assets/site.js').read_bytes()).hexdigest()[:10]
    contact = f'<div class="contact"><a href="mailto:{escape(EMAIL)}">{c["contact"]}</a><span>{escape(EMAIL)}</span></div>' if EMAIL else ''
    links = f'<a href="{home}#services">{c["services"]}</a><a href="{case}" {("aria-current=page" if kind=="case" else "")}>{c["cases"]}</a><a href="{c["aboutPath"]}" {("aria-current=page" if kind=="about" else "")}>{c["about"]}</a>'
    return f'''<!doctype html>
<html lang="{c['lang']}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{escape(title)} — WeftWorks</title><meta name="description" content="{escape(desc)}"><meta name="theme-color" content="#ffffff"><meta property="og:title" content="{escape(title)} — WeftWorks"><meta property="og:description" content="{escape(desc)}"><meta property="og:type" content="website"><meta property="og:locale" content="{'zh_CN' if zh else 'en_US'}"><meta property="og:image" content="/assets/share-cover.png"><meta name="twitter:card" content="summary_large_image"><link rel="alternate" hreflang="{c['otherlang']}" href="{other}"><link rel="icon" href="/assets/favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="/assets/site.css?v={css_version}"><script src="/assets/site.js?v={js_version}" defer></script></head>
<body><a class="skip" href="#main">{c['skip']}</a><header class="header"><div class="container nav"><a class="brand" href="{home}" aria-label="WeftWorks {'首页' if zh else 'home'}">WeftWorks<span class="brand-stitch" aria-hidden="true"></span></a><div class="nav-actions"><nav class="desktop-nav" aria-label="{'主导航' if zh else 'Main navigation'}">{links}</nav><details class="mobile-menu"><summary>{c['menu']}<span class="menu-icon" aria-hidden="true"></span></summary><nav aria-label="{'手机导航' if zh else 'Mobile navigation'}">{links}</nav></details><a class="language" href="{other}" lang="{c['otherlang']}" hreflang="{c['otherlang']}" data-language>{c['other']}</a></div></div></header>
{body}<footer class="footer container"><div><a class="brand" href="{home}">WeftWorks</a><p>{c['footer']}</p></div><div class="footer-right"><nav aria-label="{'页脚导航' if zh else 'Footer navigation'}"><a href="{home}#approach">{c['approach']}</a><a href="{c['aboutPath']}">{c['about']}</a></nav>{contact}<p class="copyright">© 2026 WeftWorks</p></div></footer></body></html>'''

def localized_write(locale, path, html):
    write(('zh/' if locale == 'zh' else '') + path, html)
    if locale == 'en':
        # Keep earlier /en/ links usable without a JavaScript redirect.
        write('en/' + path, html)

ICONS = [
    '<rect x="9" y="8" width="38" height="34" rx="3"/><path d="M9 19h38M18 27h12M18 34h21"/><circle cx="16" cy="14" r="1"/>',
    '<path d="M16 7l-7 4-5 12 7 3 4-7v19h26V19l4 7 7-3-5-12-7-4q-12 8-24 0Z"/>',
    '<path d="M8 12h40v31H8ZM8 22h40M8 32h40M22 12v31M35 12v31"/><path d="m25 27 3 3 5-6"/>',
    '<rect x="10" y="7" width="26" height="36" rx="3"/><path d="M17 16h12M17 23h9M17 30h8"/><circle cx="39" cy="33" r="11"/><path d="m34 33 4 4 7-8"/>'
]

for locale,c in COPY.items():
    rows=''.join(f'<article class="service-card service-{i}"><div class="service-card-top"><span class="service-icon" aria-hidden="true"><svg viewBox="0 0 56 50" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round" stroke-linecap="round">{ICONS[i]}</svg></span><p class="service-label">{label}</p></div><h3>{q}</h3><p class="service-answer">{answer}</p><p class="service-outcome">{c["deliverables"][i]}</p></article>' for i,(label,q,answer) in enumerate(c['servicesData']))
    board=f'''<figure class="workboard"><div class="board-top"><span>{c['board']}</span><span class="board-code">WW / KNIT</span></div><div class="board-base">{image('base',c['base'],False)}<span class="color-label"><i class="swatch sage"></i>{c['base']}</span></div><div class="board-options"><div>{image('oat',c['oat'],False)}<span class="color-label"><i class="swatch oat"></i>{c['oat']}</span></div><div>{image('navy',c['navy'],False)}<span class="color-label"><i class="swatch navy"></i>{c['navy']}</span></div></div><figcaption>{c['keep']}<small>{c['note']}</small></figcaption></figure>'''
    main=f'''<main id="main"><section class="hero container"><div class="hero-copy"><p class="eyebrow">{c['studio']}</p><h1>{c['heading']}</h1><p class="hero-intro">{c['intro']}</p><div class="hero-actions"><a class="button" href="{c['case']}">{c['cta']}</a><a class="text-link" href="#services">{c['secondary']}</a></div></div>{board}</section>
<section id="services" class="services container"><div class="section-heading"><div><p class="eyebrow">{c['services']}</p><h2>{c['serviceTitle']}</h2></div><p>{c['serviceIntro']}</p></div><div class="service-grid">{rows}</div><p class="section-note">{c['example']}</p></section>
<section class="container case-section"><a class="case-card" href="{c['case']}"><div class="case-copy"><p class="eyebrow">{c['badge']}</p><h2>{c['caseTitle']}</h2><p>{c['caseIntro']}</p><span class="text-link">{c['caseLink']}</span></div><div class="case-art" aria-hidden="true"><div>{image('oat','')}<span>{c['oat']}</span></div><div>{image('navy','')}<span>{c['navy']}</span></div></div></a></section>
<section id="approach" class="approach container"><div><p class="eyebrow">{c['approach']}</p><h2>{c['approachTitle']}</h2></div><div><p class="large-copy">{c['approachText']}</p><ul class="phases">{''.join(f'<li>{p}</li>' for p in c['phases'])}</ul></div></section>
<section id="about" class="about"><div class="container about-inner"><div class="weave" aria-hidden="true"></div><div><p class="eyebrow">Weft / {'纬线' if locale=='zh' else 'The crosswise thread'}</p><h2>{c['aboutTitle']}</h2><p>{c['aboutText']}</p><a class="text-link about-more" href="{c['aboutPath']}">{c['aboutMore']}</a></div></div></section></main>'''
    localized_write(locale,'index.html',shell(c,'home',main))
    def step(n,title,text,content):
        return f'<section class="step" id="step-{n}"><div class="step-heading"><span class="step-number">0{n}</span><div><h2>{title}</h2><p>{text}</p></div></div>{content}</section>'
    s1=f'''<div class="request-layout"><figure class="sample"><div>{image('base',c['base'])}</div><figcaption>{c['base']}<small>{c['note']}</small></figcaption></figure><blockquote><p class="eyebrow">{c['messageLabel']}</p><p>{c['quote']}</p></blockquote></div>'''
    s2=f'''<div class="change-sheet"><div class="sheet-title"><h3>{c['sheet']}</h3><span>KNIT / 01</span></div><dl>{''.join(f'<div><dt>{c[k]}</dt><dd>{c[k+"Text"]}</dd></div>' for k in ['change','preserve','pending'])}</dl></div>'''
    s3=f'''<div class="candidates">{''.join(f'<figure><div class="candidate-heading"><span>{c[key]}</span><span class="color-label"><i class="swatch {name}"></i>{c[name]}</span></div>{image(name,c[key]+" · "+c[name])}<figcaption>{c["note"]}</figcaption></figure>' for key,name in [('a','oat'),('b','navy')])}</div>'''
    s4=f'''<div class="review-roles"><div><h3>{c['designer']}</h3><p>{c['designerText']}</p></div><div><h3>{c['sales']}</h3><p>{c['salesText']}</p></div></div><p class="caution">{c['caution']}</p>'''
    main=f'''<main id="main" class="case-main container"><div class="case-intro"><a class="breadcrumb" href="{c['home']}">{c['back']}</a><p class="eyebrow case-badge">{c['badge']}</p><h1>{c['caseH1']}</h1><p class="case-lead">{c['caseLead']}</p><button class="copy-link" type="button" data-copy data-success="{c['copied']}" data-failure="{c['copyFail']}" hidden>{c['copy']}</button><p class="copy-status" role="status" aria-live="polite"></p></div>{step(1,c['step1'],c['step1text'],s1)}{step(2,c['step2'],c['step2text'],s2)}{step(3,c['step3'],c['step3text'],s3)}{step(4,c['step4'],c['step4text'],s4)}<div class="case-end"><p>{c['boundary']}</p><a class="button" href="{c['home']}#services">{c['returnServices']}</a></div></main>'''
    localized_write(locale,'cases/shengxuerong/index.html',shell(c,'case',main))
    principles = ''.join(f'<article class="about-principle"><h3>{title}</h3><p>{text}</p></article>' for title,text in c['principles'])
    fde_steps = ''.join(f'<article class="fde-step"><span class="thread-line" aria-hidden="true"></span><h3>{title}</h3><p>{text}</p></article>' for title,text in c['fdeSteps'])
    email_method = f'<div class="contact-method"><span>{c["emailLabel"]}</span><a class="contact-value" href="mailto:{escape(EMAIL)}">{escape(EMAIL)}</a></div>' if EMAIL else ''
    wechat_method = f'<div class="contact-method"><span>{c["wechatLabel"]}</span><p class="contact-value wechat-id">{escape(WECHAT)}</p>' + (f'<small>{c["wechatPending"]}</small>' if WECHAT_PLANNED else '') + '</div>' if WECHAT else ''
    about_body = f'''<main id="main" class="about-page"><section class="about-hero container"><div><p class="eyebrow">{c['aboutPageTitle']}</p><h1>{c['aboutH1']}</h1><p class="about-lead">{c['aboutLead']}</p></div><div class="about-thread" aria-hidden="true"><div class="thread-art"></div><span>WEFT / WORKS</span></div></section>
<section class="studio-story container"><div><p class="eyebrow">Weft / {'纬线' if locale=='zh' else 'The crosswise thread'}</p><h2>{c['aboutTitle']}</h2></div><p class="large-copy">{c['aboutText']}</p></section>
<section class="about-principles container"><h2>{c['principleTitle']}</h2><div>{principles}</div></section>
<section class="container" id="contact"><div class="contact-panel about-panel"><div><p class="eyebrow">{c['conversation']}</p><h2>{c['contactTitle']}</h2><p>{c['contactText']}</p></div><div class="contact-methods">{email_method}{wechat_method}</div></div></section>
<section id="fde" class="fde-section"><div class="container"><div class="fde-heading"><div><p class="eyebrow">{c['fdeLabel']}</p><h2>{c['fdeTitle']}</h2></div><p>{c['fdeText']}</p></div><div class="fde-steps">{fde_steps}</div></div></section></main>'''
    localized_write(locale, 'about/index.html', shell(c, 'about', about_body))
    err=f'<main id="main" class="container error"><p class="eyebrow">404</p><h1>{c["notfound"]}</h1><p>{c["notfoundText"]}</p><a class="button" href="{c["home"]}">{c["homeLink"]}</a></main>'
    localized_write(locale,'404.html',shell(c,'404',err).replace(f'<title>{escape(c["title"])} — WeftWorks</title>', '<title>404 — WeftWorks</title>').replace('<meta name="theme-color"', '<meta name="robots" content="noindex"><meta name="theme-color"'))
print('Built English-default site, Chinese pages, and compatible /en/ aliases.')
