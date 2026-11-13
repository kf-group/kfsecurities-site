import json, os, re, html, datetime
E=html.escape
BASE='https://www.kfsecurities.com'
def slug(x): return re.sub(r'[^a-z0-9]+','-',x.lower()).strip('-')
SITEMAP=[]
OUT='site'
LEGAL="KF Securities Private Limited"; GST="32AAFCK3475R2ZZ"
REG="Puthuval Purayidom, Thumba, Pallithura P.O., Thiruvananthapuram, Kerala 695586, India"
OFFICE="Al-Falah Towers, Kazhakkoottam – Menamkulam Road, Kazhakkoottam, Thiruvananthapuram, Kerala 695582, India"
RISK="Mutual fund investments are subject to market risks, read all scheme related documents carefully."
import shutil
# ---- prepare output folder ----
shutil.rmtree(OUT,ignore_errors=True); shutil.copytree('src/assets',OUT+'/assets'); os.makedirs(OUT+'/data',exist_ok=True)
open(OUT+'/CNAME','w').write('www.kfsecurities.com\n')
# ---- services: KF Ledger catalogue + website settings ----
CAT=json.load(open('data/catalog.json')); SITE=json.load(open('data/site.json'))
hide=set(SITE.get('hide_services',[])); cats=[]
for lc in CAT['categories']:
    sv=[x['name'] for x in CAT['services'] if x['category_id']==lc['id'] and x['id'] not in hide]
    if not sv: continue
    o=SITE.get('categories',{}).get(lc['id'],{})
    cats.append({"id":lc['id'],"name":o.get('name',lc['name']),"blurb":o.get('blurb',lc['name']+' handled end to end by KF Securities.'),"services":sv})
for x in SITE.get('extra_categories',[]):
    if x.get('services') and x['id'] not in [c['id'] for c in cats]: cats.append(dict(x))
order=SITE.get('order',[]); cats.sort(key=lambda c: order.index(c['id']) if c['id'] in order else len(order))
json.dump(cats,open(OUT+'/data/services.json','w'),ensure_ascii=False)
NSV=sum(len(c['services']) for c in cats); NSVT=f'{NSV//10*10}+' if NSV>=20 else str(NSV)
for c in cats: c['slug']=slug(c['name'])
ORG={"@context":"https://schema.org","@type":["ProfessionalService","FinancialService","LocalBusiness"],"@id":BASE+"/#org","name":"KF securities","legalName":LEGAL,"url":BASE+"/","logo":BASE+"/assets/kfs-logo.png","image":BASE+"/assets/kfs-logo.png","foundingDate":"2013",
 "telephone":"+91-9633444704","email":"social@kfsecurities.com","taxID":GST,"priceRange":"₹₹",
 "address":{"@type":"PostalAddress","streetAddress":"Al-Falah Towers, Kazhakkoottam – Menamkulam Road, Kazhakkoottam","addressLocality":"Thiruvananthapuram","addressRegion":"Kerala","postalCode":"695582","addressCountry":"IN"},
 "areaServed":{"@type":"Country","name":"India"},"sameAs":["https://www.linkedin.com/company/kf-securities"],
 "hasOfferCatalog":{"@type":"OfferCatalog","name":"Services","itemListElement":[{"@type":"OfferCatalog","name":c["name"],"itemListElement":[{"@type":"Offer","itemOffered":{"@type":"Service","name":x}} for x in c["services"]]} for c in cats]}}
ORG_LITE={k:v for k,v in ORG.items() if k!='hasOfferCatalog'}

def head(title,desc,active='',canon='/',ld=None):
    nav=[('/services','Services','services'),('/compliance','Compliance plans','compliance'),('/investments','Investments','investments'),('/pay','Pay','pay'),('/contact','Contact','contact')]
    links=''.join(f'<a href="{h}" class="{"active" if k==active else ""}">{t}</a>' for h,t,k in nav)
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title><meta name="description" content="{desc}"><meta property="og:title" content="{title}"><meta property="og:description" content="{desc}"><meta property="og:type" content="website"><meta property="og:url" content="{BASE}{canon}"><meta property="og:image" content="{BASE}/assets/kfs-logo.png"><meta property="og:site_name" content="KF securities"><meta property="og:locale" content="en_IN"><meta name="twitter:card" content="summary"><link rel="canonical" href="{BASE}{canon}"><meta name="robots" content="index,follow,max-image-preview:large"><meta name="theme-color" content="#0B2545">{LD(canon,ld)}
<link rel="icon" href="/assets/favicon.png"><link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Anton&family=Source+Sans+3:wght@400;600;700;800&display=swap" rel="stylesheet"><link rel="stylesheet" href="/assets/style.css"></head>
<body style="font-family:'Source Sans 3',system-ui,sans-serif">
<div class="top"><div class="wrap"><span>Investments · Company compliance · Legal &amp; IP · Across India since 2013</span><span>Call / WhatsApp <a href="tel:+919633444704">96334 44704</a></span></div></div>
<header class="site"><div class="wrap"><a href="/" style="text-decoration:none"><img src="/assets/kfs-logo.png" alt="KF securities" style="height:44px;width:auto"></a>
<nav class="main">{links}<a class="btn y sm basket" href="/request">Request a quote<span class="hidden"><span class="basket-n">0</span></span></a></nav><button class="menu-btn" aria-label="Menu">☰</button></div></header>
'''
FOOT=f'''<div class="cta"><div class="wrap"><div><h2>One trusted desk</h2><div style="font-weight:700;color:#071A33">Tax, compliance, legal and investments, handled by one team.</div></div><div class="nums" style="color:#0B2545">96334 44704</div><a class="btn n" data-wa="Hi KF Securities, I would like some help.">WhatsApp us</a></div></div>
<footer class="site"><div class="wrap"><div class="cols">
<div><h4>KF securities</h4><p>Financial and business services brand of {LEGAL}, part of KF Group. In business since 2013.</p><p style="margin-top:10px">GSTIN {GST}</p></div>
<div><h4>Services</h4><ul>{''.join(f'<li><a href="/services/{c["slug"]}">{c["name"]}</a></li>' for c in cats)}</ul></div>
<div><h4>Company</h4><ul><li><a href="/compliance">Compliance plans</a></li><li><a href="/investments">Investments</a></li><li><a href="/pay">Pay a quote or invoice</a></li><li><a href="/contact">Contact</a></li></ul></div>
<div><h4>Contact</h4><p><b>Registered office:</b> {REG}</p><p style="margin-top:8px"><b>Office:</b> {OFFICE}</p><p style="margin-top:8px"><a href="tel:+919633444704">+91 96334 44704</a><br><a href="mailto:social@kfsecurities.com">social@kfsecurities.com</a></p></div>
</div><div class="legal"><span>© 2026 {LEGAL}. All rights reserved.</span><span><a href="/refund-policy">Refunds &amp; cancellations</a> · <a href="/terms">Terms</a> · <a href="/privacy-policy">Privacy</a> · <a href="/disclaimer">Disclaimer</a></span></div></div></footer>
<a class="wa-float" data-wa="Hi KF Securities, I would like some help.">WhatsApp</a>
<script src="/assets/config.js"></script><script src="https://cdnjs.cloudflare.com/ajax/libs/qrcodejs/1.0.0/qrcode.min.js"></script><script src="https://checkout.razorpay.com/v1/checkout.js" defer></script><script src="/assets/app.js"></script></body></html>'''
def LD(canon,ld):
    base=[ORG if canon in ('/','/services') else ORG_LITE]+([ld] if isinstance(ld,dict) else (ld or []))
    return ''.join('<script type="application/ld+json">'+json.dumps(x,ensure_ascii=False)+'</script>' for x in base)
def page(p,t,d,b,a='',ld=None,pri='0.6'):
    fn=os.path.join(OUT,p); os.makedirs(os.path.dirname(fn) or '.',exist_ok=True)
    canon='/' if p=='index.html' else '/'+p[:-5]
    open(fn,'w').write(head(t,d,a,canon,ld)+b+FOOT); SITEMAP.append((canon,pri))
def ico(p): return f'<div class="ico"><svg viewBox="0 0 24 24">{p}</svg></div>'
IC={'SC-1':'<path d="M3 21h18M5 21V8l7-5 7 5v13M9 21v-6h6v6"/>','TAX':'<path d="M4 4h16v16H4zM8 9h8M8 13h8M8 17h5"/>','SC-2':'<path d="M12 3l8 4v6c0 4-3.5 7-8 8-4.5-1-8-4-8-8V7z"/>','SC-3':'<circle cx="9" cy="8" r="3"/><path d="M3 20c0-3 3-5 6-5s6 2 6 5M17 11h4M19 9v4"/>','SC-4':'<path d="M6 3h12v18l-3-2-3 2-3-2-3 2zM9 8h6M9 12h6"/>','SC-5':'<rect x="4" y="5" width="16" height="14" rx="2"/><path d="M8 10h8M8 14h5"/>','SC-6':'<path d="M7 3h7l5 5v13H7zM14 3v5h5M10 13h6M10 17h6"/>','SC-7':'<circle cx="12" cy="12" r="9"/><path d="M15 9.5a3 3 0 1 0 0 5"/>'}

cards=''.join(f'<a class="card {"a" if i%2 else ""}" href="/services/{c["slug"]}" style="color:inherit;text-decoration:none">{ico(IC.get(c["id"],IC["SC-6"]))}<h3>{c["name"]}</h3><p>{c["blurb"]}</p><span class="go">{len(c["services"])} services →</span></a>' for i,c in enumerate(cats))
home=f'''<section class="hero"><div class="wrap grid"><div><div class="eyebrow">Investments · Compliance · Legal &amp; IP</div>
<h1>One <span>trusted</span> desk</h1><p class="lead">Company setup, GST, income tax, payroll, ROC and RBI compliance, legal documents, trademarks and investments, for businesses and families across India since 2013.</p>
<div class="chips"><span class="chip">Mutual Funds</span><span class="chip">Demat &amp; Trading</span><span class="chip">Company Setup</span><span class="chip">GST &amp; Tax</span><span class="chip y">Legal &amp; IP</span></div>
<div class="btns"><a class="btn y" href="/services">Browse {NSVT} services</a><a class="btn o" href="/compliance">Monthly compliance plans</a></div></div>
<div class="finder"><h3>What do you need?</h3><label>Search a service</label><input id="h-q" placeholder="GST registration, trademark, ITR…" onkeydown="if(event.key==='Enter')location.href='/services?q='+encodeURIComponent(this.value)">
<button class="btn n" style="width:100%;margin-top:14px" onclick="location.href='/services?q='+encodeURIComponent(document.getElementById('h-q').value)">Find service</button>
<p class="note" style="margin-top:12px">Not sure what applies to you? <a data-wa="Hi KF Securities, I need advice on what my business needs.">Ask our desk on WhatsApp</a>.</p></div></div></section>
<section><div class="wrap"><div class="eyebrow b">Services</div><h2>Everything your business <span>files, signs and registers</span></h2><p class="sub">Pick the services you need, get one written quote, and pay online. Legal and tax work is done with our partner advocates and chartered accountants where required.</p><div class="grid4">{cards}</div></div></section>
<section class="alt"><div class="wrap"><div class="eyebrow b">How it works</div><h2>Quote to done in <span>four steps</span></h2><div class="steps">
<div class="step"><h4>Choose services</h4><p>Add what you need to your quote request, or describe it.</p></div>
<div class="step"><h4>Get a written quote</h4><p>Fixed fee, timeline and document list on WhatsApp or email.</p></div>
<div class="step"><h4>Pay online</h4><p>Pay against your quote number by UPI, card or netbanking.</p></div>
<div class="step"><h4>We file &amp; update you</h4><p>Track progress with one desk until it is done.</p></div></div></div></section>
<section><div class="wrap grid3" style="margin-top:0">
<div class="card a"><h3>Compliance plans</h3><p>GST, income tax, TDS, ROC, payroll and licence reminders in one monthly plan.</p><a class="go" href="/compliance">See plans →</a></div>
<div class="card"><h3>Investments</h3><p>Mutual funds and demat &amp; trading accounts, set up and serviced by our team.</p><a class="go" href="/investments">Learn more →</a></div>
<div class="card r"><h3>Already have a quote?</h3><p>Pay your quote or invoice online with its reference number.</p><a class="go" href="/pay">Pay now →</a></div></div></section>'''
page('index.html','KF securities | Company compliance, tax, legal & investments','KF Securities: company setup, GST, income tax, payroll, ROC & RBI compliance, legal documentation, trademarks and investments. Across India since 2013.',home)

svc='''<div class="page-hero"><div class="wrap"><div class="eyebrow">Services</div><h1>Pick what you need</h1><p>Add services to your quote request. We reply with one written quote: fixed fee, timeline and the documents we need.</p></div></div>
<section style="padding-top:20px"><div class="wrap"><div class="filters"><div><label>Category</label><select id="s-cat"></select></div><div><label>Search</label><input id="s-q" placeholder="e.g. GST, trademark, agreement"></div><div style="flex:0"><a class="btn y basket" href="/request" style="white-space:nowrap">View quote request<span class="hidden"><span class="basket-n">0</span></span></a></div></div>
<div class="count" id="s-count"></div><div id="svc"></div></div></section>
<script>(function(){var q=new URLSearchParams(location.search).get('q');if(q)document.addEventListener('DOMContentLoaded',function(){var i=document.getElementById('s-q');i.value=q;i.dispatchEvent(new Event('input'))});})();</script>'''
page('services.html','Services | KF securities',f'{NSVT} services: company setup, ROC & RBI compliance, GST, income tax, payroll, registrations, legal documentation and trademark & IP.',svc,'services')

req='''<div class="page-hero"><div class="wrap"><div class="eyebrow">Quote request</div><h1>Request a quote</h1><p>Free and with no obligation. We reply with a written quote.</p></div></div>
<div class="wrap" id="req"><div class="co"><div class="panel"><h3>Services selected</h3><div id="req-list" style="display:grid;gap:8px;margin-top:10px"></div><a href="/services" class="note" style="display:inline-block;margin-top:10px">+ Add more services</a></div>
<div class="panel"><form id="req-form"><h3>Your details</h3>
<label>Anything else we should know?</label><textarea name="details" rows="3" placeholder="Type of entity, turnover, deadlines, number of employees…"></textarea>
<div class="row2"><div><label>Name</label><input name="name" required></div><div><label>Business name</label><input name="business"></div></div>
<div class="row2"><div><label>Mobile / WhatsApp</label><input name="phone" required></div><div><label>City</label><input name="city"></div></div>
<label>Email</label><input name="email" type="email">
<button class="btn y" style="width:100%;margin-top:16px">Get my quote</button></form><div id="req-done" class="hidden"></div></div></div></div>'''
page('request.html','Request a quote | KF securities','Request a written quote for company, tax, compliance, legal and IP services.',req)

payp='''<div class="page-hero"><div class="wrap"><div class="eyebrow">Payments</div><h1>Pay a quote or invoice</h1><p>Pay online against your KF Securities quote or invoice number.</p></div></div>
<div class="wrap"><div class="co"><div class="panel"><form id="pay-form"><h3>Payment details</h3>
<label>Quote or invoice number</label><input name="quote" required placeholder="e.g. KFS-261114-AB12 or invoice no.">
<label>Amount (₹)</label><input name="amount" type="number" min="1" required>
<div class="row2"><div><label>Name</label><input name="name" required></div><div><label>Mobile</label><input name="phone" required></div></div>
<label style="display:flex;gap:8px;align-items:flex-start;font-weight:600;color:var(--ink)"><input type="checkbox" required style="width:auto;margin-top:4px">I agree to the <a href="/terms" target="_blank">terms</a> and the <a href="/refund-policy" target="_blank">refund policy</a>.</label>
<button class="btn y" style="width:100%;margin-top:16px">Continue to pay</button><div id="pay-off" class="warn hidden">Online payment is being set up; you can still send your payment request and we will share the payment details.</div></form><div id="pay-step"></div></div>
<aside class="panel"><h3>Good to know</h3><ul class="lst" style="margin-top:10px"><li>Pay only the amount in your written quote or invoice.</li><li>Government fees (stamp duty, MCA, IP office fees) are shown separately in your quote.</li><li>You get a GST invoice for our professional fees.</li><li>Questions? WhatsApp <a href="tel:+919633444704">96334 44704</a>.</li></ul></aside></div></div>'''
page('pay.html','Pay online | KF securities','Pay your KF Securities quote or invoice online by UPI, card or netbanking.',payp,'pay')

comp=f'''<div class="page-hero"><div class="wrap"><div class="eyebrow">Compliance plans</div><h1>Stay compliant every month</h1><p>One monthly plan, one desk, no missed deadlines. Plans are priced on your entity type, turnover and headcount.</p></div></div>
<section><div class="wrap"><div class="grid3" style="margin-top:0">
<div class="card pk a"><h3>Compliance Basic</h3><p>For proprietors and small firms.</p><ul><li>GST returns</li><li>Income tax and TDS</li><li>Licence and renewal reminders</li></ul><a class="btn n" style="margin-top:16px" href="/request?add=Compliance%20Basic%20plan">Get a quote</a></div>
<div class="card pk"><h3>Compliance Standard</h3><p>For private limited companies and LLPs.</p><ul><li>Everything in Basic</li><li>ROC and secretarial filings</li><li>Payroll, PF and ESI</li></ul><a class="btn n" style="margin-top:16px" href="/request?add=Compliance%20Standard%20plan">Get a quote</a></div>
<div class="card pk r"><h3>Compliance Premium</h3><p>For growing and regulated businesses.</p><ul><li>Everything in Standard</li><li>State labour and shop laws</li><li>Sector regulator filings (incl. RBI/FEMA)</li></ul><a class="btn n" style="margin-top:16px" href="/request?add=Compliance%20Premium%20plan">Get a quote</a></div></div></div></section>'''
page('compliance.html','Monthly compliance plans | KF securities','Monthly compliance plans covering GST, income tax, TDS, ROC, payroll, PF/ESI and licences.',comp,'compliance')

inv=f'''<div class="page-hero"><div class="wrap"><div class="eyebrow">Investments</div><h1>Invest with a team you can call</h1><p>Mutual fund investments and demat &amp; trading accounts, set up and serviced by KF Securities through our authorised partnership with a SEBI-registered stockbroker.</p></div></div>
<section><div class="wrap"><div class="grid3" style="margin-top:0">
<div class="card a"><h3>Mutual funds</h3><p>SIPs and lump-sum investments in mutual fund schemes, with help on KYC, nominations, statements and tax reports.</p></div>
<div class="card"><h3>Demat &amp; trading account</h3><p>Open a demat and trading account and get service support for transfers, pledges and corporate actions.</p></div>
<div class="card r"><h3>Tax reporting</h3><p>Capital gains statements and mutual fund tax reporting for your income tax return.</p></div></div>
<div class="risk"><b>{RISK}</b> KF Securities does not give individual stock recommendations or guarantee returns. Past performance is not an indicator of future returns.</div><p class="arn note"></p>
<form class="panel" data-request="Investment enquiry" data-kind="investment" style="max-width:760px;margin-top:30px"><h3>Talk to our team</h3>
<div class="row2"><div><label>Name</label><input name="Name" required></div><div><label>Mobile</label><input name="Mobile" required></div></div>
<label>I'm interested in</label><select name="Interest"><option>Mutual funds / SIP</option><option>Demat &amp; trading account</option><option>Tax reports for my investments</option></select>
<button class="btn y" style="margin-top:16px">Send on WhatsApp</button></form></div></section>'''
page('investments.html','Investments: mutual funds & demat | KF securities','Mutual fund investments and demat & trading accounts with KF Securities. '+RISK,inv,'investments')

con=f'''<div class="page-hero"><div class="wrap"><div class="eyebrow">Contact</div><h1>Talk to our desk</h1></div></div>
<section><div class="wrap"><div class="grid3" style="margin-top:0">
<div class="card"><h3>Call / WhatsApp</h3><p><a href="tel:+919633444704">+91 96334 44704</a></p><a class="btn w sm go" data-wa="Hi KF Securities">WhatsApp us</a></div>
<div class="card a"><h3>Email</h3><p><a href="mailto:social@kfsecurities.com">social@kfsecurities.com</a></p></div>
<div class="card r"><h3>Office</h3><p>{OFFICE}</p><p style="margin-top:8px"><b>Registered office:</b> {REG}</p></div></div></div></section>'''
page('contact.html','Contact | KF securities','Contact KF Securities Private Limited, Trivandrum.',con,'contact')

def legal(p,t,b): page(p,t+' | KF securities',t+' of '+LEGAL+'.',f'<div class="page-hero"><div class="wrap"><div class="eyebrow">KF securities · {LEGAL}</div><h1>{t}</h1><p>Last updated: 14 November 2026</p></div></div><article class="legal">{b}</article>')
for p,t,f in [('refund-policy.html','Refund & cancellation policy','refund.html'),('terms.html','Terms of service','terms.html'),('privacy-policy.html','Privacy policy','privacy.html'),('disclaimer.html','Disclaimer','disclaimer.html')]:
    legal(p,t,open('src/content/'+f).read())
exec(open('pages.py').read())
print('built')
