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
