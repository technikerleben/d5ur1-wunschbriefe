"""Comparable paper assessments and mock exam using one shared task template."""
from pathlib import Path
from copy import deepcopy
from docx import Document
from docx.shared import Pt,Cm,RGBColor
from docx.enum.style import WD_STYLE_TYPE
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
ROOT=Path(__file__).resolve().parents[1];EX=ROOT/'materialien/lernerfolgskontrolle';MOCK=ROOT/'materialien/probearbeit'
BASE=EX/'Wunschbrief_Das_zaehlt_Kinderfassung.docx'
helpdoc=Document(BASE);HELP=[deepcopy(x) for x in helpdoc.element.body if x.tag!=qn('w:sectPr')]
for e in HELP:
 for t in e.iter(qn('w:t')):
  if t.text:t.text=t.text.replace('auf Seite 1','unter „Das gehört in deinen Brief“')
# The wording of the existing aid is unchanged except its now-unambiguous cross-reference.
def new(title):
 d=Document(BASE);d.element.body.clear_content()
 for section in d.sections:
  for paragraph in section.footer.paragraphs:
   for run in paragraph.runs:
    run.text=run.text.replace('8. September 2026','5. Oktober 2026').replace('7. September 2026','5. Oktober 2026').replace('Fassung 2','Fassung 4').replace('Fassung 3','Fassung 4')
 d.core_properties.title=title+' · Fassung 4'
 d.core_properties.subject='Lernerfolgskontrolle · 5. Oktober 2026'
 d.core_properties.author='Deutschunterricht'
 for name,size,bold in [('ExamBody',12,False),('ExamTitle',20,True),('ExamHeading',14,True),('ExamLabel',12,True)]:
  st=d.styles[name] if name in d.styles else d.styles.add_style(name,WD_STYLE_TYPE.PARAGRAPH)
  st.font.name='Arial';st.font.size=Pt(size);st.font.bold=bold;st.font.color.rgb=RGBColor.from_string('24313A')
  st.paragraph_format.space_before=Pt(0);st.paragraph_format.space_after=Pt(6)
  st.paragraph_format.line_spacing=1.03;st.paragraph_format.keep_with_next=name!='ExamBody'
 return d

def p(d,t='',style='ExamBody'):return d.add_paragraph(t,style)
def page(d,title,first=False):
 x=p(d,title,'ExamTitle');x.paragraph_format.page_break_before=not first

def lines(d,n=1,height=26):
 for _ in range(n):
  x=p(d);x.paragraph_format.space_after=Pt(0);x.paragraph_format.line_spacing=Pt(height)
  x.add_run(' ').font.size=Pt(1)
  borders=OxmlElement('w:pBdr');b=OxmlElement('w:bottom');b.set(qn('w:val'),'single');b.set(qn('w:sz'),'3');b.set(qn('w:color'),'B2B8BC');borders.append(b);between=deepcopy(b);between.tag=qn('w:between');borders.append(between);x._p.get_or_add_pPr().append(borders)
def field(d,label):p(d,label,'ExamLabel');lines(d,1,22)
def table(d,rows):
 widths=[12.8,5.0];tw=[round(x*1440/2.54) for x in widths]
 t=d.add_table(rows=0,cols=2);t.autofit=False;pr=t._tbl.tblPr
 w=pr.find(qn('w:tblW'));w.set(qn('w:w'),str(sum(tw)));w.set(qn('w:type'),'dxa')
 ind=OxmlElement('w:tblInd');ind.set(qn('w:w'),'100');ind.set(qn('w:type'),'dxa');pr.append(ind)
 mar=OxmlElement('w:tblCellMar')
 for name in ['top','bottom','left','right']:
  e=OxmlElement('w:'+name);e.set(qn('w:w'),'80' if name in ['top','bottom'] else '100');e.set(qn('w:type'),'dxa');mar.append(e)
 pr.append(mar)
 for i,v in enumerate(tw):t._tbl.tblGrid.gridCol_lst[i].set(qn('w:w'),str(v))
 for i,row in enumerate(rows):
  r=t.add_row();r._tr.get_or_add_trPr().append(OxmlElement('w:cantSplit'))
  for j,txt in enumerate(row):
   c=r.cells[j];c.width=Cm(widths[j]);x=c.paragraphs[0];x.style=d.styles['ExamBody'];x.paragraph_format.space_after=Pt(2);run=x.add_run(txt);run.bold=i==0
  if i==0:r._tr.get_or_add_trPr().append(OxmlElement('w:tblHeader'))
 return t

# Fassung 4 (October 2026): the three dates use a common task and rubric.
# Previously completed mock assessment stays untouched.
variants=[
 ('Termin 1','eine Ausleihe von Spielgeräten für Schulhof B in den Pausen',
  ['Ausleihe von Spielgeräten','Mehr Sitzbänke','Klettergerüst mit Rutsche','Größere Fußballtore']),
 ('Termin 2','eine Ausleihe von Spielgeräten für Schulhof B in den Pausen',
  ['Ausleihe von Spielgeräten','Mehr Sitzbänke','Klettergerüst mit Rutsche','Größere Fußballtore']),
 ('Termin 3','eine Ausleihe von Spielgeräten für Schulhof B in den Pausen',
  ['Ausleihe von Spielgeräten','Mehr Sitzbänke','Klettergerüst mit Rutsche','Größere Fußballtore'])]
def append_help(d,first=False):
 page(d,'Dein Wunschbrief: Das zählt',first)
 p(d,'Dein Ziel: Du schreibst einen freundlichen und verständlichen Wunschbrief mit einem passenden Grund.')
 p(d,'Das gehört in deinen Brief','ExamHeading')
 for x in [
   'Du schreibst Ort und Datum.',
   'Du verwendest eine passende Anrede.',
   'Du wünschst dir eine Ausleihe von Spielgeräten für Schulhof B in den Pausen.',
   'Du nennst mindestens einen passenden Grund für den Wunsch.',
   'Du schreibst freundlich und in verständlichen Sätzen.',
   'Deine Schrift ist lesbar. Die Teile des Briefes sind übersichtlich.',
   'Du beendest den Brief mit einer Grußformel und deinem Namen.'
 ]:p(d,'☐ '+x)
 p(d,'Das kannst du zusätzlich zeigen · freiwillig','ExamHeading')
 p(d,'☐ Du nutzt ein passendes Ergebnis aus der Umfrage und erklärst es sinnvoll.')
 p(d,'Ein Grund ist Pflicht. Nur die Umfrage ist freiwillig.')
 p(d,'So wird dein Brief bewertet','ExamHeading')
 p(d,'Du kannst 18 Grundpunkte bekommen. Bewertet werden der Wunsch, der Briefaufbau, die freundliche Sprache, die Begründung, die sprachliche Richtigkeit und die Lesbarkeit. Für die passende Umfrage kannst du bis zu 2 Zusatzpunkte bekommen.')
 p(d,'Ein guter Brief muss nicht lang sein. Wichtig ist, dass du deinen Wunsch verständlich formulierst und begründest.')
 page(d,'Diese Hilfe darfst du nutzen')
 p(d,'Diese beiden Seiten darfst du bei der Lernerfolgskontrolle nutzen. Dafür gibt es keinen Punktabzug.')
 p(d,'Planung','ExamHeading')
 p(d,'Überlege: An wen schreibe ich? Was wünsche ich mir? Warum wäre das sinnvoll? Notiere Stichwörter in deinen Schreibplan.')
 p(d,'Durchführung','ExamHeading')
 p(d,'Schreibe deinen Brief in dieser Reihenfolge:')
 for x in ['1  Ort und Datum','2  freie Zeile','3  Anrede mit Komma','4  freie Zeile','5  Wunsch und mindestens ein passender Grund','6  freie Zeile','7  Grußformel und Name']:p(d,x)
 p(d,'Wenn du einen Anfang brauchst','ExamHeading')
 for x in ['Sehr geehrte Frau …,','ich wünsche mir …','Das wäre sinnvoll, weil …','Dann könnten wir …','Freundliche Grüße']:p(d,x)
 p(d,'Nur freiwillig für die Umfrage','ExamHeading')
 p(d,'In der Umfrage wünschen sich … Kinder …')
 p(d,'Reflexion','ExamHeading')
 p(d,'Prüfe, ob du deinen Wunsch klar nennst und mindestens einen passenden Grund dafür angibst. Kontrolliere das Komma nach der Anrede, den kleingeschriebenen Satzbeginn und die freien Zeilen.')
 p(d,'Du darfst dir den Auftrag vorlesen lassen. Deinen Brief formulierst du selbst. Keine Partnerhilfe und kein Kontroll-Kiosk während der Arbeit.')
def packet(d,spec,first=False):
 label,wish,items=spec
 page(d,label+' · Dein Wunschbrief',first)
 p(d,'Name: __________________________  Datum: ______________')
 p(d,'Arbeitszeit: max. 45 Minuten')
 p(d,'Deine Situation','ExamHeading')
 p(d,'Schulleiterin Frau Schneider sammelt Wünsche für Schulhof B. Du möchtest eine Ausleihe von Spielgeräten für die Pausen. Schreibe Frau Schneider einen Brief und erkläre, warum dir dieser Wunsch wichtig ist.')
 p(d,'Dein Auftrag','ExamHeading')
 for x in [
  'Schreibe Ort und Datum oben auf den Brief.',
  'Wähle eine passende Anrede für Schulleiterin Frau Schneider.',
  'Formuliere den Wunsch nach einer Ausleihe von Spielgeräten für Schulhof B klar und freundlich.',
  'Nenne mindestens einen passenden Grund für den Wunsch.',
  'Beende den Brief mit einer Grußformel und deinem Namen.',
  'Schreibe verständliche ganze Sätze und lesbar.'
 ]:p(d,'☐ '+x)
 p(d,'Freiwillig: Nutze die Umfrage','ExamHeading')
 p(d,'Wenn du möchtest, ergänze ein passendes Umfrageergebnis. Dies ist der einzige freiwillige Zusatz.')
 p(d,'26 Kinder einer Beispielklasse wurden gefragt: „Was wünschst du dir für den Pausenhof?“ Mehrere Antworten waren erlaubt. Die Zahlen sind erfunden.')
 table(d,[['Wunsch für den Pausenhof','Stimmen']]+[[x,str(v)] for x,v in zip(items,[17,14,11,8])])
 p(d,'Arbeite mit Planung → Durchführung → Reflexion.')
 page(d,label+' · Planung')
 p(d,'Notiere Stichwörter. Deinen Brief schreibst du erst auf den Schreibbogen. Die beiden Hilfeseiten darfst du nutzen.')
 for x in [
  'An wen schreibst du?',
  'Was wünschst du dir für Schulhof B?',
  'Warum ist die Ausleihe von Spielgeräten sinnvoll? Nenne einen Grund.',
  'Welche Anrede wählst du?',
  'Welche Grußformel wählst du?'
 ]:field(d,x)
 p(d,'Nur wenn du die Umfrage nutzen möchtest','ExamHeading')
 field(d,'Welches passende Umfrageergebnis möchtest du nutzen? · freiwillig')
 p(d,'Dieses Feld darf leer bleiben. Ein passender Grund gehört aber in den Brief.')
 page(d,label+' · Durchführung')
 p(d,'Name: __________________________  Datum: ______________')
 p(d,'Arbeitszeit: max. 45 Minuten')
 p(d,'Schreibe hier deinen vollständigen Brief. Bei Bedarf bekommst du weiteres Schreibpapier.')
 lines(d,20,24)
 p(d,'Reflexion','ExamHeading')
 p(d,'Lies deinen Brief. Prüfe ihn mit „Dein Wunschbrief: Das zählt“. Verbessere nur, was nötig ist.')
 append_help(d)
def feedback(d):
 page(d,'Rückmeldung zur Probearbeit')
 p(d,'Name: __________________________  Datum: ______________')
 p(d,'Die Lehrkraft füllt diesen Bogen mit dir aus. Er ist keine Note.')
 p(d,'Betrachteter Text: ☐ erste Fassung  ☐ unterstützte Überarbeitung')
 p(d,'Das zeigt dein Brief','ExamHeading')
 for t in ['Die Anrede passt zur Person.','Dein Wunsch passt zum Auftrag und ist verständlich.','Ein weiterer Satz passt zu deinem Wunsch.','Grußformel und dein Name stehen am Ende.','Dein Brief ist freundlich.','Du schreibst verständliche Sätze und lesbar.']:
  p(d,t);p(d,'☐ gelungen   ☐ noch üben')
 p(d,'Ort und Datum: ☐ vorhanden   ☐ noch ergänzen')
 p(d,'Freiwillige Zusätze','ExamHeading')
 p(d,'Grund: ☐ passend  ☐ noch prüfen  ☐ nicht genutzt\nDaten: ☐ passend  ☐ noch prüfen  ☐ nicht genutzt')
 field(d,'Diese zusätzliche Hilfe gab es (oder: keine):')
 field(d,'Das gelingt dir schon:')
 field(d,'Dein nächster Schritt / passendes Blatt:')
 p(d,'Terminwahl: ☐ besprechen   ☐ nach gezielter Übung besprechen')

# Save only current LEK variants. The historical Probearbeit remains unchanged.
for i,spec in enumerate(variants,1):
 d=new('Lernerfolgskontrolle Wunschbrief · Termin '+str(i))
 packet(d,spec,True)
 d.save(EX/f'Lernerfolgskontrolle_Wunschbrief_Termin_{i}.docx')
d=new('Lernerfolgskontrolle Wunschbrief · 3 Termine')
for i,spec in enumerate(variants):packet(d,spec,i==0)
d.save(EX/'Lernerfolgskontrolle_Wunschbrief_3_Termine.docx')
d=new('Wunschbrief Das zählt · Kinderfassung · LEK Fassung 4')
append_help(d,True)
d.save(EX/'Wunschbrief_Das_zaehlt_Kinderfassung.docx')
# Teacher rubric: 18 core points plus up to 2 voluntary survey points.
d=new('Bewertungsraster · LEK Fassung 4')
d.styles['ExamBody'].font.size=Pt(10)
d.styles['ExamTitle'].font.size=Pt(16)
d.styles['ExamHeading'].font.size=Pt(11)
d.sections[0].top_margin=Cm(1.15)
d.sections[0].bottom_margin=Cm(1.1)
page(d,'Bewertungsraster Wunschbrief',True)
p(d,'Deutsch 5 · Lernerfolgskontrolle · Fassung 4')
p(d,'Name: ______________________    Termin: __________')
p(d,'Pflicht: Spielgeräteausleihe für Schulhof B mit mindestens einem passenden Grund.')
p(d,'Kernmerkmale · alle müssen erkennbar sein','ExamHeading')
for x in [
 'K1: Passende Anrede.','K2: Vorgegebener Wunsch ist verständlich.',
 'K3: Mindestens ein inhaltlich passender Grund.',
 'K4: Grußformel und Name.','K5: Freundliche, sachliche Sprache.',
 'K6: Verständliche Sätze und lesbarer Brief.'
]:p(d,'☐ '+x)
p(d,'Grundpunkte · 0–3 je Bereich','ExamHeading')
for x in [
 'Schreibsituation und Wunsch:   ______ / 3',
 'Briefaufbau (Ort, Datum, Leerzeilen, Anrede, Gruß):   ______ / 3',
 'Freundliche, angemessene Sprache:   ______ / 3',
 'Begründung (nachvollziehbarer, passender Grund):   ______ / 3',
 'Sätze, Rechtschreibung, Zeichensetzung:   ______ / 3',
 'Lesbarkeit und Gliederung:   ______ / 3'
]:p(d,x)
p(d,'Grundpunkte insgesamt: ______ / 18')
p(d,'Freiwilliger Zusatz · Umfrage','ExamHeading')
p(d,'0 = nicht genutzt oder unpassend; 1 = passend genannt; 2 = korrekt und sinnvoll für den Wunsch eingesetzt.')
p(d,'Zusatzpunkte: ______ / 2    Gesamt: ______ / 20')
p(d,'Kompetenzniveaus','ExamHeading')
for x in [
 'Noch nicht erreicht: Kernmerkmal fehlt oder 0–8 Grundpunkte.',
 'Mindeststandard: alle Kernmerkmale und 9–12 Grundpunkte.',
 'Regelstandard: alle Kernmerkmale und 13–18 Grundpunkte, sofern Leistungsstandard nicht erreicht.',
 'Leistungsstandard / Vertiefung: alle Kernmerkmale, 17–18 Grundpunkte und 2 Zusatzpunkte.'
]:p(d,x)
p(d,'Fehlen Ort und Datum allein, erhält der Brief im Aufbau höchstens 2 Punkte. Eine fehlende Begründung ist ein fehlendes Kernmerkmal. Umfragedaten ersetzen keinen Grund.')
d.save(EX/'Bewertungsraster_Wunschbrief_Lernerfolgskontrolle.docx')
print('Generated LEK Fassung 4: 3 terms, collection, child help and rubric.')
