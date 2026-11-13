# executed at the end of build.py
SEP=' › '
def svc_block(c, link=True):
    items=''.join(f'<div class="svc"><span>{E(x)}</span><a class="btn sm ob" href="/request?add={E(x).replace(" ","%20")}">+ Add</a></div>' for x in c['services'])
    h=f'<a href="/services/{c["slug"]}">{E(c["name"])}</a>' if link else E(c['name'])
    return f'<div class="svc-cat" id="{c["id"]}"><h3>{h}</h3><p class="note" style="margin-top:0">{E(c["blurb"])}</p><div class="svc-list">{items}</div></div>'

# static fallback list on /services (JS replaces it with the interactive version)
sp=open('site/services.html').read()
sp=sp.replace('<div id="svc"></div>','<div id="svc">'+''.join(svc_block(c) for c in cats)+'</div>')
open('site/services.html','w').write(sp)

LOCAL={'SC-8':'income tax return filing','SC-4':'GST registration and return filing','SC-1':'company and LLP registration','SC-7':'trademark registration','SC-6':'legal documentation and agreement drafting','SC-3':'payroll, PF and ESI','SC-5':'MSME, IEC, PF and ESI registration','SC-2':'ROC and RBI (FEMA) compliance'}
for c in cats:
    others=' · '.join(f'<a href="/services/{o["slug"]}">{E(o["name"])}</a>' for o in cats if o['id']!=c['id'])
    kw=LOCAL.get(c['id'],c['name'].lower())
    lead=f"{c['blurb']} KF Securities handles {kw} for businesses and individuals in Trivandrum, across Kerala and anywhere in India, online. Pick the services you need and get one written quote."
    body=(f'<div class="page-hero"><div class="wrap"><nav style="color:#C9D3EA;font-size:14px"><a href="/" style="color:#C9D3EA">Home</a>{SEP}<a href="/services" style="color:#C9D3EA">Services</a>{SEP}{E(c["name"])}</nav>'
          f'<div class="eyebrow" style="margin-top:12px">{len(c["services"])} services</div><h1>{E(c["name"])}</h1><p>{E(lead)}</p>'
          f'<div class="btns"><a class="btn y" href="/request">Request a quote</a><a class="btn o" data-wa="Hi KF Securities, I need help with {E(c["name"])}.">WhatsApp us</a></div></div></div>'
          f'<section style="padding-top:10px"><div class="wrap">{svc_block(c,False)}'
          f'<div class="steps" style="margin-top:40px"><div class="step"><h4>Tell us what you need</h4><p>Add services or describe your case.</p></div><div class="step"><h4>Written quote</h4><p>Fixed fee, timeline and documents list.</p></div><div class="step"><h4>Pay online</h4><p>UPI, card or netbanking against the quote number.</p></div><div class="step"><h4>Done &amp; filed</h4><p>One desk updates you until completion.</p></div></div>'
          f'<div class="box" style="margin-top:34px"><b>Other services:</b> {others}</div></div></section>')
    ld=[{"@context":"https://schema.org","@type":"Service","name":c['name'],"serviceType":c['name'],"description":lead,"provider":{"@id":BASE+"/#org"},"areaServed":{"@type":"Country","name":"India"},
         "hasOfferCatalog":{"@type":"OfferCatalog","name":c['name'],"itemListElement":[{"@type":"Offer","itemOffered":{"@type":"Service","name":x}} for x in c['services']]}},
        {"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"Home","item":BASE+"/"},{"@type":"ListItem","position":2,"name":"Services","item":BASE+"/services"},{"@type":"ListItem","position":3,"name":c['name']}]}]
    page(f'services/{c["slug"]}.html',E(f'{c["name"]} in Trivandrum & across India | KF securities'),E(lead[:300]),body,'services',ld,'0.8')

for f in ['site/pay.html','site/request.html']:
    h=open(f).read().replace('content="index,follow,max-image-preview:large"','content="noindex,follow"'); open(f,'w').write(h)
SITEMAP[:]=[x for x in SITEMAP if x[0] not in ('/pay','/request')]
today=datetime.date.today().isoformat()
open('site/sitemap.xml','w').write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+''.join(f'<url><loc>{BASE}{u}</loc><lastmod>{today}</lastmod><priority>{"1.0" if u=="/" else p}</priority></url>\n' for u,p in SITEMAP)+'</urlset>\n')
open('site/robots.txt','w').write(f'User-agent: *\nAllow: /\nDisallow: /pay\nDisallow: /request\n\nSitemap: {BASE}/sitemap.xml\n')
print('kfs urls', len(SITEMAP))
