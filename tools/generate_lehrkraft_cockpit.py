from pathlib import Path
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A3, landscape
from reportlab.lib.colors import HexColor
from reportlab.lib.units import mm
from reportlab.pdfbase.pdfmetrics import stringWidth

OUT = Path("materialien/lehrkraft/Lehrkraft_Cockpit_Wunschbriefe_A3.pdf")
OUT.parent.mkdir(parents=True, exist_ok=True)

SLATE = HexColor("#3E5668")
RUST = HexColor("#D97A4A")
SAGE = HexColor("#7DBB6F")
INK = HexColor("#24313A")
MUTED = HexColor("#68757D")
LINE = HexColor("#CBD4D9")
LIGHT = HexColor("#F5F4F1")
LIGHT_BLUE = HexColor("#EEF2F4")
LIGHT_GREEN = HexColor("#F0F6EE")
LIGHT_RUST = HexColor("#FBF2EC")
WHITE = HexColor("#FFFFFF")

rows = [
    (1, "Unsere Wünsche für die neue Schule", "Schreibanlass verstehen; Wünsche sammeln", "Auftrag klären", "Pflicht", "Input 1", "Kiosk / Austausch"),
    (2, "Mein Lernweg", "Lernweg und Ziel der Reihe verstehen", "Lernziel setzen", "Pflicht", "Input 1", "Lernweg"),
    (3, "Wünsche für unsere Schule", "passende Schulwünsche entwickeln", "Auftrag klären", "Pflicht", "Input 1", "Kiosk"),
    (4, "Wer schreibt wem?", "Schreibsituation und Empfänger erkennen", "Beispiel nutzen", "Pflicht", "Input 1", "Kiosk"),
    (5, "Wer kann dabei helfen?", "passenden Empfänger auswählen", "Beispiel nutzen", "Pflicht", "Input 1", "Kiosk"),
    (6, "Was ist der Wunsch?", "Wunsch erkennen und eindeutig benennen", "Auftrag klären", "Pflicht", "Input 1", "Kiosk"),
    (7, "Die Teile eines Briefes", "Briefteile kennen und zuordnen", "Beispiel nutzen", "Pflicht", "Input 2", "Kiosk / Merkblatt"),
    (8, "Das Briefpuzzle", "Briefteile sinnvoll ordnen", "Beispiel nutzen", "Pflicht", "Input 2", "Kiosk"),
    (9, "Anrede und Grußformel", "Anrede und Gruß passend wählen", "Beispiel nutzen", "Pflicht", "Input 2", "Kiosk / Merkblatt"),
    (10, "Fehlerwerkstatt Briefaufbau", "Fehler im Briefaufbau erkennen", "Mit Kriterien prüfen", "Pflicht", "Input 2", "Kiosk"),
    (11, "Freundlich und genau", "Wünsche adressatengerecht formulieren", "Mit Kriterien prüfen", "Pflicht", "Input 3", "Kiosk"),
    (12, "Satzstarter für Wunschbriefe", "Formulierungshilfen sinnvoll einsetzen", "Beispiel nutzen", "Pflicht", "Input 3", "Kiosk / Merkblatt"),
    (13, "Mein Wunsch für den Schulalltag", "eigenen Wunsch klar formulieren", "Lernziel setzen", "Pflicht", "Input 3", "Kiosk"),
    (14, "Einen Grund ergänzen", "einen passenden Grund ergänzen", "Beispiel nutzen", "Noch einen Schritt", "Input 3", "Kiosk"),
    (15, "Auf ein Bedenken eingehen", "Bedenken aufgreifen; Lösung anbieten", "Beispiel nutzen", "Für Entdecker", "Input 3", "Kiosk"),
    (16, "Mein Schreibplan", "Inhalte vor dem Schreiben planen", "Arbeit in Schritte teilen", "Pflicht", "Input 4", "Schreibplan"),
    (17, "Mein Briefgerüst", "Brief strukturiert vorbereiten", "Arbeit in Schritte teilen", "Pflicht", "Input 4", "Kiosk / Merkblatt"),
    (18, "Mein erster Wunschbrief", "vollständigen Wunschbrief schreiben", "Zwischenstopp machen", "Pflicht", "Input 4", "Kiosk / Peer"),
    (19, "Checkliste Wunschbrief", "eigenen Text systematisch prüfen", "Mit Kriterien prüfen", "Pflicht", "Input 4", "Checkliste"),
    (20, "Mein Brief wird besser", "Text gezielt überarbeiten", "Mit Kriterien prüfen", "Pflicht", "Input 4", "Vorher/Nachher"),
    (21, "Meine Probearbeit", "Wunschbrief selbstständig verfassen", "Auftrag + Zwischenstopp", "Pflicht, unbenotet", "Input 5", "Rückmeldung"),
    (22, "Bin ich bereit?", "Prüfungsreife realistisch einschätzen", "Lernprozess reflektieren", "Pflicht", "Input 5", "Kriterien / Feedback"),
    (23, "Mein Übungsweg bis zur Arbeit", "passende weitere Übung auswählen", "Lernziel setzen", "Pflicht", "Input 5", "Lernweg / Coaching"),
    (24, "Mein Rückblick auf das Prüfungsfenster", "Lernprozess nach der LEK auswerten", "Lernprozess reflektieren", "Pflicht nach LEK", "nach LEK", "Reflexion"),
]

intro_steps = [
    ("Start", "Auftrag klären", "bei Blatt 1"),
    ("Start", "Lernziel setzen", "bei Blatt 2"),
    ("1. Lernzeit", "Hilfekette nutzen", "mit dem Lernbuddy"),
    ("Briefaufbau", "Beispiel nutzen", "ab Blatt 7"),
    ("Schreibplanung", "Arbeit in Schritte teilen", "ab Blatt 16"),
    ("Eigener Text", "Zwischenstopp machen", "ab Blatt 18"),
    ("Überarbeitung", "Mit Kriterien prüfen", "ab Blatt 19"),
    ("Prüfungsreife", "Lernprozess reflektieren", "ab Blatt 22"),
]

PAGE_W, PAGE_H = landscape(A3)

def wrap(text, font, size, maxw):
    words = text.split()
    lines, cur = [], ""
    for word in words:
        test = word if not cur else cur + " " + word
        if stringWidth(test, font, size) <= maxw:
            cur = test
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines

def text_in_cell(c, text, x, y, w, h, font="Helvetica", size=7.6, color=INK, max_lines=2):
    lines = wrap(text, font, size, w - 3*mm)
    s = size
    while len(lines) > max_lines and s > 6.3:
        s -= 0.3
        lines = wrap(text, font, s, w - 3*mm)
    c.setFillColor(color)
    c.setFont(font, s)
    line_h = s + 1.2
    total_h = len(lines[:max_lines]) * line_h
    yy = y + (h + total_h)/2 - line_h + 0.5
    for line in lines[:max_lines]:
        c.drawString(x + 1.5*mm, yy, line)
        yy -= line_h

c = canvas.Canvas(str(OUT), pagesize=landscape(A3))
c.setTitle("Lehrkraft-Cockpit - Wunschbriefe")
c.setAuthor("Deutsch 5")
margin = 10*mm

c.setFillColor(SLATE)
c.setFont("Helvetica-Bold", 24)
c.drawString(margin, PAGE_H - 18*mm, "LEHRKRAFT-COCKPIT · WUNSCHBRIEFE")
c.setFillColor(MUTED)
c.setFont("Helvetica", 9.5)
c.drawString(margin, PAGE_H - 24*mm, "Deutsch 5 · fachlicher Lernweg und SRL-Steuerung auf einen Blick")

goal_x = PAGE_W - margin - 118*mm
goal_y = PAGE_H - 31*mm
goal_w = 118*mm
goal_h = 20*mm
c.setStrokeColor(SLATE)
c.setLineWidth(1)
c.roundRect(goal_x, goal_y, goal_w, goal_h, 3*mm, stroke=1, fill=0)
c.setFillColor(SLATE)
c.setFont("Helvetica-Bold", 7.8)
c.drawString(goal_x + 4*mm, goal_y + 14.2*mm, "ZIEL DER REIHE")
c.setFillColor(INK)
c.setFont("Helvetica", 8.4)
goal = "Ich kann einen Brief schreiben und darin einen Wunsch für unseren Schulalltag freundlich und verständlich äußern."
gy = goal_y + 9.5*mm
for line in wrap(goal, "Helvetica", 8.4, goal_w - 8*mm)[:2]:
    c.drawString(goal_x + 4*mm, gy, line)
    gy -= 4.1*mm

strip_y = PAGE_H - 55*mm
strip_h = 18*mm
c.setFillColor(LIGHT)
c.setStrokeColor(LINE)
c.roundRect(margin, strip_y, PAGE_W - 2*margin, strip_h, 2*mm, stroke=1, fill=1)
c.setFillColor(SLATE)
c.setFont("Helvetica-Bold", 8.2)
c.drawString(margin + 4*mm, strip_y + 12.4*mm, "SRL-STRATEGIEN SCHRITT FÜR SCHRITT EINFÜHREN")
usable_w = PAGE_W - 2*margin - 8*mm
cell_w = usable_w / 8
for i, (when, strat, where) in enumerate(intro_steps):
    x = margin + 4*mm + i*cell_w
    if i > 0:
        c.setStrokeColor(LINE)
        c.setLineWidth(.5)
        c.line(x, strip_y + 3*mm, x, strip_y + 11.2*mm)
    c.setFillColor(INK)
    c.setFont("Helvetica-Bold", 6.8)
    c.drawString(x + 1.5*mm, strip_y + 8.3*mm, strat)
    c.setFillColor(MUTED)
    c.setFont("Helvetica", 6.2)
    c.drawString(x + 1.5*mm, strip_y + 4.5*mm, f"{when} · {where}")

table_x = margin
table_y = 22*mm
table_w = PAGE_W - 2*margin
table_top = strip_y - 5*mm
table_h = table_top - table_y
headers = ["Blatt", "Lernaufgabe", "Fachlicher Fokus", "SRL-Strategie", "Verbindlichkeit", "Input", "Kontrolle / Hilfe"]
col_fracs = [0.045, 0.245, 0.235, 0.17, 0.115, 0.075, 0.115]
col_w = [table_w*f for f in col_fracs]
header_h = 9*mm
row_h = (table_h - header_h) / 24

c.setFillColor(LIGHT_BLUE)
c.setStrokeColor(SLATE)
c.setLineWidth(0.8)
c.rect(table_x, table_top - header_h, table_w, header_h, stroke=1, fill=1)
xx = table_x
for h, w in zip(headers, col_w):
    c.setFillColor(SLATE)
    c.setFont("Helvetica-Bold", 7.6)
    c.drawString(xx + 1.6*mm, table_top - header_h + 3.2*mm, h)
    xx += w

y = table_top - header_h
for nr, title, focus, strategy, status, inputn, control in rows:
    y2 = y - row_h
    if "Noch einen" in status or "Entdecker" in status:
        c.setFillColor(LIGHT_GREEN)
    elif nr >= 21:
        c.setFillColor(LIGHT_RUST)
    else:
        c.setFillColor(WHITE)
    c.rect(table_x, y2, table_w, row_h, stroke=0, fill=1)
    c.setStrokeColor(LINE)
    c.setLineWidth(.35)
    c.line(table_x, y2, table_x + table_w, y2)
    vals = [str(nr), title, focus, strategy, status, inputn, control]
    xx = table_x
    for j, (val, w) in enumerate(zip(vals, col_w)):
        if j > 0:
            c.setStrokeColor(HexColor("#E2E7EA"))
            c.line(xx, y2, xx, y)
        font = "Helvetica-Bold" if j in (0, 1) else "Helvetica"
        color = INK
        if j == 4 and ("Noch einen" in val or "Entdecker" in val):
            color = SAGE
            font = "Helvetica-Bold"
        if j == 4 and "unbenotet" in val:
            color = RUST
            font = "Helvetica-Bold"
        text_in_cell(c, val, xx, y2, w, row_h, font=font, size=7.2 if j != 1 else 7.4, color=color)
        xx += w
    y = y2

c.setStrokeColor(SLATE)
c.setLineWidth(.8)
c.rect(table_x, table_y, table_w, table_h, stroke=1, fill=0)

bottom_y = 7*mm
c.setFillColor(MUTED)
c.setFont("Helvetica", 6.8)
c.drawString(margin, bottom_y + 6.2*mm, "Verbindlichkeit: Blätter 1–13 und 16–24 = Pflicht · Blatt 14 = Noch einen Schritt (freiwillig) · Blatt 15 = Für Entdecker (freiwillig) · Projekte = freiwillig.")
c.drawString(margin, bottom_y + 2.5*mm, "Kontroll-Kiosk: zu Blatt 1–24 stehen Tipp und Lösung bzw. Lösungsbeispiel bereit. Hilfekette bleibt während der Lernzeiten als Grundroutine verfügbar.")

box_w = 33*mm
start_x = PAGE_W - margin - 3*box_w - 6*mm
for i in range(3):
    bx = start_x + i*(box_w + 3*mm)
    c.setStrokeColor(RUST)
    c.setLineWidth(.8)
    c.roundRect(bx, bottom_y + 1.5*mm, box_w, 9*mm, 1.8*mm, stroke=1, fill=0)
    c.setFillColor(RUST)
    c.setFont("Helvetica-Bold", 6.6)
    c.drawString(bx + 2*mm, bottom_y + 7.2*mm, f"LEK-Termin {i+1}")
    c.setFillColor(MUTED)
    c.setFont("Helvetica", 6.5)
    c.drawString(bx + 2*mm, bottom_y + 3.3*mm, "Datum: __________")

c.showPage()
c.save()
print(OUT)
