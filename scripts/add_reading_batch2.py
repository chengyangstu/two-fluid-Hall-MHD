import json,fitz
from pathlib import Path
P=Path(__file__).resolve().parents[1]
cp=P/'research/catalog.json';c=json.loads(cp.read_text())
r=next(r for r in c if r['key']=='Allmann2020');r['key']='Ng2020'
r['version_note']='所读为2020-07-26作者稿；作者Ng等。旧内部键Allmann2020已纠正。'
cp.write_text(json.dumps(c,ensure_ascii=False,indent=2))
old=P/'research/text/Allmann2020.txt'
if old.exists():old.rename(P/'research/text/Ng2020.txt')
for f in list((P/'sections').glob('*.tex'))+[P/'scripts/catalog.py']:
 f.write_text(f.read_text().replace('Allmann2020','Ng2020'))
p=P/'research/reading_notes/verified.json';v=json.loads(p.read_text())
for k in ['Ren2005','GuideExp2012','Huang2011']:
 v[k]['figures_checked']=v[k]['figures_checked'].replace('；图像复核待补','；主要结果图视觉核验')
 v[k]['status']='正文完整阅读；核心图与参数核验'
v['Cassak2010']={
 'pages_read':'062105-1至7（全部）',
 'figures_checked':'图1-8；图像复核待补',
 'model':'以片宽为变量的鞍结分岔现象学模型；F3D双流体与无电子惯性Hall对照。',
 'parameters':'409.6×204.8di,dx=.1；有限质量比25的旧例D4=2e-5，无惯性新例D4=8e-5作用全部方程，初始片宽1.2di,T=1,eta=.012，磁种子.004与随机5e-6。',
 'finding':'无惯性下相同eta仍有快慢支与迟滞；片宽相图有非单调结构，电子出流随层变薄增加，与k约1/delta的双流体波速相关。',
 'limitation':'模型没有自洽给出层长；因上游场随时间变，正文明确不做片宽演化定量比较。无惯性算例保留更强超电阻，不能称无耗散。Hall-电阻平衡必然不稳定的论断后来被Huang2011在其他几何中反驳。',
 'assessment':'强证据是关闭电子惯性仍保留历史依赖；对任意电阻Hall层不稳定的外推需要保留争论。2010称已做收敛，不等于2005正文展示了独立收敛曲线。',
 'status':'正文完整阅读；图像复核待补'}
v['Huang2024']={
 'pages_read':'1-11（arXiv v2全部）',
 'figures_checked':'图1-9；图像复核待补',
 'model':'三维可压Hall MHD，标量绝热压力、pe=pi、无电子惯性，电阻黏性超电阻；压力方程不含显式耗散加热。',
 'parameters':'立方盒、两磁通管合并，h=.01L,Bg约Brec,初始pi=pe=1,rho=1,gamma=5/3；S=2e5,Pm=1,di/L=.002或.001；etaH=1e-13；网格2000×1000×2000（40亿格），中心dy=1e-4L；x/y导体滑移,z周期。',
 'finding':'同参二维均趋单X线；三维L/di500也趋准二维，1000保持自生湍动与多重联点。单X线例通量率与磁能下降更快，Hall湍动态快于电阻MHD但慢于单X线。中面涡各向异性近尺度无关，远离中面大涡部分恢复GS标度。',
 'limitation':'三维率取z平均场的二维X点磁通，是代理诊断，不是全部3D连通性。亚di尺度不足，k^-11/3只是参考线，未确证幂律。结构函数限于x-z切片，不能直接与全3D采样比较；仅两组di/固定S。',
 'assessment':'三维自由度可保留湍动但非必然加速。Petschek相似仅几何，不证明慢激波机制；闭合与真实电子物理仍未检验。',
 'status':'正文完整阅读；图像复核待补'}
v['Ng2020']={
 'pages_read':'1-8（作者稿全部，含附录A）',
 'figures_checked':'图1-7、式4-6、附录A；图像复核待补',
 'model':'十矩全Maxwell温度梯度热流，与局地各向同性化和非局地无磁化闭合比较；FV输运、局地隐式源、超时间步抛物子步。',
 'parameters':'Fadeev与Ng2015同系；lambda5di用640×320，同dx扫描系统尺寸，mi/me25,k0s=1/ds；导引场0-.4-1-2等。LHDI另例mi/me36,Ti/Te10,L=rhoi,vt,e=.06c,盒6.4L×12.8L,模数8。',
 'finding':'平均率随岛尺寸下降可接近PIC约lambda^-0.8；岛合并最大率随Bg升到1先升后降，不能套用Harris片单调下降。离子宽层及非旋转对称度改善。相同k0=1/ds可同时激发重联与LHDI。',
 'limitation':'LHDI增长率默认1.33Ωci、调k为ky后.86，动力学1.1，局地闭合.34，非局地.84；仍非完全吻合。电子各向异性空间结构仍不准、跨场热流过大；未研究LHDI对重联的非线性作用。附录指出零热流、无碰撞的对称稳态停滞点会驱动不物理Pxx趋零。',
 'assessment':'梯度闭合并非更高阶就自动正确；改善来自k²/|k0|的尺度选择，仍有自由参数和磁化缺失。',
 'status':'正文完整阅读；图像复核待补'}
v['Closure2026']={
 'pages_read':'1-23（arXiv2602.16960v1全部，含附录A）',
 'figures_checked':'图1-11、附录A1及式A1-A12；图像复核待补',
 'model':'Gkeyll三维非对称十矩；温度梯度闭合与局地闭合对照；顶点对称热扩散和alpha=.75限制器。',
 'parameters':'盒40.96×20.48×10.24di，全周期双电流片，1152×576×288，mi/me100,c/vA200,Bg/Bsx=.099；nm/ns=.062,Bxm/Bxs=-1.696,Tem/Tes12.3,Tim/Tis5.63；k0αdα约1，磁噪声.0005，psi种子.1。',
 'finding':'梯度闭合出现约5Ωci^-1内LHDI、约20后kink与通量绳/次级岛，局地同参不出现；三维率先峰后降，压力张量支撑X点非理想场。梯度闭合成本约3倍。',
 'limitation':'温度各向异性峰值侧别与MMS/PIC不符，非旋转对称度与各向异性区域过宽，作者认为背景跨场扩散产生不物理各向异性。独立2D Vlasov对照kink仅数个离子周期出现，流体需数十周期，且遗漏小尺度模。正文未给质量比/网格独立收敛序列。',
 'assessment':'证明某些先前受抑制的横向不稳定性可在十矩中出现，不是准确恢复全部三维动理学。建议的磁场方向热流及弱各向同性化仍为未来改进。',
 'implementation_check':'v1方程含归一化/符号需复核之处：Maxwell式5、局地闭合式10、附录对称化因子与A9/A10；报告用维度与耗散符号重新推导，不机械抄写，代码复现需对照公开输入与实现。',
 'status':'正文完整阅读；图像复核待补'}
p.write_text(json.dumps(v,ensure_ascii=False,indent=2))
for k,pgs in [('Cassak2010',[4,5]),('Huang2024',[5,6,7]),('Ng2020',[3,5,8]),('Closure2026',[4,8,11,14,17,19])]:
 r=next(r for r in c if r['key']==k);d=fitz.open(P/r['local_pdf'])
 for pg in pgs:d[pg-1].get_pixmap(matrix=fitz.Matrix(1.1,1.1)).save(P/f'research/qa/{k}_{pg}.png')
print('Records',len(v))
