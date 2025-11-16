# KPX Portfolio - Planning Document

## Panoramica del Progetto
**Nome Prodotto:** KPX Portfolio  
**Descrizione:** Un sito web personale per mostrare i miei lavori di sviluppo software, con un focus su applicazioni desktop professionali e strumenti di gestione dati (CRM).

## Stack Tecnologico
*   **Frontend:** HTML5, CSS3 (con variabili CSS), JavaScript (Vanilla, SortableJS per l'ordinamento)
*   **Backend:** Non applicabile (Sito statico)
*   **Styling:** Framework CSS (Tailwind CSS) - *Pianificato per un futuro refactoring*
*   **Font:** Google Fonts (Roboto)
*   **Animazioni UI:** SVG, CSS Keyframes
*   **Gestione File Excel:** Libreria `XLSX`
*   **Gestione Immagini:** Libreria `canvas-to-blob`
*   **Gestione File DXF:** Libreria `dxf-parser`
*   **Gestione PDF:** Libreria `pdfkit`
*   **Ambiente di Sviluppo:** Visual Studio Code, pgAdmin 4, nodemon

## Schema del Database (Progetto Futuro: CRM System)
*   `utenti`: Tabella per gli utenti del sistema (clienti, admin, management).
*   `clienti`: Anagrafe dei clienti.
*   `interazioni`: Tabella per tracciare le comunicazioni (email, chiamate, note).
*   `prodotti`: Catalogo dei prodotti/servizi offerti.
*   `preventivi`: Tabella per i preventivi generati dal sistema.
*   `schede_tecniche`: Tabella per la gestione dei documenti tecnici (es. schede di prodotto in formato DXF).

## Ruoli e Permessi
*   **Cliente:**
    *   Può creare e visualizzare i proprii preventivi.
    *   Può modificare il proprio profilo e il logo aziendale.
    *   Può visualizzare e scaricare le schede tecniche.
*   **Admin:**
    *   Può fare tutto ciò che fa il Cliente.
    *   Può gestire la lista utenti attivi, bloccarli/sbloccare e cancellarli.
    *   Può gestire i prodotti, i listini prezzi e le schede tecniche.
*   **Management:**
    *   È l'unico ruolo che non può essere modificato o cancellato da se stesso (per sicurezza).

## Funzionalità Implementate (Checklist)

### ✅ Gestione Utenti
- [x] Registrazione utente con dati aziendali.
- [x] Creazione automatica scheda Cliente.
- [x] Login e Logout sicuri.
- [x] Dashboard con riepilogo dati e messaggi di benvenuto casuali.
- [x] Pannello "Gestisci Utenti" per approvare, bloccare, sbloccare e cancellare utenti.
- [x] Modifica completa dei dati utente e del profilo.
- [x] Upload del logo aziendale nel profilo.
- [x] **Correzione bug pagina modifica profilo:** Risolto l'errore "Cannot GET /profile/edit" aggiungendo la rotta mancante.

### ✅ Gestione Preventivi (Cantieri/Preventivi)
- [x] Creazione di un nuovo preventivo/cantiere.
- [x] Creazione unificata: il preventivo viene automaticamente associato all'azienda dell'utente loggato.
- [x] Lista preventivi con permessi basati sul ruolo.
- [x] Pagina di dettaglio per ogni preventivo con tutti i dati, articoli e riepilogo costi.
- [x] **Sistema di Calcolo Avanzato:** Il form per aggiungere articoli usa un mini-configuratore che seleziona Prodotto, Colore e Misure e calcola il prezzo in tempo reale dalla griglia prezzi.
- [x] **CRUD Completo Articoli:** Implementato un sistema completo per Creare, Leggere, Aggiornare ed Eliminare (CRUD) gli articoli del preventivo.
- [x] **Selezione Visiva Articoli:** Nuovo sistema per aggiungere articoli tramite una selezione visiva basata su disegni SVG dei prodotti.
- [x] **Memoria Filtri:** Il sistema ricorda l'ultima selezione di `serie` e `gruppo` per ogni preventivo, velocizzando l'inserimento di articoli multipli.
- [x] **Correzione associazione cliente:** Risolto il problema "Cliente: null" usando `COALESCE` per recuperare sempre la ragione sociale corretta.
- [x] **Correzione redirect creazione preventivo:** Dopo la creazione, l'utente viene reindirizzato correttamente alla pagina di dettaglio del nuovo preventivo.

### ✅ Gestione Prodotti (Catalogo)
- [x] **CRUD Completo:** Creazione, Lettura, Modifica ed Eliminazione (CRUD) dei prodotti/servizi.
- [x] **Pagina Elenco Prodotti:** Dashboard di gestione con filtri dinamici per `Serie` e `Gruppo`.
- [x] **Pagina Dettaglio Prodotto:** Pagina dedicata per ogni singolo prodotto.

### ✅ Gestione Listini (Listino Prezzi)
- [x] **Interfaccia Ristrutturata:** Selezione di Prodotto e Variante Colore tramite menu a tendina.
- [x] **Importazione Excel:** Funzionalità robusta per caricare interi listini da file Excel. Il sistema cancella i prezzi esistenti e inserisce quelli nuovi.
- [x] **Gestione Errori:** Il sistema gestisce con eleganza file vuoti, celle non numeriche e altri problemi comuni.

### ✅ Gestione Documenti (Schede Tecniche)
- [x] **Upload File PDF:** Sistema per l'upload e la gestione dei documenti PDF.
- [x] **Download Sicuro:** Download sicuro dei file per gli utenti autorizzati.
- [x] **Ordinamento Drag-and-Drop:** Funzionalità avanzata per riordinare i documenti tramite trascinamento.
- [x] **Conversione DXF in SVG:** I file `.dxf` standard del settore vengono automaticamente convertiti in `.svg` per l'anteprima web.

### ✅ Generazione PDF Preventivi
- [x] **Contenuti Dinamici:** Il PDF generato include dati preventivo, dati cliente, riepilogo costi completo con IVA, sconti e costi aggiuntivi.
- [x] **Logo Aziendale:** Il PDF include automaticamente il logo dell'azienda dell'utente, se caricato.
- [x] **Download Diretto:** L'utente può scaricare istantaneamente il PDF generato.

### ✅ Miglioramenti UI/UX
- [x] **Animazioni Pagine di Accesso:** Implementazione di animazioni personalizzate con sagome di finestre fluttuanti sulle pagine di login e registrazione per riflettere l'identità del brand KPX.
- [x] **Layout Sidebar:** Correzione del layout della sidebar per un corretto posizionamento del pulsante di logout e una gestione pulita dei permessi visivi.
- [x] **Evidenziazione Link Attivo:** Aggiunta di una classe CSS per evidenziare il link alla pagina corrente nella barra di navigazione.

---

## Prossimi Passi (Da Fare Subito)

1.  **Invio Email Preventivo:**
    *   [ ] Integrare un servizio di invio email (es. Nodemailer) per inviare automaticamente il PDF del preventivo al cliente.
    *   [ ] Creare un sistema di notifiche per avvisare l'admin di nuovi preventivi o richieste di contatto.

2.  **Statistiche e Report:**
    *   [ ] Creare una dashboard con grafici (es. Chart.js) per analizzare i dati dei preventivi (per mese, per stato, per consulente).
    *   [ ] Generazione report esportabili in Excel o PDF per l'amministrazione.

3.  **Creazione Ruolo 'Agente':**
    *   [ ] Definire un nuovo ruolo 'Agente' con permessi limitati.
    *   [ ] Creare un sistema per assegnare i clienti agli agenti.
    *   [ ] Gli agenti possono vedere e creare preventivi solo per i proprii clienti assegnati.

---

## Idee Future (Da Fare Dopo)

- [ ] **Integrazione con Software Esterno:** Collegare l'applicazione a gestionali esistenti (es. Zucchetti, software per la contabilità) tramite l'importazione/esportazione di file Excel.
- [ ] **Sistema di Preventivazione Guidata:** Evolvere l'attuale sistema di calcolo basato su griglia in un configuratore visuale più avanzato, dove l'utente seleziona prodotti e opzioni e il sistema calcola il prezzo in tempo reale.
- [ ] **Gestione Multi-Lingua:** Tradurre l'interfaccia e permettere la selezione della lingua (es. Italiano, Inglese) per un mercato più ampio.
- [ ] **Area Clienti Self-Service:** Creare un'area riservata dove i clienti possono accedere per visualizzare i proprii preventivi, lo stato degli ordini e scaricare i documenti.

---

## Note Aggiuntive

-   **Stack Tecnologico:** Lo stack attuale (HTML, CSS, JS) è stato scelto per la sua velocità di sviluppo e per la facilità di manutenzione. Un futuro refactoring con un framework come Tailwind CSS potrebbe migliorare la scalabilità del progetto.
-   **Design del Database:** Lo schema relazionale è stato progettato per essere flessibile e scalabile, utilizzando tabelle separate con chiavi esterne per mantenere l'integrità dei dati.