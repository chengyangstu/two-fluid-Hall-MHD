# -*- coding: utf-8 -*-
import json
from pathlib import Path
P=Path(__file__).resolve().parents[1];p=P/'research/reading_notes/verified.json';v=json.loads(p.read_text())
def add(k,pages,fig,model,params,finding,limit,assess):
 v[k]=dict(pages_read=pages,figures_checked=fig,model=model,parameters=params,finding=finding,limitation=limit,assessment=assess,status='正文完整阅读；核心图与参数核验')
add('Baalrud2011','arXiv1108.3129v1 1-8全部','图1-9，图8-9视觉复核',
 '不可压标量压力、无电子惯性、电阻Hall四场；SP平衡宽度随S变化，扰动电阻内层d_eta小于di而di小于delta_SP。',
 '线性本征对照S_L=1e8,di/L=1e-5,3e-5,1e-4；非线性岛合并L=1,S=1e6,di=1e-5至1e-3；算法网格引用前作未完整列出。',
 '最快模gamma/Gamma0约3.2(di/L)^(6/13)S^(7/13)，kmax L约2.9(di/L)^(1/13)S^(11/26)，Gamma0=2vA/L；全局层仍长薄时扰动已出现四极Bz。非线性提取的增长率在di/L约2e-4转折，与d_eta约1.8e-4吻合。',
 '非线性计算只确认转折，作者承认无法精确验证6/13指数；gamma>>Gamma0,k delta_SP<<1与三层排序限制适用范围；不是非线性最终率公式。PDF自动日期2018与arxiv2011不一致，按arxiv版本记录。',
 'Hall先影响撕裂内层再改变全局平衡是重要发现；不能把线性指数和稳定单X点视为同一结论。')
add('Cassak2008','期刊PDF1-5全部','表1、图1-3，PDF第2-3页视觉复核',
 'F3D2D反平行非对称双周期Harris；绝热离子gamma5/3、冷电子；电子惯性近似采用常密度且忽略离子速度。',
 '204.8di×102.4di,dx=.05di,mi/me25,w0=2di,beta_min4；无二阶电阻黏性，所有方程四阶扩散约6.25e-6 di³ vAmax；磁噪5e-5,速度噪.08。场比至3、密度比至4。',
 '九组算例率与混合Alfven标度基本一致；对称基准率.0587，离子喷流.685vA、电子2.067vA；离子／电子停滞点及X点可三者分离；磁岛向弱场鼓起，片向强场移动。两种率测法差1-10%。',
 '电子惯性未一致保留密度不对称；高beta、无导引、二维；另一离子流速定义绝对值差60%但标度相同。作者限可可靠研究的不对称度<4；更大时电子片失真；表1ABN1行p、T、rho不相容，复现需查原始输入。',
 '支持有限范围的反平行标度，不证明磁层顶强不对称与导引场情形普适0.1。')
add('Andres2014','arXiv1312.2437v2 1-8全部','图1-5；式28、图4视觉核验',
 '常密度不可压、标量压力、完整电子惯性准中性双流体，非全Maxwell；伪谱、无显式电阻／黏性。',
 '周期2pi×2pi，双tanh半厚2pi*.02,psi扰动.02cos x,Hall .1；网格512²-2048²；me/mi .015及1/1836；总能误差<1e-8,初始零两类螺度维持1e-15。',
 '随分辨率提高理想MHD与Hall的伪重联趋零，而有限惯性通量趋非零；真实质量比案例峰值接近.1，质量比两值总体趋势相似。',
 '未扫描Hall与种子；守恒总能并非所有局地梯度准确的充分条件。真实质量比de约.00233，2048网格dx约.00307，不能凭全局通量相近声称充分解析电子层。预印本式28右端印为(2delta-1)导致物理质量比下右端负，与图1实频不相容，报告不照抄。',
 '最强证据是无惯性对照加网格扫描；结果只在其标量不可压模型内支持惯性作用，不排除真实动理学压力张量。')
add('Andres2016','arXiv1509.01169v1 1-8全部','式15-16与图4-6视觉复核',
 '同常密度不可压惯性Hall双流体，无显式耗散；提出准稳态局地量纲标度。',
 '周期2pi方盒,2048²,me/mi=.015,Hall λ=.07至.16步长.01共十组，初始片厚2pi*.02、psi扰动.02cos x；另λ.1比较me/mi .015与.15。',
 '电流拟合厚度delta约(1.3±.3)lambda_e^(1.06±.07)；固定设置中Bin约.25-.3、半长约.45-.6变化弱；准稳态率r约(.11±.07)λ^(.98±.03)，增Hall时峰值提前。',
 '只是2.3倍参数窗；取delta与Bin近恒定时段，非严格稳态；局地改用B0=Bin,L0=Delta才写r=λ，实际原归一化系数约.11。预印本式15惯性旋度项符号、式16两等号不一致；严格对称X点若停滞且稳态，标量压力无电阻模型不能用稳态对流惯性独自支撑Ez。',
 '数值有限窗线性趋势可记录；稳态X点解析推导需保留时间惯性或澄清局地估算位置，不能直接推广普适长度规律。')
p.write_text(json.dumps(v,ensure_ascii=False,indent=2));c=json.loads((P/'research/catalog.json').read_text())
for r in c:
 if r['key'] in v:r['read_status']=v[r['key']]['status']
(P/'research/catalog.json').write_text(json.dumps(c,ensure_ascii=False,indent=2));print(len(v))
