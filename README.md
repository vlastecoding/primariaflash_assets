# primariaflash_assets

The content of [Primaria Flash](https://github.com/vlastecoding/primariaflash): classes, subjects, decks and cards.

The app reads these files as a **read-only REST API**. They are published with GitHub Pages, and each resource is a JSON file at the resource's path plus `.json`:

| Request | File |
|---|---|
| `GET /classes` | `classes.json` |
| `GET /classes/{class}/subjects/{subject}` | `classes/{class}/subjects/{subject}.json` |
| `GET /classes/{class}/subjects/{subject}/decks/{deck}` | `classes/{class}/subjects/{subject}/decks/{deck}.json` |

For example, `GET /classes/quarta/subjects/storia/decks/fenici` is
`https://vlastecoding.github.io/primariaflash_assets/classes/quarta/subjects/storia/decks/fenici.json`.

The plan is to replace this repository with a real backend serving the same resources. The app only needs a different base address.

After a change is merged into `main`, it reaches the site within about 10 minutes (GitHub Pages build plus browser cache). No deploy of the app is needed.

## Content

| Class | Subject | Source | Decks | Topics |
|---|---|---|---|---|
| 4ª | **Geografia** | 4th-grade textbook | I mari e le coste (40 cards) | I mari italiani · Le coste · Isole e arcipelaghi · Le attività · Il paesaggio marino |
| | **Storia** | 4th-grade textbook | I Cretesi (53 cards) | Quando e dove · Attività e commercio · Società e scrittura · La religione · Il palazzo di Cnosso |
| | | | I Fenici (58 cards) | Quando e dove · Le attività · Invenzioni · Società e religione · Empori e colonie · Le navi · La scrittura |
| 5ª | **Scienze** | 5th-grade *Scienze e Tecnologia* textbook | Il corpo umano (29 cards) | Apparati e sistemi · Organi e tessuti · I tipi di cellule |
| | | | L'apparato digerente (36 cards) | La funzione · Gli organi · I denti · La digestione · Le sostanze nutritive |
| | **Storia** | 5th-grade textbook | I Micenei (57 cards) | Quando e dove · L'organizzazione sociale · Le attività · La religione · La scrittura · La città di Micene |

Update this table in the same pull request that adds or changes a deck.

## Resources

Every fact lives in exactly one file: a class lists the ids of its subjects, a subject lists the ids of its decks, and a deck holds its cards. Card counts and the search index are computed by the app.

Ids are lowercase letters, digits and `-` (e.g. `quarta`, `storia`, `fenici`). They appear in the site addresses (`#/quarta/storia/fenici`). `ripasso` is reserved for the Super Ripassone and can't be a deck id.

### `GET /classes`

All classes, in the order shown in the app. A class with no subjects is shown as *In arrivo*.

```json
[
  { "id": "quarta", "label": "4ª", "name": "Classe quarta", "subjects": ["storia"] }
]
```

### `GET /classes/{class}/subjects/{subject}`

```json
{
  "id": "storia",
  "name": "Storia",
  "book": "Dal libro di 4ª.",
  "blurb": "Le civiltà del Mediterraneo: Cretesi e Fenici.",
  "unit": { "singular": "civiltà", "plural": "civiltà" },
  "color": "sto",
  "icon": "<svg …>…</svg>",
  "decks": ["cretesi", "fenici"]
}
```

- `book`: the line shown under the subject title.
- `unit`: what a deck is called in this subject, used in counts like "2 civiltà" or "1 argomento".
- `icon`: an inline SVG, 64×64 `viewBox`, drawn with `stroke="currentColor"` so it takes the subject color.

### `GET /classes/{class}/subjects/{subject}/decks/{deck}`

```json
{
  "id": "fenici",
  "name": "I Fenici",
  "pages": "102–108",
  "blurb": "Città-stato, porpora e vetro, navi e colonie, l'alfabeto fonetico.",
  "color": "porpora",
  "icon": "<svg …>…</svg>",
  "topics": [{ "id": "navi", "name": "Le navi" }],
  "cards": [
    {
      "topic": "navi",
      "page": 107,
      "question": "Come navigavano i Fenici all'inizio?",
      "answer": "Solo <b>di giorno</b> e <b>lungo le coste</b>.",
      "explanation": "All'inizio non volevano rischiare di perdersi: navigavano solo con la luce del giorno e restando vicino alla costa, così la vedevano sempre."
    }
  ]
}
```

- `topics`: the filter chips, in order. Each card's `topic` must be one of these ids.
- `question`: plain text.
- `answer` and `explanation`: may contain simple HTML (`<b>`, `<br>`, `<ol><li>`).
- `explanation` (shown by *Spiegamelo meglio*): written for children, and self-contained. Don't refer to photos, maps or pages of the book, because the app doesn't show them.

### Colors

`color` is one of the app's theme colors, so it works in both light and dark mode: `porpora`, `egeo`, `cedro`, `sci`, `sto`, `mix`.

## Adding content

- **A card**: add it to the deck's `cards`.
- **A deck**: create `classes/{class}/subjects/{subject}/decks/{deck}.json` and add its id to the subject's `decks`.
- **A subject**: create `classes/{class}/subjects/{subject}.json` with at least one deck, and add its id to the class's `subjects` in `classes.json`.
- **A class**: it's already in `classes.json`; giving it a subject makes it available.

## Contributing

Changes reach `main` only through pull requests, which the repository owner reviews and merges.

1. Work on a branch, e.g. `deck/quarta-geografia-mari`.
2. Add or change the files as described above, and update the [Content](#content) table.
3. Open a pull request against `main`. If you don't have write access, fork the repository first (`gh pr create` offers to do it).

Never add the textbook PDFs or images of their pages: they are copyrighted, and the cards must always be written in your own words.

### Making cards with Claude Code

The repository includes a Claude Code skill, `.claude/skills/flashcard-primaria`, that turns pages of a textbook PDF into a deck: it reads the pages (also scanned ones), writes the cards following the rules for children, checks them, and opens the pull request once you approve. Open Claude Code in this folder and run, for example:

```
/flashcard-primaria dal libro ~/Downloads/geografia4.pdf, pagine 74–76
```

The skill needs Python 3 (it installs PyMuPDF in a temporary environment) and the GitHub CLI `gh`, logged in.

### Previewing changes

**Before pushing**, with the app cloned next to this repository and linked to it (once):

```bash
cd ..
git clone https://github.com/vlastecoding/primariaflash.git
ln -s ../primariaflash_assets primariaflash/primariaflash_assets
primariaflash/serve.sh local    # opens http://localhost:8000/?api=local
```

The app then reads the files of this folder as they are on disk, e.g. `http://localhost:8000/?api=local#/quarta/geografia/mari`.

**After pushing a branch**, nothing needs to be installed: open the site with the branch in the address, e.g. `https://primariaflash.netlify.app/?branch=deck/quarta-geografia-mari`, or `?branch=user:deck/…` for a branch of a fork. With the app cloned, `primariaflash/serve.sh prod deck/quarta-geografia-mari` does the same locally.
