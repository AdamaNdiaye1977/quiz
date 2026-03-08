// Controlla se il Service Worker è supportato dal browser
if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
      // Registriamo il Service Worker
      navigator.serviceWorker
        .register('/service-worker.js') // Percorso al tuo file service-worker.js
        .then((registration) => {
          console.log('Service Worker registrato con successo:', registration);
        })
        .catch((error) => {
          console.log('Errore nella registrazione del Service Worker:', error);
        });
    });
  } else {
    console.log('Service Worker non supportato in questo browser.');
  }
  
  