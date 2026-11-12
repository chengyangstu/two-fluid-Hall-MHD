import json,requests,fitz,hashlib
from pathlib import Path
P=Path(__file__).resolve().parents[1];c=json.loads((P/'research/catalog.json').read_text())
items=[('Shay2003','10.1029/2002gl016267','https://ireap.umd.edu/Theory/Publications/pub2003-2.pdf'),
('Katz2010','10.1103/physrevlett.104.255004','https://pdfs.semanticscholar.org/5682/b6a5e15c4d41ad39045cebadd4679b4516dc.pdf')]
for k,d,u in items:
 r=next((r for r in c if r.get('doi','').lower()==d),None)
 if r is None:
  a=requests.get('https://api.crossref.org/works/'+d,timeout=30).json()['message']
  r=dict(key=k,doi=d,title=a['title'][0],authors=[x.get('given','')+' '+x.get('family','') for x in a['author']],year=a['published']['date-parts'][0][0],journal=a['container-title'][0],scope='引用追踪补充',read_status='未读',urls=[u],landing_urls=['https://doi.org/'+d],arxiv='')
  c.append(r)
 k=r['key'];rr=requests.get(u,timeout=30);rr.raise_for_status();a=fitz.open(stream=rr.content,filetype='pdf');f=P/'papers'/f'{k}.pdf';f.write_bytes(rr.content)
 (P/'research/text'/f'{k}.txt').write_text('\n'.join(p.get_text() for p in a))
 r.update(local_pdf='papers/'+k+'.pdf',download_status='PDF已取得，待身份与全文核验',download_url=u,pages=len(a),sha256=hashlib.sha256(rr.content).hexdigest())
 print(k,len(a),r['title'])
 for i in range(len(a)):a[i].get_pixmap(matrix=fitz.Matrix(1.3,1.3)).save(str(P/'research/qa'/f'{k}_p{i+1}.png'))
(P/'research/catalog.json').write_text(json.dumps(c,ensure_ascii=False,indent=2))
