"""Render changed synthesis, selected new dossiers, navigation and bibliography."""
from pathlib import Path
import json,re
import pymupdf
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parents[1];Q=P/'research/ion_heating';R=Q/'renders'
c={r['key']:r for r in json.loads((P/'research/catalog.json').read_text(encoding='utf-8'))}
batch=json.loads((P/'specific problems/离子加热问题/batch_manifest.json').read_text(encoding='utf-8'))
names=['01_theory_numerics','02_paper_results','03_solved_open'];selected=[]
for name in names:
 d=pymupdf.open(P/'分卷'/f'{name}.pdf');pages={1,2,len(d)}
 if name=='02_paper_results':
  keys={r['key'] for r in batch['records'] if r['new_full_read']}
  for p in d:
   txt=re.sub(r'\s','',p.get_text())
   if any(k+'：'+str(c[k]['year'])+'年' in txt for k in keys):pages.update({p.number+1,min(p.number+2,len(d))})
   if any(s in txt for s in ['双温Hall已经能算局地加热','从轨道展宽到两物种熵产','实验的2:1究竟是哪一个比例','11月12日加热专题']):pages.add(p.number+1)
 if name=='03_solved_open':
  for p in d:
   if '离子加速怎样变成不可逆热化' in re.sub(r'\s','',p.get_text()):pages.update({p.number+1,min(p.number+2,len(d))})
 for n in sorted(pages):
  out=R/f'updated_{name}_p{n}.png';d[n-1].get_pixmap(matrix=pymupdf.Matrix(1.4,1.4)).save(out)
  selected.append((name,n,out))
for start in range(0,len(selected),4):
 canvas=Image.new('RGB',(1280,1840),'#ddd');draw=ImageDraw.Draw(canvas)
 for j,(name,n,path) in enumerate(selected[start:start+4]):
  im=Image.open(path);im.thumbnail((615,875));x=j%2*640;y=j//2*920
  canvas.paste(im,(x+12,y+30));draw.text((x+12,y+8),f'{name} PDF page {n}',fill='black')
 canvas.save(R/f'updated_contact_{start//4+1}.png')
(Q/'updated_render_manifest.json').write_text(json.dumps({'date':'2026-11-12','pages':[[s,n] for s,n,p in selected],
 'contacts':(len(selected)+3)//4,'note':'All new dossier starting pages and following pages; synthesis updates, covers, navigation and references. Viewing recorded separately.'},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('Rendered',len(selected),'pages in',(len(selected)+3)//4,'contacts')
