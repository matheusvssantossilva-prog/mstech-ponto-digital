self.addEventListener('install', e => {
self.skipWaiting();
});

self.addEventListener('activate', e => {
return self.clients.claim();
});

self.addEventListener('push', function(event) {
// bloqueia notificações fantasmas
return;
});
