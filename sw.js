// Service worker mínimo, solo red: no cachea nada para que el calendario
// siempre esté fresco. Existe para cumplir los requisitos de instalación
// de la PWA en Android (Chrome pide un service worker con handler de fetch).
self.addEventListener("install", () => self.skipWaiting());
self.addEventListener("activate", e => e.waitUntil(self.clients.claim()));
self.addEventListener("fetch", e => {
  e.respondWith(fetch(e.request));
});
