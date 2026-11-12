# coding: utf-8
import json
from pathlib import Path
P=Path(__file__).resolve().parents[1]
p=P/'research/reading_notes/verified.json';v=json.loads(p.read_text())
def add(k,pages,fig,model,params,finding,limit,assess):
 v[k]=dict(pages_read=pages,figures_checked=fig,model=model,parameters=params,finding=finding,limitation=limit,assessment=assess,status='正文完整阅读；核心图与参数核验')
add('Yamada2018','期刊PDF1-11全部；未核读补充电影',
 '图1-8与表1-2；PDF4、8-10页视觉核验',
 'MRX氦放电与MMS2015-10-16观测，辅以VPIC全粒子模拟；不是双流体流体求解器。',
 '密度比约10，无显著导引场；MRX电子流由Ui-J/(en)反演。'
 'VPIC40di×20di，4200×2100，mi/me100，omega_pe/omega_ce2，400粒子/格/物种约70亿总粒子；'
 't=96/omega_ci在2.5di×3di盒积分能量。',
 '强不对称时Hall四极接近双极，电子与离子停滞点、X点分离；电子停滞点偏移5-10de，离子约0.3-0.5di。'
 '电子能量转移集中于电子停滞点且垂直电功主导；离子被偏向低密度侧的势阱加速，MMS有反向离子束而实验较热化。'
 '表2非对称MRX入射磁能归一化后出射磁能.44、离子.31、电子.25；PIC分别.43/.32/.25。',
 'MMS有限轨迹不能检验全局能量分配；电场滤除高于离子回旋频率成分，不能用此排除高频能量交换。'
 '作者未找到波幅与率的确定关系。MRX电子速度是推算；模拟二维且质量比100。'
 '方法段将X写周期、Z写导体/反射，与X为片法向及单tanh初值需澄清，复现前应查输入文件。',
 '支持跨尺度两种粒子解耦形态及近X点能量转移图样；不能据此宣称Hall项本身耗散，或五矩/十矩闭合已被验证。')
add('Shay2004','期刊2199-2213共15页全部',
 '表1、图1-11；图3-5、8、10及方程视觉核验',
 '二维F3D准中性等温Hall加常系数电子惯性Bprime=(1-de²lap)B；非完整可压双流体惯性。',
 '全周期正弦双片，n1-1.5,T=1,mi/me25；Lx51.2-409.6di,Ly12.8-102.4di，通常dx=.1di、de=.2di。'
 '四阶耗散所有方程mu4=5.1e-5；run7 dx=.05、mu4=5e-7。四个大算例初始岛半宽.55di；加B及离子流噪声1e-4。',
 '局地Bd用离子Jz峰的25%位置定义，上游/下游边界并非任意取di；下游取离子电子流速交点。'
 '大系统后期Vin约.1局地Alfven速度，进入该阶段时岛半宽约6.1-9.9di。最大算例最后3%时段完成约90%磁通重联、75%岛宽增长。'
 '小Delta-prime时即使呈X形，压力背压抵消张力仍慢；大Delta-prime时电子层变薄、Hall增强伴离子层从长片缩短。',
 '无导引场、单质量比；质量比无关只是援引先前研究和预期。启动持续时间强依赖尺寸与初值，非普适0.1。'
 'de仅两格，run7同时改网格和耗散不能当作单独网格扫描。局地Bd定义含25%阈值；迟期边界干扰后停止比较。'
 '印刷式2以Ji为粒子通量却压力项写T/n grad n，且温度文字Ti+Ti，不能照抄作一致守恒方程。',
 '关键贡献是分开启动与快速阶段、实际测定局地上游场；宏观归一化与局地归一化不同，不能据后期结果抹去启动难题。')
p.write_text(json.dumps(v,ensure_ascii=False,indent=2))
c=json.loads((P/'research/catalog.json').read_text())
for r in c:
 if r['key']=='Yoo2018':r['key']='Yamada2018'
 if r['key'] in v:r['read_status']=v[r['key']]['status']
(P/'research/catalog.json').write_text(json.dumps(c,ensure_ascii=False,indent=2))
print(len(v))
