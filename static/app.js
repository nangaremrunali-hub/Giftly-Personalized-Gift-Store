document.addEventListener('DOMContentLoaded',()=>{
  document.body.classList.add('page-ready');
  requestAnimationFrame(()=>document.body.classList.add('route-mounted'));
  const path=location.pathname.replace(/^\//,'').split('/')[0]||'home';
  document.body.classList.add('route-'+path.replace(/[^a-z0-9_-]/gi,''));
  const category=new URLSearchParams(location.search).get('category');
  if(category) document.body.classList.add('category-'+category.toLowerCase());
});

document.addEventListener('DOMContentLoaded',()=>{
 const q=(s,p=document)=>p.querySelector(s), qa=(s,p=document)=>[...p.querySelectorAll(s)];
 document.body.classList.add('js');
 const toast=m=>{const t=q('#toast');if(!t)return;t.textContent=m;t.classList.add('show');clearTimeout(window.__toast);window.__toast=setTimeout(()=>t.classList.remove('show'),2200)};
 const reveal=()=>{qa('.reveal,.reveal-left,.reveal-right').forEach((el,i)=>{if(el.dataset.revealBound)return;el.dataset.revealBound='1';});const io=new IntersectionObserver(es=>es.forEach(e=>{if(e.isIntersecting){e.target.classList.add('visible');io.unobserve(e.target)}}),{threshold:.08,rootMargin:'0px 0px -40px'});qa('.reveal,.reveal-left,.reveal-right').forEach(x=>io.observe(x));setTimeout(()=>qa('.reveal,.reveal-left,.reveal-right').forEach(x=>x.classList.add('visible')),1800)};
 reveal();
 const bar=q('.progress');const progress=()=>{const max=document.documentElement.scrollHeight-innerHeight;if(bar)bar.style.width=(max?scrollY/max*100:0)+'%'};addEventListener('scroll',progress,{passive:true});progress();
 qa('[data-add]').forEach(btn=>btn.addEventListener('click',async e=>{e.preventDefault();const fd=new FormData();fd.append('id',btn.dataset.add);try{const d=await(await fetch('/cart/add',{method:'POST',body:fd})).json();if(d.ok){const badge=q('.bag i');if(badge)badge.textContent=d.count;btn.classList.add('added');toast('Added to your bag ✦');setTimeout(()=>btn.classList.remove('added'),650)}}catch{toast('Please try again.')}}));
 qa('[data-wish]').forEach(btn=>btn.addEventListener('click',async e=>{e.preventDefault();const fd=new FormData();fd.append('id',btn.dataset.wish);try{const d=await(await fetch('/wish',{method:'POST',body:fd})).json();btn.textContent=d.active?'♥':'♡';toast(d.active?'Saved for later ♡':'Removed from saved')}catch{toast('Please log in to save gifts.')}}));
 if(matchMedia('(pointer:fine)').matches)qa('[data-tilt]').forEach(card=>{card.addEventListener('pointermove',e=>{const r=card.getBoundingClientRect(),x=e.clientX-r.left-r.width/2,y=e.clientY-r.top-r.height/2;card.style.transform=`perspective(1000px) translateY(-5px) rotateX(${-y/r.height*2}deg) rotateY(${x/r.width*2}deg)`});card.addEventListener('pointerleave',()=>card.style.transform='')});
 const pay=q('#pay'),modal=q('#modal');if(pay&&modal){pay.onclick=()=>modal.classList.add('open');q('#x',modal)?.addEventListener('click',()=>modal.classList.remove('open'));q('#place',modal)?.addEventListener('click',async()=>{const choice=q('[name=payment]:checked',modal);if(!choice){toast('Choose a payment method first');return}const fd=new FormData();fd.append('payment',choice.value);const d=await(await fetch('/order',{method:'POST',body:fd})).json();if(d.ok)modal.innerHTML=`<div class="modalbox success"><div class="success-mark">✓</div><h2>Order placed!</h2><p>${d.msg}</p><a class="btn dark full" href="/orders">View my orders →</a></div>`})}
});

window.addEventListener('pageshow',()=>{const w=document.querySelector('.page-wipe');if(w){w.style.animation='pageWipe .95s cubic-bezier(.2,.8,.2,1) forwards';}});
