self.addEventListener("install", event => {
  console.log("App instalado");
  self.skipWaiting();
});

self.addEventListener("fetch", event => {
  event.respondWith(
    caches.open("ponto-cache").then(cache => {
      return cache.match(event.request).then(response => {
        return response || fetch(event.request).then(fetchRes => {
          cache.put(event.request, fetchRes.clone());
          return fetchRes;
        });
      });
    })
  );
});
