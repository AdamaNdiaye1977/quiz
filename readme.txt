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
********************************