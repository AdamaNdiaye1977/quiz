document.addEventListener("DOMContentLoaded", () => {
  const input = document.getElementById("code_input");
  
  document.querySelectorAll(".key").forEach((key) => {
    key.addEventListener("click", () => {
      const value = key.textContent;
  
      // Se il tasto è "clear", resetta il campo input
      if (key.classList.contains("clear")) {
        input.value = "";
      } 
      // Se il tasto è "confirm", invia il form
      else if (key.classList.contains("confirm")) {
        input.form.submit();
      } 
      // Altrimenti, aggiungi il valore del tasto all'input
      else {
        if (input.value.length < 6) {  // Limita a 6 cifre
          input.value += value;
        }
      }
    });
  });
});
