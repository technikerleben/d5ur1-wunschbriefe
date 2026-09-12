from pathlib import Path
import io
import fitz
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
COLLAGE = ROOT / 'materialien' / 'Collage Otterbilder Briefe.png'

BLUE = (36/255, 86/255, 136/255)
MINT = (72/255, 220/255, 203/255)
ORANGE = (240/255, 166/255, 111/255)
SOFT_BLUE = (220/255, 236/255, 248/255)
SOFT_MINT = (224/255, 247/255, 241/255)
SOFT_ORANGE = (252/255, 236/255, 222/255)
INK = (32/255, 52/255, 68/255)
WHITE = (1, 1, 1)

CROPS = [
    (0.00, 0.00, 0.34, 0.34),
    (0.33, 0.00, 0.67, 0.34),
    (0.66, 0.00, 1.00, 0.34),
    (0.00, 0.33, 0.34, 0.67),
    (0.33, 0.33, 0.67, 0.67),
    (0.66, 0.33, 1.00, 0.67),
    (0.00, 0.66, 0.34, 1.00),
    (0.33, 0.66, 0.67, 1.00),
    (0.66, 0.66, 1.00, 1.00),
]

def otter_bytes(index: int) -> bytes:
    with Image.open(COLLAGE).convert('RGB') as im:
        w, h = im.size
        l, t, r, b = CROPS[index % len(CROPS)]
        crop = im.crop((int(l*w), int(t*h), int(r*w), int(b*h)))
        gray = crop.convert('L')
        bbox = gray.point(lambda p: 0 if p > 248 else 255).getbbox()
        if bbox:
            pad = 12
            x0, y0, x1, y1 = bbox
            crop = crop.crop((max(0, x0-pad), max(0, y0-pad), min(crop.width, x1+pad), min(crop.height, y1+pad)))
        out = io.BytesIO()
        crop.save(out, format='PNG', optimize=True)
        return out.getvalue()

def add_brand(page, page_no: int, kind='a5', otter=0):
    w, h = page.rect.width, page.rect.height
    page.draw_rect(fitz.Rect(6, 6, w-6, h-6), color=BLUE, width=1.2, overlay=True)
    page.draw_line(fitz.Point(12, 72 if kind != 'a3' else 136), fitz.Point(w-12, 72 if kind != 'a3' else 136), color=BLUE, width=2.0, overlay=True)
    page.draw_line(fitz.Point(10, 10), fitz.Point(10, 44), color=ORANGE, width=3.0, overlay=True)
    page.draw_line(fitz.Point(w-10, h-44), fitz.Point(w-10, h-10), color=MINT, width=3.0, overlay=True)
    if kind == 'a5':
        page.draw_rect(fitz.Rect(12, 10, min(w-95, 155), 39), fill=SOFT_BLUE, color=None, fill_opacity=.38, overlay=True)
        page.draw_rect(fitz.Rect(12, 77, w-12, 112), fill=SOFT_MINT, color=None, fill_opacity=.16, overlay=True)
    elif kind == 'a4':
        page.draw_rect(fitz.Rect(18, 14, min(w-130, 210), 48), fill=SOFT_BLUE, color=None, fill_opacity=.35, overlay=True)
        page.draw_rect(fitz.Rect(18, 88, w-18, 128), fill=SOFT_MINT, color=None, fill_opacity=.12, overlay=True)
    elif kind == 'a3':
        page.draw_rect(fitz.Rect(26, 22, min(w-190, 330), 78), fill=SOFT_BLUE, color=None, fill_opacity=.35, overlay=True)
        page.draw_rect(fitz.Rect(26, 145, w-26, 215), fill=SOFT_MINT, color=None, fill_opacity=.12, overlay=True)
    data = otter_bytes(otter)
    if kind == 'a5':
        box = fitz.Rect(w-86, 8, w-16, 67)
    elif kind == 'a4':
        box = fitz.Rect(w-118, 8, w-20, 82)
    else:
        box = fitz.Rect(w-175, 18, w-30, 126)
    page.draw_rect(box, fill=WHITE, color=None, fill_opacity=.94, overlay=True)
    page.insert_image(box, stream=data, keep_proportion=True, overlay=True)
    label = f'Otterklasse 5.3 · grafische Druckfassung · {page_no}'
    fs = 6.5 if kind == 'a5' else (8 if kind == 'a4' else 11)
    page.insert_text(fitz.Point(16 if kind!='a3' else 30, h-10 if kind!='a3' else h-18), label, fontsize=fs, fontname='helv', color=BLUE, overlay=True)

def copy_with_design(src_path: Path, out_path: Path, kind='a5', scale_to=None):
    src = fitz.open(src_path)
    out = fitz.open()
    for i, sp in enumerate(src):
        if scale_to is None:
            pw, ph = sp.rect.width, sp.rect.height
        else:
            pw, ph = scale_to
        p = out.new_page(width=pw, height=ph)
        p.draw_rect(p.rect, fill=WHITE, color=None)
        p.show_pdf_page(p.rect, src, sp.number, keep_proportion=True)
        if kind == 'a5':
            p.draw_rect(fitz.Rect(10, ph-91, pw-10, ph-52), fill=SOFT_MINT, color=None, fill_opacity=.09, overlay=True)
            p.draw_rect(fitz.Rect(10, ph-49, pw-10, ph-12), fill=SOFT_BLUE, color=None, fill_opacity=.09, overlay=True)
        elif kind == 'a4':
            p.draw_rect(fitz.Rect(16, ph-118, pw-16, ph-70), fill=SOFT_MINT, color=None, fill_opacity=.07, overlay=True)
            p.draw_rect(fitz.Rect(16, ph-66, pw-16, ph-16), fill=SOFT_BLUE, color=None, fill_opacity=.07, overlay=True)
        add_brand(p, i+1, kind=kind, otter=i)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out.save(out_path, deflate=True, garbage=4)
    src.close()
    out.close()
    print(out_path)

def strategy_design(src_path: Path, out_path: Path):
    src = fitz.open(src_path)
    out = fitz.open()
    strip_fills = [SOFT_BLUE, SOFT_ORANGE, SOFT_MINT, (0.95, 0.90, 0.94)]
    for i, sp in enumerate(src):
        p = out.new_page(width=sp.rect.width, height=sp.rect.height)
        p.show_pdf_page(p.rect, src, sp.number)
        h = p.rect.height
        top = 18
        usable = h-36
        sh = usable/4
        for j in range(4):
            y0 = top + j*sh
            y1 = top + (j+1)*sh - 4
            p.draw_rect(fitz.Rect(10, y0, p.rect.width-10, y1), fill=strip_fills[j], color=BLUE, width=.6, fill_opacity=.10, overlay=True)
            data = otter_bytes(i*4+j)
            box = fitz.Rect(p.rect.width-68, y0+7, p.rect.width-18, y0+50)
            p.draw_rect(box, fill=WHITE, color=None, fill_opacity=.95, overlay=True)
            p.insert_image(box, stream=data, keep_proportion=True, overlay=True)
        p.insert_text(fitz.Point(18, h-8), f'Otterklasse 5.3 · Strategiekarten · grafische Druckfassung · {i+1}/2', fontsize=7, fontname='helv', color=BLUE, overlay=True)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out.save(out_path, deflate=True, garbage=4)
    src.close()
    out.close()
    print(out_path)

def main():
    A5 = fitz.paper_size('a5')
    copy_with_design(
        ROOT/'materialien/arbeitsblaetter/Mein_Lernweg.pdf',
        ROOT/'materialien/arbeitsblaetter/Mein_Lernweg_grafisch_A5.pdf',
        kind='a5', scale_to=A5)
    copy_with_design(
        ROOT/'materialien/arbeitsblaetter/Arbeitsblaetter_1-24_DIN_A5_ueberarbeitet.pdf',
        ROOT/'materialien/arbeitsblaetter/Arbeitsblaetter_1-24_DIN_A5_grafisch.pdf',
        kind='a5')
    A3 = fitz.paper_size('a3')
    copy_with_design(
        ROOT/'materialien/merkblaetter/Merkblaetter_Wunschbriefe_DIN_A5_Mathe_angepasst.pdf',
        ROOT/'materialien/merkblaetter/Merkblaetter_Wunschbriefe_A3_grafisch.pdf',
        kind='a3', scale_to=A3)
    strategy_design(
        ROOT/'materialien/strategiekarten/Strategiekarten_Lernbuddy_Querstreifen_8_Karten.pdf',
        ROOT/'materialien/strategiekarten/Strategiekarten_Lernbuddy_Querstreifen_grafisch.pdf')
    copy_with_design(
        ROOT/'materialien/probearbeit/Probearbeit_Wunschbrief_Komplettpaket.pdf',
        ROOT/'materialien/probearbeit/Probearbeit_Wunschbrief_grafisch.pdf',
        kind='a4')
    copy_with_design(
        ROOT/'materialien/projekte/Freiwillige_Projekte_Wunschbriefe_DIN_A5.pdf',
        ROOT/'materialien/projekte/Freiwillige_Projekte_Wunschbriefe_DIN_A5_grafisch.pdf',
        kind='a5')

if __name__ == '__main__':
    main()
