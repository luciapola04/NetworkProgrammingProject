# Relazione tecnica: Realizzazione di un Web Server minimale in Python e sito statico

## 1. Obiettivo

L'obiettivo del progetto è quello di realizzare un semplice server HTTP minimale utilizzando Python e il modulo `socket`, in grado di servire un sito web statico HTML/CSS.
Il server deve:
-rispondere su `localhost` alla porta `8080`
-servire almeno 3 pagine HTML statiche
-gestire le richieste GET e rispondere con codice 200
-implementare risposta 404 per file inesistenti

## 2. Descrizione del Web Server

Il server è stato implementato utilizzando socket TCP in Python. Ascolta sulla porta 8080 e accetta connessioni in ingresso. Per ogni richiesta:

- Si legge la richiesta HTTP inviata dal client e viene effettuato il parsing della prima riga per estrarre il metodo HTTP, il percorso richiesto e la versione.
- Sono gestite esclusivamente le richieste di tipo `GET`. Qualsiasi altro metodo riceve una risposta con codice `405 Method Not Allowed`.
- Se la richiesta è rivolta alla root (`/`), viene servito il file `index.html` di default.
- Viene costruito il percorso assoluto al file richiesto nella cartella `www/`.
- Se il file esiste, il server lo legge in modalità binaria e ne determina il MIME type tramite la libreria `mimetypes`.
- Il server risponde con codice `200 OK`, le intestazioni HTTP appropriate (Content-Type, Content-Length, Connection) e il contenuto del file.
- Se il file non viene trovato, viene restituita una pagina semplice con errore `404 Not Found`.
- Ogni richiesta viene loggata sulla console con timestamp, metodo, percorso e codice di risposta.

## 3. Struttura del sito web

La cartella `www/` contiene le risorse statiche del sito:

- `index.html`: pagina principale con una breve descrizione e link alle altre pagine.
- `salati.html`: pagina con ricette di snack salati.
- `dolci.html`: pagina con ricette dolci.
- `quiz.html`: pagina contenente un quiz interattivo realizzato in HTML e JavaScript.
- `style.css`: foglio di stile CSS comune a tutte le pagine, con un design semplice e coerente.
- `images/chef.png`: immagine con sfondo trasparente utilizzata nella home page.

Le pagine HTML sono scritte in italiano, con una struttura semantica chiara e navigazione facilitata tramite menu.

## 4. Funzionalità aggiuntive

Oltre ai requisiti minimi, il server implementa:

- Riconoscimento e gestione automatica dei MIME types, per servire correttamente file HTML, CSS, immagini e altri formati.
- Logging dettagliato di ogni richiesta HTTP ricevuta con data, ora, metodo, percorso e codice di stato.
- Risposta con codice `405 Method Not Allowed` per metodi diversi da GET.
- Nel sito, il quiz utilizza JavaScript per calcolare e mostrare il risultato senza ricaricare la pagina.
- Meta tag `viewport` nelle pagine HTML per una migliore esperienza su dispositivi mobili.

## 5. Modalità d'uso

Per avviare il server:

1. Posizionare la cartella `www` nella stessa directory in cui si trova lo script Python del server.
2. Eseguire il server con il comando: python webServer.py
3. Aprire un browser e navigare all'indirizzo: http://localhost:8080/
4. Navigare il sito e utilizzare le pagine e il quiz.

**Creato da Pola Lucia per il corso 'Programmazione di Reti', Ingegneria e Scienze Informatiche A.A 2024/2025**

