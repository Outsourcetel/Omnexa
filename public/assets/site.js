(function(){
  window.dataLayer=window.dataLayer||[];
  function track(name,params){window.dataLayer.push(Object.assign({event:name},params||{}));}
  document.addEventListener('click',function(e){
    var a=e.target.closest&&e.target.closest('a[href]');
    if(!a)return;
    var h=a.getAttribute('href')||'';
    if(h.indexOf('tel:')===0)track('click_to_call',{page:location.pathname});
    else if(h.indexOf('wa.me')>-1)track('click_whatsapp',{page:location.pathname});
  });
  document.querySelectorAll('form.lead').forEach(function(f){
    f.addEventListener('submit',function(e){
      e.preventDefault();
      var d=new FormData(f), g=function(k){return (d.get(k)||'').toString().trim();};
      var msg='Hello, I need: '+g('service')+'\nName: '+g('name')+'\nPhone: '+g('phone')+'\nCity: '+g('city')+(g('message')?'\nDetails: '+g('message'):'')+'\nPage: '+location.pathname;
      track('generate_lead',{service:g('service'),page:location.pathname});
      var ep=f.getAttribute('data-endpoint');
      var wa='https://wa.me/'+f.getAttribute('data-wa')+'?text='+encodeURIComponent(msg);
      var go=function(){window.location.href=wa;};
      if(ep){fetch(ep,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(Object.fromEntries(d))}).then(go,go);}
      else go();
    });
  });
})();
/* Scroll reveal. Illustrations start drawing when they come into view. */
(function(){
  var show=function(el){el.classList.add('in');};
  var fade=document.querySelectorAll('main section h2.s,main section .kicker,main section p.sub,.cards .card,.door,ul.ticks li,ol.steps li,details,.notice,.chips a,.cta-band h2');
  var art=document.querySelectorAll('.illus');
  if(!('IntersectionObserver' in window)){fade.forEach(show);art.forEach(show);return;}
  var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){show(e.target);io.unobserve(e.target);}});},{threshold:.15,rootMargin:'0px 0px -30px 0px'});
  var last=null,n=0;
  fade.forEach(function(el){
    el.classList.add('reveal');
    n=(el.parentNode===last)?n+1:0; last=el.parentNode;
    el.style.transitionDelay=Math.min(n,6)*70+'ms';
    io.observe(el);
  });
  art.forEach(function(el){io.observe(el);});
})();

/* Process: tabbed stepper (autoplays when in view, stops on interaction) */
(function(){
  var calm=window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches;
  document.querySelectorAll('.pw').forEach(function(w){
    var steps=[].slice.call(w.querySelectorAll('.pstep')),panels=[].slice.call(w.querySelectorAll('.ppanel'));
    var cur=0,timer=null,stopped=calm,inView=false,hover=false;
    function show(i){
      cur=i;
      steps.forEach(function(s,k){var on=k===i;s.classList.toggle('active',on);s.setAttribute('aria-selected',on?'true':'false');s.tabIndex=on?0:-1;});
      panels.forEach(function(p,k){p.classList.toggle('active',k===i);});
      var a=steps[i];if(a&&a.scrollIntoView&&w.querySelector('.plist').scrollWidth>w.querySelector('.plist').clientWidth){var l=w.querySelector('.plist');l.scrollTo({left:a.offsetLeft-12,behavior:'smooth'});}
    }
    function tick(){
      clearTimeout(timer);
      var run=!stopped&&inView&&!hover;
      w.classList.toggle('auto',run);
      if(run){timer=setTimeout(function(){show((cur+1)%steps.length);tick();},7000);}
    }
    function userPick(i){stopped=true;show(i);tick();}
    steps.forEach(function(s,i){
      s.addEventListener('click',function(){userPick(i);});
      s.addEventListener('keydown',function(e){
        var n=null;
        if(e.key==='ArrowDown'||e.key==='ArrowRight')n=(cur+1)%steps.length;
        if(e.key==='ArrowUp'||e.key==='ArrowLeft')n=(cur-1+steps.length)%steps.length;
        if(n!==null){e.preventDefault();userPick(n);steps[n].focus();}
      });
    });
    w.addEventListener('mouseenter',function(){hover=true;tick();});
    w.addEventListener('mouseleave',function(){hover=false;tick();});
    show(0);
    if('IntersectionObserver' in window){
      new IntersectionObserver(function(es){es.forEach(function(e){inView=e.isIntersecting;tick();});},{threshold:.35}).observe(w);
    }
  });
})();

/* Process: full timeline progress rail, gantt and lanes */
(function(){
  var wrap=document.querySelector('.tlwrap');
  if(wrap){
    var rail=wrap.querySelector('.tlrail'),raf=0;
    var upd=function(){
      raf=0;var r=wrap.getBoundingClientRect(),h=window.innerHeight;
      var p=(h*.55-r.top)/r.height;p=Math.max(0,Math.min(1,p));
      rail.style.setProperty('--p',p.toFixed(3));
    };
    window.addEventListener('scroll',function(){if(!raf)raf=requestAnimationFrame(upd);},{passive:true});
    window.addEventListener('resize',upd);upd();
  }
  var io=('IntersectionObserver' in window)?new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target);}});},{threshold:.25,rootMargin:'0px 0px -12% 0px'}):null;
  document.querySelectorAll('.tl,.gantt,.lane').forEach(function(el){if(io)io.observe(el);else el.classList.add('in');});
})();
