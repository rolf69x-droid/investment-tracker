const CACHE='investment-install-v3';
const SHELL=['index-1.html','manifest.webmanifest','icon-192.png','icon-512.png'];
self.addEventListener('install',event=>{
  event.waitUntil(caches.open(CACHE).then(cache=>cache.addAll(SHELL)).then(()=>self.skipWaiting()));
});
self.addEventListener('activate',event=>{
  event.waitUntil(caches.keys().then(keys=>Promise.all(keys.filter(key=>key.startsWith('investment-')&&key!==CACHE).map(key=>caches.delete(key)))).then(()=>self.clients.claim()));
});
self.addEventListener('fetch',event=>{
  const url=new URL(event.request.url);
  if(event.request.method!=='GET'||url.origin!==self.location.origin||url.pathname.includes('/data/'))return;
  const scope=new URL('./',self.location.href);
  const corrected=new URL('index-1.html',scope).href;
  if(event.request.mode==='navigate'){
    const legacy=url.pathname===scope.pathname||url.pathname===new URL('index.html',scope).pathname;
    event.respondWith(fetch(legacy?corrected:event.request).catch(()=>caches.match(corrected)));
    return;
  }
  event.respondWith(fetch(event.request).catch(()=>caches.match(event.request)));
});
