"""Build the reviewed A5 worksheets from the shared content source (python-docx)."""
from pathlib import Path
import json
from docx import Document
from docx.shared import Cm,Pt,RGBColor
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'materialien/arbeitsblaetter/arbeitsblaetter_inhalte.json'
OUT=ROOT/'materialien/arbeitsblaetter/Arbeitsblaetter_1-24_DIN_A5_ueberarbeitet.docx'
D=Document()
s=D.sections[0];s.page_width=Cm(14.8);s.page_height=Cm(21)
s.top_margin=Cm(.8);s.bottom_margin=Cm(.8);s.left_margin=Cm(.9);s.right_margin=Cm(.9)
s.footer_distance=Cm(.3)
for name,size in [('Normal',14),('Heading 1',16),('Heading 2',14)]:
 st=D.styles[name];st.font.name='Arial';st.font.size=Pt(size);st.font.color.rgb=RGBColor.from_string('24313A')
 st.paragraph_format.space_after=Pt(5);st.paragraph_format.space_before=Pt(0);st.paragraph_format.line_spacing=1.02
 st.paragraph_format.keep_with_next=name!='Normal'
D.core_properties.title='Wunschbriefe · Arbeitsblätter 1–24 · Fassung 3'
D.core_properties.author='Deutschunterricht'
D.core_properties.subject='Schritt 2 · 7. September 2026'
def para(t,bold=False,size=None):
 p=D.add_paragraph();r=p.add_run(t);r.bold=bold
 if size:r.font.size=Pt(size)
 return p

def band(label,t,color='EEF2F4'):
 p=D.add_paragraph();p.paragraph_format.space_before=Pt(4);p.paragraph_format.space_after=Pt(6)
 r=p.add_run(label+('\n' if '\n' in t else ': '));r.bold=True;p.add_run(t)
 sh=OxmlElement('w:shd');sh.set(qn('w:fill'),color);p._p.get_or_add_pPr().append(sh)
 return p

def table(rows):
 widths=[1.5,11.5] if rows[0][0]=='Nr.' else [8.1,4.9]
 ts=[round(x*1440/2.54) for x in widths]
 t=D.add_table(rows=0,cols=2);t.autofit=False
 pr=t._tbl.tblPr
 for name,value in [('tblW',sum(ts)),('tblInd',80)]:
  el=pr.find(qn('w:'+name))
  if el is None:el=OxmlElement('w:'+name);pr.append(el)
  el.set(qn('w:w'),str(value));el.set(qn('w:type'),'dxa')
 m=OxmlElement('w:tblCellMar')
 for k in ['top','bottom','left','right']:
  el=OxmlElement('w:'+k);el.set(qn('w:w'),'60' if k in ['top','bottom'] else '80');el.set(qn('w:type'),'dxa');m.append(el)
 pr.append(m)
 for i,v in enumerate(ts):t._tbl.tblGrid.gridCol_lst[i].set(qn('w:w'),str(v))
 for rowi,row in enumerate(rows):
  rw=t.add_row();rw._tr.get_or_add_trPr().append(OxmlElement('w:cantSplit'))
  for j,txt in enumerate(row):
   c=rw.cells[j];c.width=Cm(widths[j]);c._tc.get_or_add_tcPr().find(qn('w:tcW')).set(qn('w:w'),str(ts[j]))
   p=c.paragraphs[0];p.paragraph_format.space_after=Pt(3);r=p.add_run(txt);r.bold=rowi==0
   if rowi==0:
    sh=OxmlElement('w:shd');sh.set(qn('w:fill'),'E5EDF2');c._tc.get_or_add_tcPr().append(sh)
  if rowi==0:rw._tr.get_or_add_trPr().append(OxmlElement('w:tblHeader'))
 return t
for item in json.loads(DATA.read_text()):
 p=para('Blatt '+str(item['n']),True,20);p.paragraph_format.space_after=Pt(3);p.paragraph_format.page_break_before=item['n']>1
 para(item['status'],True)
 D.add_paragraph(item['title'],'Heading 1')
 band('Dein Ziel',item['goal'])
 for b in item['blocks']:
  if b[0]=='task':
   p=para(b[1],True);p.paragraph_format.space_before=Pt(12);p.paragraph_format.keep_with_next=True
   para(b[2])
  elif b[0]=='text':para(b[1])
  elif b[0]=='checks':
   for line in b[1]:para('☐ '+line)
  elif b[0]=='box':band(b[1],b[2],'F5F4F1' if b[1]!='Zusatz · freiwillig' else 'F9F0E9')
  elif b[0]=='table':table(b[1])
 band('Hilfe',item['help'],'EDF4EA')
 band('Prüfe',item['check'])
D.save(OUT)
print(OUT)
