---
name: flashcard-primaria
description: Crea flash card di ripasso per bambini della primaria dalle pagine di un libro di testo in PDF, come file JSON per il repository primariaflash_assets di Primaria Flash, e apre una pull request.
---

# Flash card per Primaria Flash da un libro in PDF

Usa questa procedura quando l'utente carica un PDF di un libro scolastico e chiede le flash card (o le domande "tipo interrogazione") per un intervallo di pagine. Il pubblico è un bambino di 8–11 anni. Le carte vanno nel sito **Primaria Flash** (primariaflash.netlify.app), che legge i contenuti come file JSON da questo repository, **primariaflash_assets** (GitHub `vlastecoding/primariaflash_assets`, pubblicato con GitHub Pages).

Tutti i percorsi qui sotto sono relativi alla radice di questo repository. Prima di scrivere, leggi sempre il `README.md`: è la fonte di verità sul formato. Se differisce da quanto scritto qui, vale il README.

## 0. Preparare il branch

Le modifiche arrivano su `main` solo con una pull request, approvata dal proprietario del repository.

1. `git status`: se ci sono modifiche non tue, fermati e chiedi.
2. Aggiorna `main` (`git switch main && git pull`) e crea un branch `deck/{classe}-{materia}-{mazzo}` (es. `deck/quarta-geografia-mari`). Se il mazzo esiste già e aggiungi carte, va bene lo stesso nome.

## 1. Capire dove va il contenuto

- **Classe**: quella del libro, non quella attuale del bambino (es. libro di 4ª → `quarta`, anche se oggi è in quinta). Le classi sono già tutte in `classes.json` (`prima` … `quinta`).
- **Materia**: se esiste già (`classes/{classe}/subjects/{materia}.json`) aggiungi il mazzo alla sua lista `decks`; altrimenti creala (vedi §6).
- **Mazzo**: di solito un capitolo del libro = un mazzo. Id brevi in minuscolo con lettere, cifre e `-` (es. `corpo`, `fenici`). `ripasso` è riservato.
- Se classe o materia non sono chiare, chiedi all'utente.

## 2. Trovare le pagine giuste nel PDF

Il numero stampato sulla pagina spesso NON coincide con il numero di pagina del PDF. I libri sono spesso scansionati (niente testo estraibile), quindi si lavora sulle immagini con lo script `.claude/skills/flashcard-primaria/scripts/pages.py`, che usa PyMuPDF.

1. Se PyMuPDF non c'è, crealo in un ambiente a parte, fuori dal repository (es. nella cartella temporanea): `python3 -m venv <tmp>/venv && <tmp>/venv/bin/pip install pymupdf pillow`. Non installare pacchetti nel sistema e non aggiungere file al repository.
2. Anteprima di una zona di pagine: `python pages.py grid libro.pdf 70 79 <tmp>/griglia.png`, poi guardala con Read.
3. Leggi il numero stampato e calcola lo scarto (es. pagina stampata 6 = pagina PDF 8, scarto +2). Controlla se una pagina del PDF è una pagina singola o una doppia pagina affiancata.
4. Renderizza solo le pagine richieste: `python pages.py render libro.pdf 74 <tmp>/img` crea due metà leggibili (`p74_0.png`, `p74_1.png`); guardale con Read. Gli estremi indicati dall'utente sono compresi ("da 102 a 108" include 102 e 108).

Le immagini restano nella cartella temporanea: non vanno nel repository.

## 3. Leggere tutta la pagina, non solo il testo principale

- i paragrafi con il loro titolo (diventano i `topics`);
- i box ("A colpo d'occhio", "Curiosità", "Imparo con le parole", "Tecnologia", "Metodo di studio", "Strategia");
- le didascalie di foto e disegni, le carte geografiche e le loro legende, le linee del tempo, gli schemi;
- gli esercizi del libro ("Imparo con la carta/il testo/l'immagine", tabelle da completare): trasformali in domande, anche "al contrario" (dalla tabella funzione→apparato nasce "Quale apparato ci fornisce energia?").

## 4. Scrivere le carte

Circa 7–10 carte per pagina di libro, coprendo ogni concetto in grassetto, ogni data, ogni nome e ogni parola nuova.

**`question`**: testo semplice (niente HTML), breve e diretta, come la farebbe la maestra all'interrogazione. Può chiedere due cose collegate ("Quando e perché…?").

**`answer`**: corta, con le parole chiave in `<b>…</b>`. Per elenchi o sequenze usa `<br>` oppure `<ol><li>…</li></ol>`. Solo questi tag. Le date con "a.C.".

**`explanation`** (pulsante *Spiegamelo meglio*): 2–3 frasi rivolte al bambino ("tu"), con parole semplici, **autosufficienti**. NON citare foto, disegni, cartine, tabelle o pagine del libro ("guarda la foto…", "a pagina 9…"): l'app non le mostra. Usa a seconda dei casi:
- un paragone concreto ("è come un'orchestra", "come le piastrelle di un pavimento", "come una bolla di chewing-gum");
- un trucco per ricordare (acronimi, frasi tipo "Nonna Emma Mangia Ciliegie");
- il significato delle parole difficili o di origine greca (talassocrazia = thàlassa + kratìa);
- un collegamento con altri mazzi già presenti (es. il re fenicio decideva con l'assemblea, quello cretese aveva potere assoluto).
Aggiungi solo fatti sicuri e di cultura generale; non inventare dettagli che il libro non dice e che non sono certi.

**`page`**: il numero di pagina stampato da cui viene la carta (resta nei dati anche se oggi l'app non lo mostra).

**`topic`**: id di uno dei `topics` del mazzo. 3–7 argomenti per mazzo, di solito uno per paragrafo o gruppo di paragrafi del libro.

## 5. Regole sui contenuti

- Non copiare MAI il testo del libro parola per parola: riformula sempre con parole tue, anche nelle risposte. Se l'utente chiede di riportare il testo del libro "verbatim", spiega che non si può (diritto d'autore, sito pubblico) e offri una riformulazione.
- Linguaggio inclusivo e adatto ai bambini ("un genitore", "ragazzi e ragazze").
- Niente emoji nei contenuti.
- Non mettere nel repository il PDF del libro né le immagini delle pagine.

## 6. Formato dei file (JSON, UTF-8, indentazione 2 spazi)

**Mazzo** — `classes/{classe}/subjects/{materia}/decks/{mazzo}.json`:

```json
{
  "id": "corpo",
  "name": "Il corpo umano",
  "pages": "6–9",
  "blurb": "Apparati e sistemi, organi, tessuti e i diversi tipi di cellule.",
  "color": "sci",
  "icon": "<svg viewBox=\"0 0 64 64\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"3\" stroke-linecap=\"round\" stroke-linejoin=\"round\">…</svg>",
  "topics": [
    { "id": "apparati", "name": "Apparati e sistemi" }
  ],
  "cards": [
    {
      "topic": "apparati",
      "page": 6,
      "question": "Che cos'è un apparato (o sistema)?",
      "answer": "Un <b>insieme di organi</b> collegati tra loro per svolgere le <b>funzioni vitali</b>.",
      "explanation": "Un organo da solo non basta. Per mangiare, per esempio, servono bocca, stomaco, intestino e altri ancora: tutti insieme formano l'apparato digerente."
    }
  ]
}
```

- `pages`: intervallo con il trattino lungo `–`.
- `blurb`: una riga che riassume il capitolo.
- `color`: uno tra `porpora`, `egeo`, `cedro`, `sci`, `sto`, `mix`. Scegline uno diverso dai mazzi vicini della stessa materia quando ha senso.
- `icon`: SVG semplice a tratto, `viewBox="0 0 64 64"`, `stroke="currentColor"`, legato al tema (toro, nave, cuore…).

**Materia nuova** — `classes/{classe}/subjects/{materia}.json` con `id`, `name`, `book` (es. "Dal libro di Scienze e Tecnologia di 5ª."), `blurb`, `unit` (`{"singular": "argomento", "plural": "argomenti"}`), `color`, `icon`, `decks`; poi aggiungi l'id della materia alla lista `subjects` della classe in `classes.json`.

**Mazzo nuovo in materia esistente**: crea il file del mazzo e aggiungi il suo id alla lista `decks` della materia; aggiorna anche il `blurb` della materia se ora non la descrive più.

Il Super Ripassone, i conteggi e la ricerca sono calcolati dall'app: non servono altri file.

## 7. Controlli prima di consegnare

1. JSON valido (`python3 -m json.tool file.json`).
2. Ogni carta ha `topic`, `page`, `question`, `answer`, `explanation`; ogni `topic` esiste nei `topics`; nessun argomento resta vuoto.
3. Nessuna `explanation` cita foto, immagini, cartine, tabelle o pagine (cerca parole come "foto", "guarda", "disegno", "cartina", "pagina", "pag.").
4. Gli id del mazzo e della materia compaiono nelle liste del livello superiore.
5. Rileggi le carte confrontandole con le immagini delle pagine: date, nomi e numeri devono corrispondere al libro.
6. Aggiorna la tabella "Content" nel `README.md` di questo repository con mazzo, numero di carte e argomenti.
7. Prova in locale, se si può (vedi "Previewing changes" nel README): se accanto a questo repository c'è il clone dell'app (`../primariaflash/serve.sh` esiste) con il collegamento `primariaflash_assets`, lancia `../primariaflash/serve.sh local` in background e apri `http://localhost:8000/?api=local#/{classe}/{materia}/{mazzo}`: gira qualche carta, apri *Spiegamelo meglio*, prova il Super Ripassone. Altrimenti salta questo passo e dillo all'utente. Dopo la PR, ricorda all'utente che può controllarla sul sito con `https://primariaflash.netlify.app/?branch={branch}`.

## 8. Pull request

Fai commit e PR solo dopo che l'utente ha visto il riepilogo (§9) e ha detto di procedere.

1. Aggiungi solo i file dei contenuti e il `README.md` (`git add classes.json classes/… README.md`), mai PDF, immagini o file temporanei.
2. Commit con un messaggio breve in inglese, come quelli nel `git log` (es. "Add I mari e le coste deck to Geografia (4ª), 40 cards").
3. `git push -u origin <branch>`, poi `gh pr create --base main` con un titolo uguale al commit e nella descrizione: libro e pagine, classe/materia/mazzo, numero di carte per argomento, eventuali dubbi da controllare sul libro. Se l'utente non ha accesso in scrittura al repository, `gh` propone di fare un fork: accetta.
4. Non fare mai push su `main` e non fare il merge della PR: lo fa il proprietario del repository. Dopo il merge le modifiche arrivano sul sito in circa 10 minuti, senza nuovo deploy dell'app.

## 9. Cosa dire all'utente

In breve: quante carte, divise in quali argomenti, in quale classe e materia, quali file sono stati creati o modificati, eventuali punti da controllare sul libro, e il link della PR (o che manca ancora).
