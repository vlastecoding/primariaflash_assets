"""Immagini delle pagine di un PDF, per leggere i libri scansionati.

  python pages.py grid   libro.pdf DA A uscita.png   anteprima piccola delle pagine DA..A in una griglia
  python pages.py render libro.pdf PAGINA cartella    una pagina leggibile, in due metà (pPAGINA_0.png, pPAGINA_1.png)

I numeri sono quelli del PDF (dalla 1), non quelli stampati sulla pagina.
Serve PyMuPDF: pip install pymupdf pillow
"""
import sys
from pathlib import Path

import fitz
from PIL import Image


def grid(pdf, first, last, out, cols=5):
    doc = fitz.open(pdf)
    ims = []
    for n in range(first, last + 1):
        p = doc[n - 1].get_pixmap(dpi=25)
        ims.append(Image.frombytes("RGB", (p.width, p.height), p.samples))
    w = max(im.width for im in ims)
    h = max(im.height for im in ims)
    rows = (len(ims) + cols - 1) // cols
    sheet = Image.new("RGB", (w * cols, h * rows), "white")
    for k, im in enumerate(ims):
        sheet.paste(im, ((k % cols) * w, (k // cols) * h))
    Path(out).parent.mkdir(parents=True, exist_ok=True)
    sheet.save(out)


def render(pdf, page, folder, dpi=110):
    doc = fitz.open(pdf)
    r = doc[page - 1].rect
    Path(folder).mkdir(parents=True, exist_ok=True)
    # due metà che si sovrappongono un po', così nessuna riga resta tagliata
    for k, (top, bottom) in enumerate([(0, 0.52), (0.48, 1)]):
        clip = fitz.Rect(0, r.height * top, r.width, r.height * bottom)
        doc[page - 1].get_pixmap(dpi=dpi, clip=clip).save(f"{folder}/p{page}_{k}.png")


if __name__ == "__main__":
    cmd, args = sys.argv[1], sys.argv[2:]
    if cmd == "grid":
        grid(args[0], int(args[1]), int(args[2]), args[3])
    elif cmd == "render":
        render(args[0], int(args[1]), args[2])
    else:
        sys.exit(__doc__)
