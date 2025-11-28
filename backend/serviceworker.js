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
            .then(cache => cache.addAll(filesToCache))
    );
});

// Clear old caches on activate
self.addEventListener('activate', event => {
    event.waitUntil(
        caches.keys().then(cacheNames => 
            Promise.all(
                cacheNames
                    .filter(name => name.startsWith("django-pwa-") && name !== staticCacheName)
                    .map(name => caches.delete(name))
            )
        )
    );
});

// Serve from cache only if offline
self.addEventListener("fetch", event => {
    const url = event.request.url;

    // Siempre dejar pasar API y JSON
    if (url.endsWith(".json") || url.includes("/api/")) {
        return; 
    }

    // Siempre dejar pasar manifest
    if (url.includes("manifest.json")) {
        event.respondWith(
            caches.match(event.request)
                .then(resp => resp || fetch(event.request))
        );
        return;
    }

    // Solo usar cache si estamos offline
    if (!navigator.onLine) {
        event.respondWith(
            caches.match(event.request)
                .then(response => response || caches.match('/offline/'))
        );
    }
    // Si estamos online, no interceptamos (pasará directo al servidor)
});
