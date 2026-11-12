# -*- coding: utf-8 -*-
import json
from pathlib import Path
P=Path(__file__).resolve().parents[1]
p=P/'research/reading_notes/verified.json';v=json.loads(p.read_text())
def add(k,pages,fig,model,params,finding,limit,assess):
 v[k]=dict(pages_read=pages,figures_checked=fig,model=model,parameters=params,finding=finding,limitation=limit,assessment=assess,status='正文完整阅读；核心图与参数核验')
for k in ['Huang2011','Cassak2010','Huang2024','Ng2020','Closure2026']:
 v[k]['figures_checked']+='；主要结果页已视觉复核'
add('L049','1-11全部','图1-5，PDF第5-7、9页视觉复核',
 '作者团队强导引场约化双流体及漂移动理学结果综述；二维Hamilton两场；暖电子模型需保留抵消抗磁漂移惯性的压力张量修正。',
 'psi0=-L/[2cosh²(x/L)]，Lx=2Ly=4pi L，Nx=2048,Ny=1024，de=.3L,rho_s/de=0-1.5；只一个线性不稳定模，随机扰动。',
 '暖电子G±不断卷绕细丝，粗粒化磁岛可饱和而总能量守恒；冷电子极限出现二次KH、单极和偶极涡，岛形脉动与流体／电子动能交换；rho_s/de接近1时饱和前未见KH。漂移动理学按不同正则动量薄片发生不同方向卷绕。',
 '第573页明确暖电子细丝无限变薄导致流体近似不一致；综述未给完整算法细节；未证明三维、任意尺度或热化过程。',
 '可以学习磁拓扑与广义拓扑不相同以及宏观饱和不等于微观静止；不能把细丝当成已被解析的真实耗散。')
add('Rogers2001','1-4全部','图1-4；图3、4视觉核验',
 '二维等温双流体，电子惯性，周期双电流片；EMHD和约化KAW机制推导及完整线性两流体色散关系。',
 '主要扫描mi/me=82.6,Lx×Ly=20di×10di,w0=di，Bg/Bx=3和30；另用质量比300；早期图1盒10×5di、质量比300；正文未报告网格及耗散实现。',
 '同时允许whistler和KAW时率约.12；仅一分支约.06；强导引冷等离子体无二次色散波时率显著低、长片。控制量mu_k=(me/mi)(c_A²+c_s²)/c_Ak²与beta_k/2=c_s²/c_Ak²，而非单独Bg/Bx。',
 '线性波向非线性外推时By随时间空间变化，图2用Bx上游作方便替代，作者明确承认；不是任意闭合、对等离子体或动理学的必要条件定理；无网格收敛展示。',
 '证据支持其等温流体模型的波模／几何关联，后来的压力机制及动理学反例需要单独核验。')
add('Schep1994','PDF1-11全部（正文2843-2852）','式1-18视觉复核；图1、2及全文理论',
 '低beta强导引场、等温电子，平行离子流忽略，保留电子惯性和电子陀螺黏性抵消；离子响应采用全FLR非线性构造。',
 '频率低于离子回旋／磁声、高于离子声响应；slab,yz周期；定常传播解背景指数密度及线性磁剪切；本文无时变重联模拟网格。',
 '构造能量与非正则Hamilton结构，二维有两族电子Casimir，冻结组合是Psi_e±de sqrt(beta_e) ln(n/n0)，不是Psi或Psi_e；有限惯性去掉电流本身的奇点，但梯度仍可能很大，广义通量X点分离。',
 '第2845页明确全FLR离子方程是ansatz，并非从Vlasov严格推导；第2849页未求解完整非线性本征问题；第2851页指出相关传播尺度Landau共振使流体模型失效；机构库封面年份错误，正文1994。',
 '适合严谨说明约化模型的构造条件与守恒；不能把全FLR构造称为完整动力学或已完成数值重联验证。')
add('Ottaviani1993','JET-P(93)66 PDF1-16全部，扫描件OCR后核关键公式与图','图1-4，关键式11和图3视觉核验',
 '无耗散、不可压、二维周期冷两场惯性模型，忽略Larmor、密度和压强梯度，F=psi-de²lap psi被输运。',
 'psi0=cos x,Lx=pi,epsilon=Lx/Ly=.5,de/(2Lx)=.04，Delta′de约2.03，仅m=1不稳定；伪谱1024×64 Fourier分量；t约125小尺度不可解析而终止。',
 '早期非线性de<w<<Lx内对流胞保持宏观结构，电流子层按delta~de exp(-位移/de)缩窄，流速层仍约de；幅度方程A″约A+c2 A^4给准爆发增长。',
 '是早期非线性与大Delta′结果；到宏观岛宽时增长变慢的另一计算仅文字报告；不能把有限时形式发散当成物理无限电流；无收敛扫描且细层未解析后主动停止。读取的是投稿前JET版，不冒充期刊最终版逐字核对。',
 '重要新现象是多尺度电流／速度结构与非线性加速，排除了该序列中必然Sweet–Parker式减速；不提供任意参数的最终饱和／热化预测。')
p.write_text(json.dumps(v,ensure_ascii=False,indent=2))
c=json.loads((P/'research/catalog.json').read_text())
for r in c:
 if r['key'] in v:r['read_status']=v[r['key']]['status']
(P/'research/catalog.json').write_text(json.dumps(c,ensure_ascii=False,indent=2));print('verified',len(v))
