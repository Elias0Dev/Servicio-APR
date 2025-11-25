// Base Service Worker implementation.  To use your own Service Worker, set the PWA_SERVICE_WORKER_PATH variable in settings.py

var staticCacheName = "django-pwa-v" + new Date().getTime();
var filesToCache = [
    '/offline/',
    '/manifest.json',
    '/detalle_boletas/',
    '/static/inicio/css/style.css',
    '/static/inicio/css/bootstrap.min.css',
    '/static/inicio/css/bootstrap.min.css.map',
    '/static/inicio/js/bootstrap.bundle.min.js',
    '/static/inicio/js/script.js',
    '/static/inicio/js/db.js',
    '/static/inicio/img/boleta-icon.png',
    '/static/inicio/img/pago-icon.png',
    '/static/inicio/img/logo.png',
];

// Cache on install
self.addEventListener("install", event => {
    this.skipWaiting();
    event.waitUntil(
        caches.open(staticCacheName)
            .then(cache => {
                return cache.addAll(filesToCache);
            })
    )
});

// Clear cache on activate
self.addEventListener('activate', event => {
    event.waitUntil(
        caches.keys().then(cacheNames => {
            return Promise.all(
                cacheNames
                    .filter(cacheName => (cacheName.startsWith("django-pwa-")))
                    .filter(cacheName => (cacheName !== staticCacheName))
                    .map(cacheName => caches.delete(cacheName))
            );
        })
    );
});

// Serve from Cache
self.addEventListener("fetch", event => {
    
    const url = event.request.url;

    // Permitir que manifest use cache, pero no fetch del server offline
    if (url.includes("manifest.json")) {
        event.respondWith(
            caches.match(event.request)
                .then(resp => resp || fetch(event.request))
        );
        return;
    }

    // NO interceptar JSON API
    if (url.endsWith(".json") || url.includes("/api/")) {
        return; // dejar que falle si está offline
    }

    event.respondWith(
        caches.match(event.request)
            .then(response => response || fetch(event.request))
            .catch(() => caches.match('/offline/'))
    );
});

