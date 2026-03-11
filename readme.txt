***** Per lanciare la APP ******

commando : python app.py

codice segreto : penny77

********************************
Procedure per GITHUB
    - Crea il file requirements.txt
        COMMAND: pip freeze > requirements.txt
    
    - Crea il file Procfile (fondamentale!) Il Procfile dice a Render come avviare la tua app in produzione
        COMMAND: echo "web: gunicorn app:app" > Procfile
    
    - Installiamo gunicorn (necessario per il Procfile)
        COMMAND:  pip install gunicorn
          poi subito fare update .  
        COMMAND:python.exe -m pip install --upgrade pip
    
    - Poi aggiorniamo requirements.txt per includere gunicorn:

        COMMAND: pip freeze > requirements.txt
    
    - Inizializziamo Git
        # Inizializza Git nella cartella
        COMMAND: git init

        # Aggiungi tutti i file
        COMMAND: git add .

        # Crea il primo commit
        COMMAND: git commit -m "Primo commit - preparazione per Render"

        # Rinomina il branch in main (standard)
        COMMAND: git branch -M main

    -Configura il nome utente
        COMMAND: git config --global user.name "AdamaNdiaye1977"
    
    - Configura l'email
        COMMAND : git config --global user.email "adama29439@gmail.com"

    -Verifica la configurazione
        COMMAND: git config --global --list
    
    - Ora prova il commit
        Una volta configurato, riprova:
        COMMAND: git commit -m "Primo commit - preparazione per Render"

    -----------------------------------------
    -----------------------------------------
    ✅ Soluzione CORRETTA passo passo:
Passo 1: ANNULLA tutto e ricomincia
Prima di tutto, esci dalla modalità di attesa premendo CTRL+C (lo hai già fatto, bene).

Passo 2: Ora esegui UN COMANDO ALLA VOLTA:
bash
# 1. AGGIUNGI i file
git add .
bash
# 2. COMMIT con le virgolette CHIUSE (importante!)
git commit -m "Primo commit"
Nota: le virgolette devono essere così: "Primo commit" NON "Primo commit (mancava la virgoletta di chiusura)

bash
# 3. Controlla che il commit esista
git log --oneline
Dovresti vedere qualcosa come: abc1234 Primo commit

bash
# 4. Rinomina il branch
git branch -M main
bash
# 5. Ora pusha
git push -u origin main

     -----   
✅ COSA ABBIAMO COMPLETATO:
Configurato Git ✅

Fatto il commit di 216 file con successo ✅

Branch rinominato in main ✅

Push su GitHub completato con 225 oggetti caricati (3.58 MB) ✅

🌍 VERIFICA SU GITHUB
Ora puoi andare su:

text
https://github.com/AdamaNdiaye1977/quiz
e vedrai tutti i tuoi file online! 🚀

☁️ PASSO SUCCESSIVO: DEPLOY SU RENDER


☁️ PASSO SUCCESSIVO: DEPLOY SU RENDER
Ora che il codice è su GitHub, passiamo a Render:

1. Vai su Render.com
2. Crea un account (se non l'hai già)
Clicca su "Sign up"

Scegli "Sign up with GitHub" (così si collega automaticamente)

Autorizza Render ad accedere a GitHub

3. Crea un nuovo Web Service
Dal dashboard, clicca "New +" → "Web Service"

Connetti il repository "quiz" che hai appena caricato

Autorizza se richiesto

4. Configura il Web Service:
Campo	Valore
Name	quiz (o quello che vuoi)
Region	Frankfurt (EU Central)
Branch	main
Runtime	Python 3
Build Command	pip install -r requirements.txt
Start Command	gunicorn app:app
Plan	Free ✅
5. Clicca su "Create Web Service"
Render impiegherà 2-3 minuti per fare il deploy. Alla fine ti darà un URL tipo:

text
https://quiz.onrender.com

--------------------------------------------------
********************************