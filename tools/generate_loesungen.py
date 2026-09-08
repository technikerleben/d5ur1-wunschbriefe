"""Single source for the offline kiosk and printable worksheet solutions."""
from pathlib import Path
import json,re
from docx import Document
from docx.shared import Cm,Pt,RGBColor
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'materialien/arbeitsblaetter'
data=json.loads((OUT/'loesungen_inhalte.json').read_text());works=json.loads((OUT/'arbeitsblaetter_inhalte.json').read_text())
assert list(data)==[str(i) for i in range(1,25)]
assert all(data[str(w['n'])]['title']==w['title'] for w in works)
f=ROOT/'apps/kontroll-kiosk/index.html';html=f.read_text();public={k:{x:v[x] for x in ['title','tip','type','solution','extra','status']} for k,v in data.items()}
encoded=json.dumps(public,ensure_ascii=False).replace('</','<\\/')
if '/* DATA_START */' not in html:
 html=re.sub(r'const DATA=.*?;let mode=null',lambda m:'/* DATA_START */const DATA='+encoded+';/* DATA_END */let mode=null',html,count=1,flags=re.S)
else:html=re.sub(r'/\* DATA_START \*/.*?/\* DATA_END \*/',lambda m:'/* DATA_START */const DATA='+encoded+';/* DATA_END */',html,flags=re.S)
f.write_text(html)
d=Document();s=d.sections[0];s.page_width=Cm(14.8);s.page_height=Cm(21);s.top_margin=s.bottom_margin=Cm(.8);s.left_margin=s.right_margin=Cm(.9)
for name,size in [('Normal',14),('Title',20),('Heading 1',16),('Heading 2',14)]:
 st=d.styles[name];st.font.name='Arial';st.font.size=Pt(size);st.font.color.rgb=RGBColor.from_string('24313A');st.paragraph_format.space_after=Pt(6);st.paragraph_format.space_before=Pt(0);st.paragraph_format.line_spacing=1.0;st.paragraph_format.keep_with_next=name!='Normal'
d.core_properties.title='Lösungspaket Arbeitsblätter 1–24 · Fassung 3';d.core_properties.author='Deutschunterricht'
for n,item in data.items():
 p=d.add_paragraph('Blatt '+n,'Title');p.paragraph_format.page_break_before=n!='1';d.add_paragraph(item['title'],'Heading 1')
 for label,body in [('Tipp',item['tip']),('Lösung und Vergleich',item['solution']),('Zusatz · freiwillig',item['extra']),('Hinweis für die Lehrkraft',item['teacher'])]:
  if body:d.add_paragraph(label,'Heading 2');d.add_paragraph(body)
d.save(OUT/'Loesungspaket_Arbeitsblaetter_1-24_Wunschbriefe.docx')
print('Kiosk data and DOCX generated from 24 reviewed records.')
