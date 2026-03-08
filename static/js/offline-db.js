// Apri (o crea) un database chiamato 'quizDB'
const request = indexedDB.open("quizDB", 1);

request.onupgradeneeded = function (event) {
  const db = event.target.result;
  // Crea un archivio per le risposte se non esiste
  const store = db.createObjectStore("responses", { keyPath: "questionId" });
  console.log("IndexedDB: archivio creato");
};

request.onsuccess = function (event) {
  const db = event.target.result;
  console.log("IndexedDB pronto!");

  // ESEMPIO: salva una risposta
  function saveAnswer(questionId, answer) {
    const tx = db.transaction("responses", "readwrite");
    const store = tx.objectStore("responses");
    store.put({ questionId, answer });
  }

  // ESEMPIO: recupera una risposta
  function getAnswer(questionId, callback) {
    const tx = db.transaction("responses", "readonly");
    const store = tx.objectStore("responses");
    const request = store.get(questionId);
    request.onsuccess = () => {
      callback(request.result);
    };
  }

  // Uso esempio:
  saveAnswer(1, "12345"); // salva il codice per la domanda 1
  getAnswer(1, (data) => {
    console.log("Risposta salvata:", data);
  });
};

request.onerror = function () {
  console.error("Errore nell'aprire IndexedDB");
};
