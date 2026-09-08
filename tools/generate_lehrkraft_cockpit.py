"""A3 overview from the same task data as the current pupil worksheets."""
from pathlib import Path
import json
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A3,landscape
from reportlab.lib.colors import HexColor
from reportlab.lib.units import mm
from reportlab.pdfbase.pdfmetrics import stringWidth, registerFont
from reportlab.pdfbase.ttfonts import TTFont
registerFont(TTFont("Body", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"))
registerFont(TTFont("Body-Bold", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"))
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'materialien/lehrkraft/Lehrkraft_Cockpit_Wunschbriefe_A3.pdf'
data=json.loads((ROOT/'materialien/arbeitsblaetter/arbeitsblaetter_inhalte.json').read_text())
strategies=['Auftrag klären','Lernziel setzen','Auftrag klären','Beispiel nutzen','Beispiel nutzen','Auftrag klären','Beispiel nutzen','Beispiel nutzen','Beispiel nutzen','Mit Kriterien prüfen','Mit Kriterien prüfen','Beispiel nutzen','Lernziel setzen','Beispiel nutzen','Beispiel nutzen','Arbeit in Schritte teilen','Arbeit in Schritte teilen','Zwischenstopp machen','Mit Kriterien prüfen','Mit Kriterien prüfen','Auftrag klären','Lernprozess reflektieren','Lernziel setzen','Lernprozess reflektieren']
helps=['Kiosk / Merkblatt 1','Papierlernweg / Lehrkraft','Kiosk / Merkblatt 1','Kiosk / Merkblatt 1','Kiosk / Merkblatt 1','Kiosk / Merkblatt 1','Kiosk / Merkblatt 2','Kiosk / Merkblatt 2','Kiosk / Merkblatt 2','Kiosk / Merkblatt 2','Kiosk / Merkblatt 3','Kiosk / Merkblatt 3','Kiosk / Merkblatt 1','Kiosk / Merkblatt 4','Kiosk / Vertiefungskarten','Plan / Merkblatt 5','Gerüst / Merkblatt 5','Kiosk / Merkblatt 5','Checkliste / Merkblatt 6','Kiosk / Merkblatt 6','Probearbeitspaket / Lehrkraft','Probearbeit / Kompetenzcheck','Blatt 23 / Lehrkraft','Reflexion nach der Arbeit']
W,H=landscape(A3);M=10*mm;c=canvas.Canvas(str(OUT),pagesize=(W,H));c.setTitle('Lehrkraft-Cockpit Wunschbriefe - Fassung 3');c.setAuthor('Deutsch 5')
INK=HexColor('#24313A');SLATE=HexColor('#3E5668');LINE=HexColor('#CBD4D9')
def text(t,x,y,size=12,bold=False):
 c.setFillColor(INK);c.setFont('Body-Bold' if bold else 'Body',size);c.drawString(x,y,t)
def wrap(t,width,font='Body',size=12):
 result=[];line=''
 for word in t.split():
  nxt=(line+' '+word).strip()
  if stringWidth(nxt,font,size)>width and line:result.append(line);line=word
  else:line=nxt
 if line:result.append(line)
 return result
text('LEHRKRAFT-COCKPIT · WUNSCHBRIEFE',M,H-35,23,True)
text('8. September 2026 · Fassung 3 · Kinder arbeiten mit Papier; Kiosk nur am Klassenraum-Laptop.',M,H-54)
text('Planung → Durchführung → Reflexion',M,H-72,12,True)
text('Input → Übung → Vertiefung → Probearbeit → Projekte → Lernerfolgskontrolle (Arbeit)',M,H-90)
# Exactly the usable width: the previous widths overran the page.
widths=[42,377,176,131,61,W-2*M-787]
assert abs(sum(widths)-(W-2*M))<.01
headers=['Blatt','Lernaufgabe','SRL-Strategie','Verbindlichkeit','Input','Kontrolle / Hilfe']
top=H-105;header_h=24;rh=25
c.setFillColor(HexColor('#EEF2F4'));c.rect(M,top-header_h,W-2*M,header_h,fill=1,stroke=0)
x=M
for head,width in zip(headers,widths):text(head,x+4,top-16,12,True);x+=width
for row,a in enumerate(data):
 n=a['n'];y=top-header_h-row*rh
 if n in [14,15,17]:c.setFillColor(HexColor('#F0F6EE'));c.rect(M,y-rh,W-2*M,rh,fill=1,stroke=0)
 status='freiwillig' if n in [14,15] else 'bei Bedarf' if n==17 else 'Pflicht, ohne Note' if n==21 else 'nach der Arbeit' if n==24 else 'Übung / Absprache'
 inp='1' if n<=6 else '2' if n<=10 else '3' if n<=15 else '4' if n<=20 else '5' if n<=23 else 'danach'
 vals=[str(n),a['title'],strategies[row],status,inp,helps[row]];x=M
 for j,(v,w) in enumerate(zip(vals,widths)):
  lines=wrap(v,w-8,'Body-Bold' if j in [0,1] else 'Body',12)
  assert len(lines)<=2,(n,j,v)
  for k,line in enumerate(lines):text(line,x+4,y-10-k*12,12,j in [0,1])
  x+=w
 c.setStrokeColor(LINE);c.setLineWidth(.4);c.line(M,y-rh,W-M,y-rh)
base=top-header_h-24*rh
assert base>85
text('Pflichtkern: Anrede · klarer Wunsch · weiterer passender Satz · Gruß + Name · freundlich · lesbar und verständlich.',M,base-18,12)
text('Ort/Datum gehören dazu. Gründe und Daten bleiben freiwillig. Blatt 17 ist eine Hilfe bei Bedarf; alle Projekte sind freiwillig.',M,base-34,12)
text('Die Lehrkraft vereinbart passende Übungen. Bei der Arbeit: nur das Prüfungspaket und vereinbarte individuelle Hilfen.',M,base-50,12)
text('Strategien schrittweise einführen; Ablauf, Rollen und Druckbedarf: Hinweise_Unterricht_Fassung3.md',M,base-66,12)
c.showPage();c.save();print(OUT)
