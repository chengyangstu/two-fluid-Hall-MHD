# coding: utf-8
import json,hashlib,requests,fitz
from pathlib import Path
P=Path(__file__).resolve().parents[1]
p=P/'research/catalog.json';c=json.loads(p.read_text());b={r['key']:r for r in c}
r=b['L296']
if not r.get('alternate_versions'):
 r['alternate_versions']=[{k:r.get(k) for k in ['year','arxiv','local_pdf','download_url','sha256','pages']}]
r.update(year=2025,date='2025-04-01',doi='10.1016/j.jcp.2025.113789',journal='Journal of Computational Physics',type='article',
 authors=['Luis Chacón'],local_pdf='papers/L296_accepted.pdf',pages=29,
 download_url='https://www.osti.gov/servlets/purl/2520135',
 sha256=hashlib.sha256((P/'papers/L296_accepted.pdf').read_bytes()).hexdigest(),
 identity_check='题名作者、OSTI接收稿封面DOI和期刊出版信息一致；接收稿电子惯性/能量模型不同于2024 arXiv v1；全文判断以接收稿为准。')
r['landing_urls'].append('https://doi.org/10.1016/j.jcp.2025.113789')
for a,z in [('F613','L116'),('F663','L160')]:
 b[a]['duplicate_of']=z;b[a]['identity_check']='首页题名作者与预印本号及文件SHA256相同，版本重复。'
b['L116'].update(doi='10.1051/0004-6361:200809624',journal='Astronomy and Astrophysics')
# Two same-title papers, 2005 and 2008, are different studies.
r=b['L076'];old={k:r.get(k) for k in ['local_pdf','download_url','sha256','pages']}
url='https://www.physics.udel.edu/~shay/papers/Sullivan.PoP.2005.pdf'
resp=requests.get(url,timeout=50);resp.raise_for_status();d=fitz.open(stream=resp.content,filetype='pdf')
assert '1.2146910' in d[0].get_text()
path=P/'papers/L076_2005.pdf';path.write_bytes(resp.content)
r.update(local_pdf='papers/L076_2005.pdf',pages=len(d),download_url=url,
 sha256=hashlib.sha256(resp.content).hexdigest(),
 identity_check='2005期刊首页DOI与三作者已核。先前0906.0334实际上是2008年同题二维/三维续篇，保留在F717；不能按同题合并。',
 previous_mismatch=old,urls=[url],landing_urls=['https://doi.org/10.1063/1.2146910'])
b['F717'].update(arxiv='0906.0334',identity_check='首页两作者和三维研究；DOI/2008年出版信息经作者机构出版目录核对。与2005同题文章不同，不合并。')
p.write_text(json.dumps(c,ensure_ascii=False,indent=2))
p=P/'research/reading_notes/verified.json';v=json.loads(p.read_text())
v['L296']=dict(
 status='正文完整阅读；核心图与参数核验',
 pages_read='2025 OSTI接收稿封面及正文/附录全部29页（正文1-28）；2024 arXiv v1全部25页亦读，用于版本核对',
 figures_checked='图1-4、表1全部视觉核验；模型式5/6与附录A-C逐式检查',
 model='可压缩Hall流体，固定Ti/Te温比，p由加权速度vstar输运。接收稿改用de² De(j/rho)惯性以匹配v≈vi下能量；不是精确有限质量双流体。全部实际测试de=0。',
 parameters='二阶单元中心有限体积、矢势兼容curl；波用Crank-Nicolson、GEM用BDF2。Newton-FGMRES与物理块Schur、多重网格V(3,3)、阻尼Jacobi .7；EMHD内层GMRES最多10次或残差降至.1。'
 'GEM256²拉伸网格，最小dx.02/dy.05，dt.05、di1、eta.005、nu_i.05、nu_e1e-4、kappa.02、温比5。弱扩展32²单MPI至4096²/16384MPI，dt.01、100步。',
 finding='Hall电子块与离子流动块分离的预条件降低刚性求解迭代；波相位和HiFi GEM能量曲线吻合，多数非线性阶段接近，末期约1%差。'
 '16384倍问题规模时总时间132至1130秒，2-3次Newton/外层GMRES每步；隐式步比显式CFL最高8400，实际速度最高75倍，粗网格反而慢25倍。',
 limitation='弱扩展而非强扩展；nu_e随细网格由1e-4降至6e-9，非固定物理参数收敛。性能段总时长1，早于GEM非线性启动约20。'
 '附录平滑分析仅均匀周期、无背景电子流、de0、刚性及足够网格黏性条件；不是一般异质三维证明。'
 '理论能量含电子应力而实现动量忽略它，GEM另以v替vstar匹配HiFi；形式定理与实际算例须分开。'
 '密度初值印刷为sech而非与tanh平衡相容的sech²；热能定义多写1/2，不能机械照抄，未核代码不判实现错误。',
 assessment='解决大时间步求解成本的重要方法证据；没有验证有限de、全三维或任意高S新物理。预条件中的近似不能当成实际残差删除物理项；接受稿与v1必须区分。')
p.write_text(json.dumps(v,ensure_ascii=False,indent=2))
print('full reads',len(v),'L076 corrected pages',len(d))
