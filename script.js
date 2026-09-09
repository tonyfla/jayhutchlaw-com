const t=document.querySelector('.menu-toggle'),n=document.querySelector('.site-nav');
const overrides=document.createElement('link');overrides.rel='stylesheet';overrides.href='overrides.css';document.head.append(overrides);
if(n&&!n.querySelector('[href="index.html"]')){const home=document.createElement('a');home.href='index.html';home.textContent='Home';n.prepend(home)}
t?.addEventListener('click',()=>{n.classList.toggle('open');t.setAttribute('aria-expanded',n.classList.contains('open'))});
document.querySelectorAll('.site-nav a').forEach(a=>a.onclick=()=>n?.classList.remove('open'));
document.querySelectorAll('.year').forEach(y=>y.textContent=new Date().getFullYear());
document.querySelectorAll('form').forEach(f=>f.onsubmit=e=>{e.preventDefault();f.querySelector('.form-success')?.classList.add('show')});
