from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor
from reportlab.pdfbase.pdfmetrics import stringWidth
import os

OUT='materialien/offener-anfang/Offener_Anfang_Wunschbriefe_Druckpaket.pdf'
B=HexColor('#245688'); R=HexColor('#8E1F24'); K=HexColor('#262626'); M=HexColor('#666666'); L=HexColor('#C9CDD1'); W=HexColor('#FFFFFF')
PW,PH=A4

def wrap(t,f='Helvetica',s=10,w=100*mm):
    out=[]; cur=''
    for z in t.split():
        q=z if not cur else cur+' '+z
        if stringWidth(q,f,s)<=w: cur=q
        else:
            if cur: out.append(cur)
            cur=z
    if cur: out.append(cur)
    return out

def txt(c,t,x,y,w,s=9.5,f='Helvetica',lead=None,col=K,n=None):
    lead=lead or s*1.25; ls=wrap(t,f,s,w); ls=ls[:n] if n else ls
    c.setFont(f,s); c.setFillColor(col)
    for q in ls: c.drawString(x,y,q); y-=lead
    return y

def head(c,t,st,p):
    c.setStrokeColor(R); c.setLineWidth(3); c.line(14*mm,PH-15*mm,38*mm,PH-15*mm)
    c.setStrokeColor(B); c.line(40*mm,PH-15*mm,56*mm,PH-15*mm)
    c.setFillColor(K); c.setFont('Helvetica-Bold',18); c.drawString(14*mm,PH-27*mm,t)
    c.setFillColor(M); c.setFont('Helvetica',9); c.drawString(14*mm,PH-33*mm,st)
    c.setFont('Helvetica',7); c.drawRightString(PW-12*mm,8*mm,str(p)); c.setStrokeColor(L); c.setLineWidth(.4); c.line(14*mm,12*mm,PW-14*mm,12*mm)

def border(c,x,y,w,h,col=B):
    c.setStrokeColor(col); c.setLineWidth(1); c.setFillColor(W); c.roundRect(x,y,w,h,3*mm,stroke=1,fill=1)
    c.setStrokeColor(R); c.setLineWidth(2); c.line(x+5*mm,y+h-7*mm,x+22*mm,y+h-7*mm); c.setStrokeColor(B); c.line(x+24*mm,y+h-7*mm,x+36*mm,y+h-7*mm)

def cut(c,x1,y1,x2,y2):
    c.saveState(); c.setStrokeColor(HexColor('#AAAAAA')); c.setLineWidth(.5); c.setDash(2,2); c.line(x1,y1,x2,y2); c.restoreState()

def steps(c,arr,x,y,w,col=B,s=8.5):
    for i,t in enumerate(arr,1):
        c.setStrokeColor(col); c.circle(x+3*mm,y+1*mm,2.5*mm,stroke=1,fill=0); c.setFillColor(col); c.setFont('Helvetica-Bold',8); c.drawCentredString(x+3*mm,y-1.5*mm,str(i))
        ls=wrap(t,'Helvetica',s,w-9*mm); c.setFillColor(K); c.setFont('Helvetica',s); yy=y+3.5*mm
        for q in ls: c.drawString(x+8*mm,yy,q); yy-=10
        y-=max(10*mm,len(ls)*4*mm+3*mm)
    return y

offers=[
('Ankommen & waehlen','allein','5 Min.','Wahlkarte + andere Angebote',['Schau auf die Wahlkarte: Wie moechtest du heute starten?','Waehle ein Angebot, das zu deiner Energie und deinem Ziel passt.','Starte direkt. Pruefe nach ein paar Minuten: War deine Wahl passend?'],'Es gibt keine richtige Wahl. Wichtig ist, dass sie heute zu dir passt.'),
('Briefteile-Domino','allein / zu zweit','5-10 Min.','Domino-Set A oder B + Kontrollkarte',['Mische die Dominosteine und lege START vor dich.','Lege immer Begriff und passende Erklaerung oder Beispiel aneinander.','Bei ZIEL vergleichst du mit der Kontrollkarte.'],'Set A wiederholt Grundlagen. Set B ist fuer spaeter in der Reihe.'),
('Freundlich oder nicht?','allein / zu zweit','5-10 Min.','Sortierkarten + Felder + Kontrollkarte',['Lies jede Formulierung.','Ordne zu: PASST GUT oder MUSS BESSER WERDEN.','Kontrolliere und verbessere danach eine Formulierung.'],'Die Kontrollkarte zeigt eine moegliche Zuordnung und Verbesserungen.'),
('Wunsch-Detektiv','allein / zu zweit','5-10 Min.','Detektivkarten + Kontrollkarte',['Zieh eine Karte und lies den Mini-Brief.','Finde Empfaenger, Wunsch und eine besonders freundliche Stelle.','Vergleiche mit der Kontrollkarte.'],'Karten 7 und 8 enthalten zusaetzliche Informationen.'),
('Satzbau-Werkstatt','allein / zu zweit','5-10 Min.','Karten A-D + Beispielkarte',['Waehle eine Anrede, einen Wunsch und einen Gruss.','Wenn du moechtest, ergaenze einen passenden Grund.','Lege einen kurzen Mini-Brief und lies ihn laut.'],'Viele Loesungen sind moeglich. Pruefe: vollstaendig, freundlich, verstaendlich?'),
('Brief-Blitz','2-4 Personen','5-10 Min.','Stapel EMPFAENGER + Stapel WUNSCH',['Zieh je eine Karte von beiden Stapeln.','Formuliere in einem Satz einen freundlichen Wunsch.','Passt der Empfaenger nicht? Begruende kurz und nenne einen besseren.'],'Die Gruppe prueft: klar, freundlich und passend adressiert?')]

det=[
('1','Liebe Frau Koenig,\nich wuensche mir eine Leseecke in unserem Klassenraum. Es waere schoen, wenn wir dort in freien Zeiten lesen koennten.\nViele Gruesse\nMia','Frau Koenig','eine Leseecke im Klassenraum','Es waere schoen, wenn ...'),
('2','Lieber Herr Weber,\nkoennten Sie bitte pruefen, ob wir in der Pause mehr Baelle ausleihen koennen? Das wuerde vielen Kindern helfen.\nViele Gruesse\nNoah','Herr Weber','mehr Baelle zum Ausleihen','Koennten Sie bitte pruefen, ob ...'),
('3','Liebe Schulleitung,\nich wuensche mir zusaetzliche Sitzplaetze auf dem Schulhof. Dann koennten mehr Kinder in der Pause zusammensitzen.\nViele Gruesse\nElif','die Schulleitung','zusaetzliche Sitzplaetze','Ich wuensche mir ...'),
('4','Liebe Frau Schmitt,\nich moechte gern eine Technik-AG vorschlagen. Vielleicht waere es moeglich, eine solche AG am Nachmittag anzubieten.\nViele Gruesse\nBen','Frau Schmitt','eine Technik-AG','Vielleicht waere es moeglich ...'),
('5','Lieber Herr Becker,\nes waere schoen, wenn wir mehr Pflanzen im Klassenraum haetten. Sie wuerden den Raum freundlicher machen.\nViele Gruesse\nLina','Herr Becker','mehr Pflanzen','Es waere schoen, wenn ...'),
('6','Liebes Mensateam,\nich wuensche mir einen ruhigen Platz, an dem man in der Pause kurz sitzen kann. Koennten Sie unsere Idee bitte weitergeben?\nViele Gruesse\nSamir','das Mensateam','einen ruhigen Platz','Koennten Sie ... bitte ...'),
('7 +','Liebe Schulleitung,\nin unserer Umfrage haben sich 18 von 26 Kindern eine Spieleausleihe gewuenscht. Ich moechte deshalb vorschlagen, einige Spiele fuer die Pause anzuschaffen.\nViele Gruesse\nAylin','die Schulleitung','eine Spieleausleihe','Ich moechte deshalb vorschlagen ...'),
('8 *','Liebe Frau Koenig,\nich wuensche mir gemuetliche Sitzmoeglichkeiten. Vielleicht ist dafuer nicht viel Platz. Man koennte zuerst nur zwei Sitzkissen ausprobieren.\nViele Gruesse\nJonas','Frau Koenig','gemuetliche Sitzmoeglichkeiten','Man koennte zuerst ... ausprobieren.')]

good=['Ich wuensche mir eine Leseecke.','Koennten Sie bitte pruefen, ob wir mehr Baelle bekommen koennen?','Es waere schoen, wenn es zusaetzliche Sitzplaetze gaebe.','Ich moechte gern eine Technik-AG vorschlagen.','Vielleicht waere es moeglich, einen ruhigen Pausenraum einzurichten.','Vielen Dank, dass Sie meinen Wunsch lesen.','Ich faende es gut, wenn wir mehr Pflanzen im Klassenraum haetten.','Waere es moeglich, eine Spieleausleihe auszuprobieren?','Man koennte zuerst mit wenigen neuen Spielen starten.']
bad=['Ich will sofort neue Baelle.','Sie muessen uns einen Pausenraum geben.','Machen Sie das!','Kaufen Sie einfach neue Sitzmoebel.','Alle wollen eine Technik-AG!','Das ist sowieso die beste Idee.','Wir brauchen das. Punkt.','Geben Sie uns mehr Spiele!','Das muss jetzt geaendert werden.']

cats={
'A - ANREDE':['Liebe Frau Koenig,','Lieber Herr Weber,','Liebe Schulleitung,','Lieber Herr Becker,','Liebe Frau Schmitt,','Liebes Ganztagsteam,','Liebe Klassenleitung,','Liebes Mensateam,'],
'B - WUNSCH':['ich wuensche mir eine Leseecke.','ich wuensche mir mehr Baelle fuer die Pause.','ich moechte zusaetzliche Sitzplaetze vorschlagen.','es waere schoen, wenn wir mehr Pflanzen haetten.','koennten Sie bitte eine Technik-AG pruefen?','ich wuensche mir eine Spieleausleihe.','vielleicht waere ein ruhiger Pausenraum moeglich.','ich faende gemuetliche Sitzmoeglichkeiten gut.'],
'C - ZUSATZ +':['Dann koennten wir dort in Ruhe lesen.','Das wuerde unsere Pausen abwechslungsreicher machen.','So haetten mehr Kinder einen Platz zum Sitzen.','Die Pflanzen wuerden den Raum freundlicher machen.','So koennten Kinder gemeinsam tuefteln.','Viele Kinder aus unserer Klasse finden die Idee gut.','Dort koennte man sich kurz zurueckziehen.','Man koennte zuerst nur wenige Sitzkissen ausprobieren.'],
'D - GRUSS':['Viele Gruesse\nMia','Viele Gruesse\nNoah','Freundliche Gruesse\nElif','Viele Gruesse\nBen','Viele Gruesse\nLina','Freundliche Gruesse\nSamir','Viele Gruesse\nAylin','Viele Gruesse\nJonas']}
rec=['Klassenleitung','Schulleitung','Hausmeister','Ganztagsteam','Sportlehrkraft','SV','Schulsozialarbeit','Mensateam','Sekretariat','Bibliotheks-Team','Techniklehrkraft','Klassenrat']
wish=['Spieleausleihe','neue Baelle','ruhiger Pausenraum','zusaetzliche Sitzplaetze','Leseecke','Pflanzen im Klassenraum','Ablagefaecher','gemuetliche Sitzmoeglichkeiten','Sport-AG','Technik-AG','Theater-AG','Kreativ-AG']

os.makedirs(os.path.dirname(OUT),exist_ok=True); c=canvas.Canvas(OUT,pagesize=A4); c.setTitle('Offener Anfang - Wunschbriefe'); p=1
# Uebersicht
head(c,'OFFENER ANFANG - WUNSCHBRIEFE','Druckpaket Deutsch 5 - sechs selbststaendig nutzbare Angebote',p)
c.setFillColor(K); c.setFont('Helvetica-Bold',12); c.drawString(14*mm,PH-48*mm,'Einsatz')
txt(c,'Die ersten Minuten der Stunde sind als freie Wahlphase gedacht. Die Materialien sind nach einer kurzen Einfuehrung selbststaendig, analog und moeglichst mit Selbstkontrolle nutzbar.',14*mm,PH-56*mm,PW-28*mm,10.2,lead=13)
y0=PH-82*mm
for i,o in enumerate(offers):
    y=y0-i*24*mm; col=B if i%2==0 else R; c.setStrokeColor(col); c.roundRect(14*mm,y-18*mm,PW-28*mm,19*mm,2*mm,stroke=1,fill=0); c.setFillColor(K); c.setFont('Helvetica-Bold',10); c.drawString(18*mm,y-5*mm,f'{i+1}. {o[0]}'); c.setFillColor(M); c.setFont('Helvetica',8); c.drawString(18*mm,y-11*mm,f'{o[1]} - {o[2]} - {o[3]}'); txt(c,o[4][0],93*mm,y-5*mm,PW-111*mm,8.2,lead=10,n=2)
c.setFillColor(R); c.setFont('Helvetica-Bold',9); c.drawString(14*mm,25*mm,'Praxistipp'); txt(c,'Lege die Angebote in beschrifteten Umschlaegen oder kleinen Boxen aus. Kontrollkarten bleiben separat und werden erst nach der Bearbeitung genutzt.',14*mm,20*mm,PW-28*mm,8.5,lead=10)
c.showPage(); p+=1
# 6 Anleitungskarten
head(c,'DIE SECHS ANGEBOTE','Anleitungskarten - ausschneiden und zum Material legen',p); mx=12*mm; top=PH-40*mm; gx=4*mm; gy=4*mm; cw=(PW-2*mx-gx)/2; ch=75*mm
for i,o in enumerate(offers):
    x=mx+(i%2)*(cw+gx); y=top-(i//2+1)*ch-(i//2)*gy; col=B if i%2==0 else R; border(c,x,y,cw,ch,col); c.setFillColor(col); c.setFont('Helvetica-Bold',7); c.drawString(x+6*mm,y+ch-13*mm,f'ANGEBOT {i+1} - {o[2]} - {o[1]}'); c.setFillColor(K); c.setFont('Helvetica-Bold',13); c.drawString(x+6*mm,y+ch-23*mm,o[0]); c.setFillColor(M); c.setFont('Helvetica',7.8); c.drawString(x+6*mm,y+ch-34*mm,'Material: '+o[3]); steps(c,o[4],x+6*mm,y+ch-43*mm,cw-12*mm,col,8.2); txt(c,'Selbstkontrolle: '+o[5],x+6*mm,y+8*mm,cw-12*mm,6.9,'Helvetica-Oblique',8.2,M,2)
cut(c,PW/2,18*mm,PW/2,PH-38*mm)
for r in (1,2): cut(c,7*mm,top-r*ch-(r-.5)*gy,PW-7*mm,top-r*ch-(r-.5)*gy)
c.showPage(); p+=1
# Wahlkarte
head(c,'ANGEBOT 1 - ANKOMMEN & WAEHLEN','Selbstregulatives Angebot - laminieren und wiederverwenden',p); c.setFillColor(K); c.setFont('Helvetica-Bold',14); c.drawString(14*mm,PH-48*mm,'Wie moechtest du heute starten?'); c.setFillColor(M); c.setFont('Helvetica',10); c.drawString(14*mm,PH-56*mm,'Waehle eine Moeglichkeit, die heute zu deiner Energie und deinem Ziel passt.')
choices=[('RUHIG','Ich moechte erst einmal allein und ohne viel Sprechen arbeiten.','Wunsch-Detektiv oder Satzbau-Werkstatt'),('KNIFFLIG','Ich moechte meinen Kopf direkt ein bisschen herausfordern.','Briefteile-Domino oder schwierige Detektivkarte'),('ZU ZWEIT','Ich moechte mit jemandem gemeinsam denken und sprechen.','Freundlich oder nicht? oder Brief-Blitz'),('WIEDERHOLEN','Ich moechte etwas ueben, bei dem ich noch nicht ganz sicher bin.','Waehle das Angebot, das zu deinem Lernbedarf passt.')]
for i,q in enumerate(choices):
    ww=(PW-32*mm)/2; x=14*mm+(i%2)*(ww+4*mm); y=PH-78*mm-(i//2+1)*55*mm-(i//2)*5*mm; col=B if i in (0,2) else R; border(c,x,y,ww,55*mm,col); c.setFillColor(col); c.setFont('Helvetica-Bold',12); c.drawString(x+6*mm,y+37*mm,q[0]); txt(c,q[1],x+6*mm,y+28*mm,ww-12*mm,9,lead=11); c.setFillColor(M); c.setFont('Helvetica-Bold',7.5); c.drawString(x+6*mm,y+11*mm,'PASSENDES ANGEBOT'); txt(c,q[2],x+6*mm,y+7*mm,ww-12*mm,7.4,lead=8.5,col=M)
c.setStrokeColor(L); c.roundRect(14*mm,24*mm,PW-28*mm,34*mm,2*mm,stroke=1,fill=0); c.setFillColor(R); c.setFont('Helvetica-Bold',9); c.drawString(19*mm,48*mm,'NACH EIN PAAR MINUTEN'); c.setFillColor(K); c.setFont('Helvetica',9); c.drawString(19*mm,41*mm,'War deine Wahl passend?   [ ] Ja     [ ] Vielleicht     [ ] Nein'); c.setFillColor(M); c.setFont('Helvetica',8); c.drawString(19*mm,32*mm,'Wenn nicht: Waehle beim naechsten Mal anders. Das ist eine gute Lernentscheidung.')
c.showPage(); p+=1
# Domino A/B
for title,sub,data,col in [('ANGEBOT 2 - BRIEFTEILE-DOMINO - SET A','Grundlagen - ausschneiden',[('START','Wer soll den Brief lesen?'),('EMPFAENGER','Liebe Frau Koenig,'),('ANREDE','Hier steht der eigentliche Inhalt des Briefes.'),('BRIEFTEXT','Ich wuensche mir eine Spieleausleihe.'),('WUNSCH','Viele Gruesse'),('GRUSSFORMEL','Mina'),('NAME','Ist der Brief vollstaendig, freundlich und verstaendlich?'),('KONTROLLE','ZIEL')],B),('ANGEBOT 2 - BRIEFTEILE-DOMINO - SET B','Erweiterung - fuer spaeter in der Reihe',[('START','Das waere gut, weil wir gemeinsam spielen koennten.'),('GRUND +','In unserer Umfrage haben 18 von 26 Kindern die Idee gewaehlt.'),('UMFRAGEDATEN +','Vielleicht ist dafuer nicht genug Platz.'),('BEDENKEN *','Man koennte zuerst nur zwei Sitzkissen ausprobieren.'),('LOESUNG *','Koennten Sie bitte pruefen, ob das moeglich ist?'),('FREUNDLICHE BITTE','Das ist wichtig, weil ...'),('BEGRUENDUNG','Passt mein Zusatz wirklich zu meinem Wunsch?'),('KONTROLLE','ZIEL')],R)]:
    head(c,title,sub,p); tw=87*mm; th=31*mm; ytop=PH-48*mm
    for i,(a,b) in enumerate(data):
        x=[14*mm,109*mm][i%2]; y=ytop-(i//2+1)*th-(i//2)*5*mm; c.setStrokeColor(col); c.roundRect(x,y,tw,th,2*mm,stroke=1,fill=0); c.setStrokeColor(L); c.line(x+tw/2,y+3*mm,x+tw/2,y+th-3*mm); c.setFillColor(col); c.setFont('Helvetica-Bold',9); c.drawCentredString(x+tw/4,y+th/2,a); ls=wrap(b,'Helvetica',8.5,tw/2-8*mm); c.setFillColor(K); c.setFont('Helvetica',8.5); yy=y+th/2+4*mm
        for z in ls[:3]: c.drawCentredString(x+3*tw/4,yy,z); yy-=9.5
    for r in (1,2,3): cut(c,10*mm,ytop-r*th-(r-.5)*5*mm,PW-10*mm,ytop-r*th-(r-.5)*5*mm)
    cut(c,PW/2,18*mm,PW/2,PH-40*mm); c.showPage(); p+=1
# Domino Key
head(c,'KONTROLLKARTEN - DOMINO','Nach dem Legen vergleichen',p)
for j,(name,seq,col) in enumerate([('SET A - GRUNDLAGEN',['START','EMPFAENGER','ANREDE','BRIEFTEXT','WUNSCH','GRUSSFORMEL','NAME','KONTROLLE','ZIEL'],B),('SET B - ERWEITERUNG',['START','GRUND +','UMFRAGEDATEN +','BEDENKEN *','LOESUNG *','FREUNDLICHE BITTE','BEGRUENDUNG','KONTROLLE','ZIEL'],R)]):
    y=PH-68*mm-j*92*mm; c.setStrokeColor(col); c.roundRect(14*mm,y,PW-28*mm,72*mm,3*mm,stroke=1,fill=0); c.setFillColor(col); c.setFont('Helvetica-Bold',12); c.drawString(20*mm,y+59*mm,name); c.setFillColor(K); c.setFont('Helvetica',9); yy=y+48*mm
    for i in range(len(seq)-1): c.drawString(20*mm,yy,f'{i+1}. {seq[i]}  ->  {seq[i+1]}'); yy-=6*mm
c.showPage(); p+=1
# Sort pages
head(c,'ANGEBOT 3 - FREUNDLICH ODER NICHT?','Sortierfelder und erste neun Karten',p); fy=PH-95*mm
for i,(lab,col,sub) in enumerate([('PASST GUT',B,'freundlich, klar und passend'),('MUSS BESSER WERDEN',R,'zu direkt, unfreundlich oder uebertrieben')]):
    x=14*mm+i*93*mm; c.setStrokeColor(col); c.roundRect(x,fy,88*mm,43*mm,3*mm,stroke=1,fill=0); c.setFillColor(col); c.setFont('Helvetica-Bold',12); c.drawCentredString(x+44*mm,fy+28*mm,lab); c.setFillColor(M); c.setFont('Helvetica',8); c.drawCentredString(x+44*mm,fy+17*mm,sub)
cw=(PW-32*mm)/3; ch=35*mm; sy=fy-12*mm
for i,t in enumerate(good):
    x=14*mm+(i%3)*(cw+2*mm); y=sy-(i//3+1)*ch-(i//3)*3*mm; border(c,x,y,cw,ch,B,); txt(c,t,x+6*mm,y+ch-16*mm,cw-12*mm,9,lead=10,n=3)
c.showPage(); p+=1
head(c,'ANGEBOT 3 - SORTIERKARTEN & KONTROLLE','Restliche neun Karten und Loesungshinweise',p)
for i,t in enumerate(bad):
    x=14*mm+(i%3)*(cw+2*mm); y=PH-55*mm-(i//3+1)*ch-(i//3)*3*mm; border(c,x,y,cw,ch,R); txt(c,t,x+6*mm,y+ch-16*mm,cw-12*mm,9,lead=10,n=3)
c.setStrokeColor(L); c.roundRect(14*mm,26*mm,PW-28*mm,72*mm,3*mm,stroke=1,fill=0); c.setFillColor(B); c.setFont('Helvetica-Bold',10); c.drawString(20*mm,85*mm,'KONTROLLKARTE'); c.setFillColor(K); c.setFont('Helvetica',8); c.drawString(20*mm,75*mm,'Die neun Karten von der vorherigen Seite passen gut. Beispiele fuer Verbesserungen:'); yy=66*mm
for t in ['Ich will sofort ... -> Ich wuensche mir ...','Sie muessen ... -> Koennten Sie bitte pruefen, ob ...','Machen Sie das! -> Es waere schoen, wenn ...','Alle wollen ... -> Viele Kinder finden die Idee gut.']:
    c.drawString(24*mm,yy,'- '+t); yy-=8*mm
c.showPage(); p+=1
# Detektiv 2 pages
for batch in range(2):
    head(c,f'ANGEBOT 4 - WUNSCH-DETEKTIV - KARTEN {batch*4+1}-{batch*4+4}','Zieh eine Karte - lies - finde drei Hinweise',p); ww=(PW-32*mm)/2; hh=103*mm
    for j in range(4):
        idx=batch*4+j; num,letter,a1,a2,a3=det[idx]; x=14*mm+(j%2)*(ww+4*mm); y=PH-48*mm-(j//2+1)*hh-(j//2)*5*mm; col=B if idx<6 else R; border(c,x,y,ww,hh,col); c.setFillColor(col); c.setFont('Helvetica-Bold',8); c.drawString(x+6*mm,y+hh-14*mm,'KARTE '+num); c.setFillColor(K); c.setFont('Helvetica-Bold',10); c.drawString(x+6*mm,y+hh-24*mm,'Lies den Mini-Brief.'); yy=y+hh-33*mm; c.setFont('Helvetica',8.7)
        for para in letter.split('\n'):
            for z in wrap(para,'Helvetica',8.7,ww-12*mm): c.drawString(x+6*mm,yy,z); yy-=9.5
            yy-=2
        c.setStrokeColor(L); c.line(x+6*mm,y+29*mm,x+ww-6*mm,y+29*mm); c.setFillColor(B); c.setFont('Helvetica-Bold',8); c.drawString(x+6*mm,y+23*mm,'FINDE:'); c.setFillColor(K); c.setFont('Helvetica',8); c.drawString(x+6*mm,y+17*mm,'1. Wer bekommt den Brief?'); c.drawString(x+6*mm,y+12*mm,'2. Was ist der Wunsch?'); c.drawString(x+6*mm,y+7*mm,'3. Welche Stelle klingt besonders freundlich?')
    c.showPage(); p+=1
head(c,'KONTROLLKARTE - WUNSCH-DETEKTIV','Antworten zu Karten 1-8',p); yy=PH-48*mm
for i,(num,letter,a1,a2,a3) in enumerate(det):
    col=B if i<6 else R; c.setStrokeColor(col); c.roundRect(14*mm,yy-27*mm,PW-28*mm,25*mm,2*mm,stroke=1,fill=0); c.setFillColor(col); c.setFont('Helvetica-Bold',8.5); c.drawString(19*mm,yy-8*mm,'KARTE '+num); c.setFillColor(K); c.setFont('Helvetica',7.7); c.drawString(43*mm,yy-8*mm,'Empfaenger: '+a1); txt(c,'Wunsch: '+a2,43*mm,yy-14*mm,73*mm,7.5,lead=8.2); txt(c,'Freundlich: '+a3,121*mm,yy-8*mm,69*mm,7.5,lead=8.2); yy-=30*mm
c.showPage(); p+=1
# Satzbau 2 pages
allc=[]
for cat,vals in cats.items():
    for v in vals: allc.append((cat,v))
for batch in range(2):
    head(c,f'ANGEBOT 5 - SATZBAU-WERKSTATT - KARTEN {batch+1}/2','A + B + optional C + D = Mini-Brief',p); ww=(PW-32*mm)/4; hh=48*mm
    for j in range(16):
        cat,t=allc[batch*16+j]; x=14*mm+(j%4)*(ww+1.3*mm); y=PH-46*mm-(j//4+1)*hh-(j//4)*3*mm; col=B if cat[0] in 'AB' else R; border(c,x,y,ww,hh,col); c.setFillColor(col); c.setFont('Helvetica-Bold',6.3); c.drawString(x+5*mm,y+hh-13*mm,cat); fs=8.7 if len(t)<45 else 8; y0=y+hh-23*mm
        for para in t.split('\n'):
            for z in wrap(para,'Helvetica',fs,ww-10*mm)[:3]: c.setFillColor(K); c.setFont('Helvetica',fs); c.drawString(x+5*mm,y0,z); y0-=9
    c.showPage(); p+=1
head(c,'SATZBAU-WERKSTATT - BEISPIELKARTE','Viele Loesungen sind moeglich',p); c.setFillColor(K); c.setFont('Helvetica-Bold',12); c.drawString(14*mm,PH-50*mm,'So baust du einen Mini-Brief:'); steps(c,['Waehle genau eine Karte A (Anrede).','Waehle genau eine Karte B (Wunsch).','Wenn du moechtest, ergaenze eine Karte C (Zusatz).','Waehle eine Karte D (Gruss).','Lies alles zusammen und pruefe: freundlich, klar, verstaendlich?'],14*mm,PH-62*mm,PW-28*mm,B,10)
c.setStrokeColor(R); c.roundRect(14*mm,78*mm,PW-28*mm,82*mm,3*mm,stroke=1,fill=0); c.setFillColor(R); c.setFont('Helvetica-Bold',10); c.drawString(20*mm,146*mm,'BEISPIEL'); c.setFillColor(K); c.setFont('Helvetica',11); y=134*mm
for z in ['Liebe Frau Koenig,','ich wuensche mir eine Leseecke.','Dann koennten wir dort in Ruhe lesen.','Viele Gruesse','Mia']:
    c.drawString(24*mm,y,z); y-=10*mm
txt(c,'Andere Kombinationen sind ebenfalls richtig, wenn Anrede, Wunsch, moeglicher Zusatz und Gruss zusammenpassen.',20*mm,88*mm,PW-40*mm,8.5,lead=10,col=M)
c.showPage(); p+=1
# Brief Blitz 2 pages
for title,data,col,label in [('ANGEBOT 6 - BRIEF-BLITZ - STAPEL EMPFAENGER',rec,B,'EMPFAENGER'),('ANGEBOT 6 - BRIEF-BLITZ - STAPEL WUNSCH',wish,R,'WUNSCH')]:
    head(c,title,'Ausschneiden - verdeckt stapeln',p); ww=(PW-32*mm)/3; hh=48*mm
    for i,t in enumerate(data):
        x=14*mm+(i%3)*(ww+2*mm); y=PH-48*mm-(i//3+1)*hh-(i//3)*4*mm; border(c,x,y,ww,hh,col); c.setFillColor(col); c.setFont('Helvetica-Bold',7); c.drawString(x+6*mm,y+hh-14*mm,label); fs=11 if len(t)<25 else 10; c.setFillColor(K); c.setFont('Helvetica-Bold',fs); ls=wrap(t,'Helvetica-Bold',fs,ww-12*mm); yy=y+hh-27*mm
        for z in ls[:2]: c.drawCentredString(x+ww/2,yy,z); yy-=13
    c.showPage(); p+=1
c.save(); print('generated',OUT,'pages',p-1)
