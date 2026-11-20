"""Baut die drei Kopiervorlagen als einzelne A4-PDFs für den Download auf der Website."""
import sys, os, io
sys.path.insert(0, "/home/claude/buch")
from reportlab.platypus import Paragraph, PageBreak, Spacer

_oi = Paragraph.__init__


def _ni(self, text, style=None, bulletText=None, *a, **k):
    self._raw = text
    _oi(self, text, style, bulletText, *a, **k)


Paragraph.__init__ = _ni

from booklib import *            # noqa
import anhang as AN
from pypdf import PdfReader, PdfWriter, Transformation, PageObject
from reportlab.lib.pagesizes import A4

OUT = "/home/claude/lp/pdf"
os.makedirs(OUT, exist_ok=True)
TMP = "/tmp/claude-0/vorlagen"
os.makedirs(TMP, exist_ok=True)

FOOT = ("Kopiervorlage aus: Sebastian Klatt, „Verbieten reicht nicht – Handy weg, und dann?“, Band 1. "
        "Das Kopieren für Familie, Schule und Elternarbeit ist ausdrücklich erlaubt. "
        "Mehr Material: verbietenreichtnicht.de")

TITLES = {
    "B1": ("Mediennutzungsvertrag", "Unser_Mediennutzungsvertrag"),
    "B2": ("Klassenchat-Regeln", "Unsere_Klassenchat-Regeln"),
    "B3": ("Elternbrief zur Handyregel", "Elternbrief_zur_Handyregel"),
}


def groups():
    """Teilt kopiervorlagen() an den Seitenumbrüchen in die einzelnen Vorlagen."""
    flow = AN.kopiervorlagen()
    parts, cur = [], []
    for f in flow:
        if isinstance(f, PageBreak):
            if cur:
                parts.append(cur)
            cur = []
            continue
        if type(f).__name__ in ("NextPageTemplate", "SetHead"):
            continue
        cur.append(f)
    if cur:
        parts.append(cur)
    # die erste Gruppe ist die Einleitungsseite des Anhangs
    out = {}
    for g in parts:
        key = None
        for f in g:
            raw = getattr(f, "_raw", "")
            if isinstance(raw, str) and raw.startswith("KOPIERVORLAGE "):
                key = raw.split()[-1]
                break
        if key in TITLES:
            out[key] = g
    return out


def render(key, flow):
    """Setzt eine Vorlage auf Buchformat und skaliert sie anschließend auf A4."""
    small = f"{TMP}/{key}.pdf"
    doc = BaseDocTemplate(small, pagesize=(PW, PH), initialFontName="Cal",
                          title=f"{TITLES[key][0]} – Verbieten reicht nicht",
                          author="Sebastian Klatt")
    fr = Frame(INNER, BOTTOM, TW, PH - TOP - BOTTOM + 10 * mm, id="v",
               leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
    doc.addPageTemplates([PageTemplate("v", [fr])])
    story = []
    for f in flow:
        raw = getattr(f, "_raw", "")
        if isinstance(raw, str) and raw.startswith("Kopiervorlage aus:"):
            story.append(Paragraph(FOOT, f.style))
        else:
            story.append(f)
    doc.build(story)
    n = len(PdfReader(small).pages)
    assert n == 1, f"{key} hat {n} Seiten"

    src = PdfReader(small).pages[0]
    w, h = float(src.mediabox.width), float(src.mediabox.height)
    aw, ah = A4
    s = min((aw - 40) / w, (ah - 56) / h)
    page = PageObject.create_blank_page(width=aw, height=ah)
    page.merge_transformed_page(src, Transformation().scale(s, s)
                                .translate((aw - w * s) / 2, (ah - h * s) / 2))
    out = f"{OUT}/{TITLES[key][1]}.pdf"
    wr = PdfWriter()
    wr.add_page(page)
    wr.add_metadata({"/Title": f"{TITLES[key][0]} – Verbieten reicht nicht",
                     "/Author": "Sebastian Klatt",
                     "/Subject": "Kopiervorlage aus Band 1. Kopieren für Familie, Schule und "
                                 "Elternarbeit erlaubt."})
    with open(out, "wb") as fh:
        wr.write(fh)
    return out


if __name__ == "__main__":
    gs = groups()
    assert set(gs) == set(TITLES), sorted(gs)
    for k in ("B1", "B2", "B3"):
        p = render(k, gs[k])
        print(k, p, os.path.getsize(p) // 1024, "KB")
