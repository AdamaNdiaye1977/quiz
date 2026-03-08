self.addEventListener("fetch", (event) => {
  event.respondWith(
    caches.match(event.request).then((response) => {
      // Se la risorsa è nella cache, la restituisce
      if (response) {
        // Aggiorna la cache in background se la risorsa è presente
        fetch(event.request).then((networkResponse) => {
          if (networkResponse && networkResponse.status === 200) {
            caches.open(CACHE_NAME).then((cache) => {
              cache.put(event.request, networkResponse.clone());
            });
          }
        });
        return response;
      }

      // Se non c'è nella cache, fai una richiesta di rete
      return fetch(event.request)
        .then((networkResponse) => {
          if (networkResponse && networkResponse.status === 200) {
            caches.open(CACHE_NAME).then((cache) => {
              cache.put(event.request, networkResponse.clone());
            });
          }
          return networkResponse;
        })
        .catch((error) => {
          // Fallback in caso di errore di rete (esempio: mostra una pagina offline)
          return caches.match('/offline.html');  // Assicurati di avere una pagina offline.html nella cache
        });
    })
  );
});
