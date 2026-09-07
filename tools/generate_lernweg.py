"""Generate the paper learning path and formative checks; matches worksheets v3."""
from pathlib import Path
import json, shutil
from docx import Document
from docx.shared import Cm, Pt, RGBColor
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'materialien/arbeitsblaetter'
# Existing classroom design: A4 portrait, Arial 14, toner-saving bands.
def doc(title):
 d=Document();s=d.sections[0];s.page_width=Cm(21);s.page_height=Cm(29.7)
 s.top_margin=s.bottom_margin=Cm(1.3);s.left_margin=s.right_margin=Cm(1.5)
 for name,size in [('Normal',14),('Title',22),('Heading 1',17),('Heading 2',14)]:
  st=d.styles[name];st.font.name='Arial';st.font.size=Pt(size);st.font.color.rgb=RGBColor.from_string('24313A')
  st.paragraph_format.space_before=Pt(0);st.paragraph_format.space_after=Pt(6);st.paragraph_format.line_spacing=1.05
  st.paragraph_format.keep_with_next=name!='Normal'
 d.core_properties.title=title;d.core_properties.author='Deutschunterricht';d.core_properties.subject='Schritt 3 · Fassung 3 · 7. September 2026'
 p=s.footer.paragraphs[0];p.text='Wunschbriefe · Fassung 3 · '
 r=p.add_run();f=OxmlElement('w:fldSimple');f.set(qn('w:instr'),'PAGE');r._r.addnext(f)
 for r in p.runs:r.font.size=Pt(10)
 return d

def p(d,t,style=None):return d.add_paragraph(t,style)
def band(d,label,t):
 x=p(d,'');x.add_run(label+' ').bold=True;x.add_run(t)
 sh=OxmlElement('w:shd');sh.set(qn('w:fill'),'EEF2F4');x._p.get_or_add_pPr().append(sh)
 return x

def title(d,t,new=False):
 x=p(d,t,'Title');x.paragraph_format.page_break_before=new

data=json.loads((OUT/'arbeitsblaetter_inhalte.json').read_text())
d=doc('Mein Lernweg · Wunschbriefe')
title(d,'Mein Lernweg · Wunschbriefe')
p(d,'Name: _______________________________________')
band(d,'Dein Ziel:', 'Du schreibst einen freundlichen und verständlichen Brief mit einem Wunsch für die Schule.')
p(d,'Input → Übung → Vertiefung → Probearbeit → Projekte → Lernerfolgskontrolle (Arbeit)')
p(d,'Input heißt: Du bekommst eine Erklärung. Vertiefung und Projekte sind freiwillig. Die Probearbeit ist ohne Note.')
band(d,'So nutzt du den Lernweg:', 'Kreise dein nächstes Blatt ein. Hake ab, was du bearbeitet und geprüft hast. Ein Haken zeigt: erledigt. Er zeigt noch nicht: sicher gekonnt.')
p(d,'Planung: Wähle ein Blatt. Durchführung: Bearbeite es.\nReflexion: Prüfe dein Ergebnis. Wähle den nächsten Schritt.')
p(d,'Deine Übungen · Blätter 1–12','Heading 1')
for a in data[:12]:
 x=p(d,f"☐  Blatt {a['n']}   {a['title']}");x.paragraph_format.space_after=Pt(7)
band(d,'Halt nach Blatt 12:', 'Zeige an einem Beispiel: Anrede, Wunsch und Grußformel. Unsicher? Übe mit Blatt 7, 9 oder 12 und frage nach Hilfe.')
p(d,'Aufgabe: Das tust du. Hilfe: Das unterstützt dich.\nBeispiel: So kann es aussehen. Prüfe: Daran erkennst du dein Ergebnis.')
title(d,'Mein Lernweg · weiter geht’s',True)
p(d,'Deine Übungen · Blätter 13–24','Heading 1')
for a in data[12:]:
 extra={14:' · freiwillig',15:' · freiwillig',17:' · Hilfe bei Bedarf',21:' · ohne Note',24:' · nach der Arbeit'}.get(a['n'],'')
 x=p(d,f"☐  Blatt {a['n']}   {a['title']}{extra}");x.paragraph_format.space_after=Pt(8)
band(d,'Halt nach Blatt 19:', 'Prüfe deinen eigenen Brief mit dem Kompetenzcheck. Besprich eine passende nächste Übung mit der Lehrkraft.')
p(d,'Blatt 14 und 15 sowie alle Zusätze sind freiwillig. Brauchst du Blatt 17 nicht, gehe zu Blatt 18. Projekte wählst du freiwillig nach der Probearbeit.')
p(d,'Vor deiner Arbeit','Heading 1')
p(d,'☐  Du hast die Probearbeit geschrieben und besprochen.\n☐  Du hast deinen Brief mit dem Kompetenzcheck geprüft.\n☐  Du weißt, was du schon kannst und noch üben möchtest.')
p(d,'Dein nächster Schritt: __________________________________\n_____________________________________________________')
p(d,'Dein Termin für die Arbeit: ______________________________\nBesprochen mit: _______________________________________')
band(d,'Hilfen sind erlaubt:', 'Nutze in der Übung die ausgedruckten Hilfen oder frage nach. Hilfe zu nutzen ist kein Zeichen für wenig Können.')
d.save(OUT/'Mein_Lernweg.docx');shutil.copy2(OUT/'Mein_Lernweg.docx',OUT/'Mein_Lernweg_Wunschbriefe_A4_NEU.docx')

d=doc('Kompetenzcheck · Mein Wunschbrief')
title(d,'Kompetenzcheck · Mein Wunschbrief')
p(d,'Name: ________________________  Datum: ______________\nDein Text: ☐ Übungsbrief   ☐ Probearbeit   ☐ Überarbeitung')
band(d,'Aufgabe 1:', 'Lege deinen Brief daneben. Lies jeden Prüfpunkt. Schreibe bei Punkt 1–4 die Zahl an die passende Stelle. Lies für Punkt 5 und 6 den ganzen Brief. Kreuze an.')
p(d,'Fehlt etwas oder bist du unsicher? Kreuze „Noch üben“ an.\nDu darfst Hilfen nutzen. Der Check bekommt keine Note.')
checks=[('1 · Anrede','Deine Anrede passt zur Person, die den Brief bekommt.'),('2 · Wunsch','Dein Wunsch ist klar. Er passt zur Aufgabe und zur Schule.'),('3 · Weiterer Satz','Mindestens ein weiterer Satz passt zu deinem Wunsch.'),('4 · Schluss','Eine passende Grußformel und dein Name stehen am Ende.'),('5 · Freundlicher Ton','Dein Brief bittet freundlich. Er droht nicht und beleidigt nicht.'),('6 · Verständlich und lesbar','Dein Brief besteht aus verständlichen ganzen Sätzen.\nMan kann deine Schrift lesen.')]
for h,t in checks:
 p(d,h,'Heading 2');p(d,t);x=p(d,'☐ Das zeigt dein Brief.     ☐ Noch üben.');x.paragraph_format.space_after=Pt(11)
band(d,'Prüfe auch:', 'Stehen Ort und Datum oben?\n☐ Ja.   ☐ Du ergänzt sie noch.')
p(d,'Ein weiterer Satz kann eine Bitte oder eine Hoffnung sein.\nEin Grund und Zahlen sind freiwillig. Ein kurzer Brief kann gelingen.')
title(d,'Dein nächster Lernschritt',True)
band(d,'Aufgabe 2:', 'Wähle einen Punkt, den du noch üben möchtest. Nutze die passende Übung. Besprich deine Wahl mit der Lehrkraft.')
for h,t in [('Anrede oder Schluss','Nutze Blatt 9. Für die Reihenfolge hilft Blatt 7 oder 8.'),('Wunsch','Nutze Blatt 6 oder 13. Sage zuerst mündlich, was du möchtest.'),('Weiterer Satz','Nutze Blatt 16 oder 17. Sage zum Beispiel, was du dir erhoffst.'),('Freundlicher Ton','Nutze Blatt 11 oder 20. Formuliere eine freundliche Bitte.'),('Verständlich und lesbar','Lies deinen Brief leise Satz für Satz. Verbessere unklare Stellen. Prüfe Satzanfänge, Satzschlusszeichen und Wortabstände.')]:
 p(d,h,'Heading 2');p(d,t)
p(d,'Planung','Heading 1')
p(d,'Du übst: ______________________________________________\nDeine Hilfe oder dein Blatt: ______________________________')
p(d,'Durchführung','Heading 1')
p(d,'Bearbeite die gewählte Übung. Prüfe danach die passende Stelle in deinem Brief. Ändere sie nur, wenn es nötig ist.')
p(d,'Reflexion','Heading 1')
p(d,'Zeige der Lehrkraft, was jetzt gelingt.\n☐ Der Punkt gelingt jetzt.   ☐ Du möchtest weiter üben.\nDeine genutzte Hilfe: ___________________________________')
band(d,'Alles sicher? Freiwillig:', 'Ergänze einen passenden Grund (Blatt 14), bearbeite ein Bedenken (Blatt 15) oder nutze passende Daten (Zusatz auf Blatt 3, 12 oder 20).')
p(d,'Rückmeldung der Lehrkraft: ______________________________\n_____________________________________________________')
d.save(OUT/'Kompetenzcheck_Wunschbrief.docx')
print('Generated two-page learning path (two identical filenames) and two-page competence check.')
