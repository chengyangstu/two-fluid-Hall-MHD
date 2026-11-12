import json,fitz
from pathlib import Path
P=Path(__file__).resolve().parents[1]
p=P/'research/reading_notes/verified.json';v=json.loads(p.read_text())
for k in ['Toth2008','Arnold2008']:
 v[k]['figures_checked']=v[k]['figures_checked'].replace('；图像复核待补','；主要结果图表视觉核验');v[k]['status']='正文完整阅读；核心图与参数核验'
v['Arnold2008']['implementation_check']='所读v1式21逆矩阵(3,1)写为+cy；由式20直接相乘可知应为-cy。属于本报告代数核对，未断言期刊版本相同。'
v['Ren2005']={'pages_read':'055003-1至4（全部4页）','figures_checked':'图1-4及式1；图像复核待补','model':'MRX无初始净导引场的H/D实验；二维磁探针与高分辨率1D扫描。','parameters':'71通道径向间距1.25mm，系统误差小于10G；90通道2D图轴向4cm、径向扫描1cm且多次放电平均；重联约40微秒对Alfven约1微秒。','finding':'四极Hall磁场高分辨率50-60G，对重联场约100G；粗2D图20-40G。Hall结构径向约di、轴向约5di；碰撞率指标delta/lambda_mfp由.2到20，BHall/Brec约.6降.25。','limitation':'电子20km/s由电流及电子承担假设推断，并非直接流速测量；Hall电场140V/m对Erec约100V/m是上游量级估计，部分区域BR不准，未全项闭合，也不证明Hall在X点断线。误差棒为放电差异。','assessment':'强证据是四极场的空间极性及碰撞率关联；与湍动同时存在，不能排除其他耗散机制。','status':'正文完整阅读；图像复核待补'}
v['GuideExp2012']={'pages_read':'PPPL-4753全部8页（正文编号1-5，含封面说明）','figures_checked':'图1-7、式1-3；图像复核待补','model':'MRX外加可控环向导引场；counterhelicity pull，磁场探针测Hall项与感应电场，中心Langmuir探针测n/Te。','parameters':'Bg/Brec从0到约1；delta约2cm，di约5cm，rho_s约2.5cm；Hall项取X点上游3cm、下游5cm，归一化使用重联分量Brec而非总场。','finding':'导引场改变四极场形状与幅值，重联率降低比典型局地模拟更强；磁通芯阻碍排气，环向导引场被压缩、堆积，对全局压力平衡产生影响。','limitation':'正文明确不能把速率降低分成局部Hall与全局边界两部分；密度仅中心一点，完整压力平衡/离子流速测量留待未来。所读是PPPL预印本，式号图号以此版本为准。','assessment':'边界可显著控制观察到的导引场依赖；不可当成所有开边界空间重联的普适Bg标度。','status':'正文完整阅读；图像复核待补'}
v['Huang2011']={'pages_read':'1-25（arXiv v2全部）','figures_checked':'图1-11、式1-6；图像复核待补','model':'二维等温、标量压力、无电子惯性、电阻Hall MHD；HMHD五点差分/梯形leapfrog；psi、By演化保证二维散度。','parameters':'S=5e5，L/di=2500,5000,10000，对照纯电阻；T=3，导体滑移边界，仅上半域，6400乘1024非均匀网格，最小dx=1.2e-4L,dz=1.4e-5L；另在Sdi=100扫描L/di500,1000,2500。','finding':'2500形成持久单X点；5000经历磁岛触发Hall、排岛、再拉长到约500di、再生岛的间歇循环，率.005-.03；10000未进入Hall。主SP宽大于di时，次级薄层仍可触发。较大系统在相同Sdi下片更长更宽、开放角更小。','limitation':'Hall分支仍由电阻断线；此循环与无碰撞PIC连续产岛机制不等同。宽度定义为四分之一峰值全宽，不能与半高半宽直接比（.7di对应.17di）。相图边界仅统计估计，Sdi临界随系统尺寸未得到定律；对太阳日冕/磁尾Spitzer参数该中间区未必适用。','assessment':'破除Hall必然单X点的说法，但不能由形状相像认定动力学机制一致。小系统欧姆项与收敛支持电阻可单独维持Hall分支，作者与Cassak2010有实质争论。','status':'正文完整阅读；图像复核待补'}
p.write_text(json.dumps(v,ensure_ascii=False,indent=2))
c=json.loads((P/'research/catalog.json').read_text())
for k,pgs in [('Ren2005',[2,4]),('GuideExp2012',[5,6]),('Huang2011',[11,19])]:
 r=next(r for r in c if r['key']==k);d=fitz.open(P/r['local_pdf'])
 for pg in pgs:d[pg-1].get_pixmap(matrix=fitz.Matrix(1.15,1.15)).save(P/f'research/qa/{k}_{pg}.png')
print('Records',len(v))
