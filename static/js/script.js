function checkAnswer() {
    const input = document.getElementById('code-input');
    const feedback = document.getElementById('feedback');
    const userCode = input.value.trim();
    const correctCode = questions[currentQuestion].code;
    
    const correctSound = document.getElementById("correctSound");
    const wrongSound = document.getElementById("wrongSound");
  
    if (userCode === correctCode) {
      feedback.textContent = "✅ Corretto!";
      feedback.className = "feedback correct";
      score++;
      correctSound.play();  // Suono corretto
      currentQuestion++;
      attempts = 0;
      setTimeout(showQuestion, 1000);
    } else {
      attempts++;
      if (attempts < 3) {
        feedback.textContent = `❌ Codice errato. Tentativo ${attempts} di 3.`;
        wrongSound.play();  // Suono errore
      } else {
        feedback.textContent = `✖️ Risposta errata. Il codice corretto era ${correctCode}.`;
        wrongSound.play();  // Suono errore
        currentQuestion++;
        attempts = 0;
        setTimeout(showQuestion, 1500);
      }
    }
  }

  function showResult() {
    container.style.display = 'none';
    scoreBox.style.display = 'block';
    restartBtn.style.display = 'inline-block';
    scoreBox.innerHTML = `Hai totalizzato <strong>${score}</strong> su <strong>${Math.min(10, questions.length)}</strong>!`;
  
    // Salvataggio del punteggio nel localStorage
    const quizStats = JSON.parse(localStorage.getItem("quizStats")) || [];
    quizStats.push({
      score: score,
      total: Math.min(10, questions.length),
      date: new Date().toISOString()
    });
    localStorage.setItem("quizStats", JSON.stringify(quizStats));
  }

  
  