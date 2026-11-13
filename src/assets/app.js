(function(){
const C = window.KFS;
const $ = s => document.querySelector(s);
const $$ = s => [...document.querySelectorAll(s)];
const inr = n => '₹' + Number(n).toLocaleString('en-IN');
const esc = s => String(s??'').replace(/[&<>"]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
const wa = (num, text) => 'https://wa.me/' + num + '?text=' + encodeURIComponent(text);
const qs = new URLSearchParams(location.search);
const KEY='kfs_basket';
const getB = () => { try{ return JSON.parse(localStorage.getItem(KEY)||'[]'); }catch(e){ return []; } };
const setB = b => { try{ localStorage.setItem(KEY, JSON.stringify(b)); }catch(e){} badge(); };
function badge(){ const n=getB().length; $$('.basket-n').forEach(e=>{ e.textContent=n; e.parentElement.classList.toggle('hidden', n===0); }); }
function sendLead(p){ if(!C.leadEndpoint) return; try{ fetch(C.leadEndpoint,{method:'POST',mode:'no-cors',headers:{'Content-Type':'text/plain'},body:JSON.stringify(Object.assign({brand:'KF Securities',page:location.pathname,ts:new Date().toISOString()},p))}); }catch(e){} }
function ref(p){ const d=new Date(); const z=n=>String(n).padStart(2,'0'); return p+'-'+String(d.getFullYear()).slice(2)+z(d.getMonth()+1)+z(d.getDate())+'-'+Math.random().toString(36).slice(2,6).toUpperCase(); }

const mb=$('.menu-btn'); if(mb) mb.onclick=()=>$('nav.main').classList.toggle('open');
$$('[data-wa]').forEach(a=>{ a.href=wa(C.whatsapp.orders, a.dataset.wa||'Hi KF Securities, I would like some help.'); a.target='_blank'; a.rel='noopener'; });
badge();

/* services catalogue */
async function services(){
  const root=$('#svc'); if(!root) return;
  const cats=await (await fetch('/data/services.json')).json();
  const q=$('#s-q'), cs=$('#s-cat');
  cs.innerHTML='<option value="">All services</option>'+cats.map(c=>`<option value="${c.id}">${esc(c.name)}</option>`).join('');
  if(qs.get('cat')) cs.value=qs.get('cat');
  const run=()=>{
    const term=q.value.trim().toLowerCase(), cat=cs.value, b=getB(); let n=0;
    root.innerHTML=cats.filter(c=>!cat||c.id===cat).map(c=>{
      const list=c.services.filter(s=>!term||s.toLowerCase().includes(term)||c.name.toLowerCase().includes(term)); n+=list.length;
      if(!list.length) return '';
      return `<div class="svc-cat" id="${c.id}"><h3>${esc(c.name)}</h3><p class="note" style="margin-top:0">${esc(c.blurb)}</p><div class="svc-list">${list.map(s=>{const on=b.includes(s);return `<div class="svc"><span>${esc(s)}</span><button class="btn sm ${on?'n':'ob'}" data-s="${esc(s)}">${on?'✓ Added':'+ Add'}</button></div>`}).join('')}</div></div>`;
    }).join('') || '<p>No service matches. Message us on WhatsApp and we will help.</p>';
    $('#s-count').textContent=n+' services';
    $$('#svc button[data-s]').forEach(x=>x.onclick=()=>{ let b=getB(); const s=x.dataset.s; b=b.includes(s)?b.filter(y=>y!==s):b.concat(s); setB(b); run(); });
  };
  q.oninput=run; cs.onchange=run; run();
}

/* request (quote) checkout */
function request(){
  const root=$('#req'); if(!root) return;
  const pre=qs.get('add'); if(pre){ const b=getB(); if(!b.includes(pre)) setB(b.concat(pre)); }
  const draw=()=>{
    const b=getB();
    $('#req-list').innerHTML = b.length ? b.map(s=>`<div class="svc"><span>${esc(s)}</span><button class="btn sm ob" data-r="${esc(s)}">Remove</button></div>`).join('') : '<p>No services added yet. <a href="/services">Browse services</a> or describe what you need below.</p>';
    $$('#req-list button[data-r]').forEach(x=>x.onclick=()=>{ setB(getB().filter(y=>y!==x.dataset.r)); draw(); });
  };
  draw();
  $('#req-form').onsubmit=e=>{
    e.preventDefault(); const f=Object.fromEntries(new FormData(e.target).entries()); const r=ref('KFS'); const b=getB();
    const msg=[`New service request ${r}`, b.length?'Services:\n- '+b.join('\n- '):'', f.details?`Details: ${f.details}`:'', `Name: ${f.name}`, f.business?`Business: ${f.business}`:'', `Phone: ${f.phone}`, f.email?`Email: ${f.email}`:'', `City: ${f.city||'-'}`].filter(Boolean).join('\n');
    sendLead({kind:'service_request',ref:r,services:b,form:f});
    $('#req-form').classList.add('hidden');
    $('#req-done').classList.remove('hidden');
    $('#req-done').innerHTML=`<div class="ok"><b>Request reference: ${r}</b><br>Send it to our desk on WhatsApp. We reply with a written quote, timeline and the documents we need.</div><a class="btn w" style="width:100%;margin-top:14px" target="_blank" rel="noopener" href="${wa(C.whatsapp.orders,msg)}">Send request on WhatsApp</a><p class="note">Once you accept the quote, pay online on our <a href="/pay">payments page</a> using the quote number.</p>`;
    setB([]);
  };
}

/* pay against quote / invoice */
function pay(){
  const root=$('#pay-form'); if(!root) return;
  if(!C.upi.id && !C.razorpayKey) $('#pay-off').classList.remove('hidden');
  root.onsubmit=e=>{
    e.preventDefault(); const f=Object.fromEntries(new FormData(e.target).entries()); const amt=Math.round(Number(f.amount)); if(!(amt>0)) return;
    const msg=`Payment for ${f.quote}\nName: ${f.name}\nPhone: ${f.phone}\nAmount: ${inr(amt)}`;
    let h=`<div class="ok"><b>Paying ${inr(amt)} against ${esc(f.quote)}</b></div>`;
    if(C.upi.id){ const link=`upi://pay?pa=${encodeURIComponent(C.upi.id)}&pn=${encodeURIComponent(C.upi.payee)}&am=${amt}&cu=INR&tn=${encodeURIComponent(f.quote)}`;
      h+=`<div class="paybox"><h4>Pay by UPI</h4><a class="btn n" href="${link}" style="margin-top:10px">Open UPI app</a><div id="qr" class="qr"></div><p class="note">UPI ID: <b>${esc(C.upi.id)}</b> · ${esc(C.upi.payee)}</p><label>UPI transaction ID</label><input id="utr"></div>`; }
    if(C.razorpayKey) h+=`<div class="paybox"><h4>Card, netbanking or wallet</h4><button type="button" class="btn n" id="rzp" style="margin-top:10px">Pay ${inr(amt)} securely</button></div>`;
    if(!C.upi.id && !C.razorpayKey) h+=`<div class="warn">Online payment is being set up. Send this to our desk and we will share the payment details.</div>`;
    h+=`<a class="btn w" id="send" target="_blank" rel="noopener" style="width:100%;margin-top:14px">Send payment confirmation on WhatsApp</a>`;
    $('#pay-step').innerHTML=h; root.classList.add('hidden');
    if($('#qr')&&window.QRCode) new QRCode($('#qr'),{text:`upi://pay?pa=${C.upi.id}&pn=${encodeURIComponent(C.upi.payee)}&am=${amt}&cu=INR&tn=${f.quote}`,width:196,height:196});
    const set=()=>{ const u=$('#utr')?$('#utr').value.trim():''; $('#send').href=wa(C.whatsapp.orders,msg+(u?`\nUPI transaction ID: ${u}`:'')); }; if($('#utr')) $('#utr').oninput=set; set();
    if($('#rzp')) $('#rzp').onclick=()=>{ new Razorpay({key:C.razorpayKey,amount:amt*100,currency:'INR',name:'KF Securities',description:f.quote,prefill:{name:f.name,contact:f.phone},notes:{quote:f.quote},theme:{color:'#0B2545'},handler:r=>{ $('#send').href=wa(C.whatsapp.orders,msg+'\nPaid online, payment ID: '+r.razorpay_payment_id); sendLead({kind:'payment',quote:f.quote,payment:r.razorpay_payment_id}); }}).open(); };
  };
}

/* simple request forms */
$$('form[data-request]').forEach(f=>f.onsubmit=e=>{ e.preventDefault(); const fd=new FormData(f); const lines=[f.dataset.request]; for(const [k,v] of fd.entries()) if(String(v).trim()) lines.push(k+': '+v); sendLead({kind:f.dataset.kind||'enquiry',fields:Object.fromEntries(fd.entries())}); window.open(wa(C.whatsapp.orders,lines.join('\n')),'_blank'); });
$$('.arn').forEach(e=>{ if(C.arn) e.textContent='AMFI-registered Mutual Fund Distributor · ARN-'+C.arn; else e.remove(); });

services(); request(); pay();
})();
