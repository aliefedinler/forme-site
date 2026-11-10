# FORME SPORT — Pacchetto per clothingforme.com

Questo ZIP aggiunge una **pagina FORME SPORT** al repository `aliefedinler/forme-site` senza cancellare la collezione originale. È la versione approvata del mockup **senza la barra “Performance / Breathable / Versatile / Timeless”**.

## Cosa contiene

- `sport.html`: pagina completa FORME SPORT con banner sul campo da calcio, cinque capi, prezzi illustrativi, pulsanti “View details” funzionanti, layout responsive.
- `assets/forme-sport/`: sei immagini WebP ottimizzate (campagna + prodotti).
- `apply_forme_sport.py`: script facoltativo che aggiunge sul sito attuale un link FORME SPORT nell'header e nel footer, più un banner di lancio sulla homepage.
- `INIZIA-QUI.txt`: istruzioni rapide.

## Metodo 1: caricamento sul repository dal browser GitHub

1. **Estrai lo ZIP** sul computer. Non caricare il file ZIP come singolo allegato nel repository: GitHub non lo decomprime automaticamente.
2. Apri https://github.com/aliefedinler/forme-site e crea, se possibile, un nuovo branch dall'attuale `main`.
3. Premi **Add file → Upload files**. Trascina il file `sport.html` e la cartella `assets/forme-sport/` (mantenendo le sottocartelle). Non eliminare/sostituire le altre immagini in `assets/`.
4. Nel file `index.html` premi la matita **Edit**. Cerca nella barra di navigazione la riga:
   `<li><a href="#collection">Collection</a></li>`
   Subito dopo aggiungi:
   `<li><a href="sport.html">Forme Sport</a></li>`
5. Scorri alla sezione del footer nel medesimo `index.html`; dopo `<a href="#collection">Collection</a>` aggiungi:
   `<a href="sport.html">Forme Sport</a>`
6. Salva le modifiche. La nuova pagina sarà raggiungibile a `https://clothingforme.com/sport.html` **dopo il deploy**, se il sito è collegato al repository.

Con il metodo 1, la pagina FORME SPORT e i collegamenti sono attivi, **ma non il banner promozionale aggiuntivo sulla homepage**. Per avere anche il banner usa il metodo 2.

## Metodo 2: integrazione completa con un comando

Se lavori con il repository sul tuo computer o in GitHub Codespaces:

1. Estrai lo ZIP **nella radice del repository**, dove si trova già `index.html`. Aggiungi/mergia la cartella `assets`; non sostituirla integralmente.
2. Da un terminale aperto nella radice del repository, esegui: `python3 apply_forme_sport.py`.
3. Lo script inserisce automaticamente link nel menu e nel footer, **più il banner FORME SPORT sulla homepage**. Tutto il resto del vecchio sito rimane inalterato.
4. Controlla le modifiche (git diff), poi fai commit e push, idealmente su un branch dedicato, e apri una Pull Request.

Per vedere la pagina prima della pubblicazione, esegui `python3 -m http.server 8000` e visita `http://localhost:8000/sport.html`.

## Note

- FORME SPORT è una collezione dimostrativa/accademica; **non sono disponibili acquisti**. I prezzi sono soltanto esempi.
- Le immagini sono concept/mockup, non fotografie di prodotti reali già in commercio.
- Il file `sport.html` è autonomo, non modifica né avvia il sistema di cookie, analytics o pubblicità della homepage. Se vuoi tracciare gli accessi a questa pagina con GA4, bisogna estendere l'integrazione nel rispetto della scelta sui cookie.
- **Non ho modificato direttamente `main`**: questo ZIP serve per l'importazione da parte tua.
