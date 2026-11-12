# coding: utf-8
import json
from pathlib import Path
P=Path(__file__).resolve().parents[1]
p=P/'research/reading_notes/verified.json';v=json.loads(p.read_text())
def add(k,pages,fig,model,params,finding,limit,assess):
 v[k]=dict(pages_read=pages,figures_checked=fig,model=model,parameters=params,finding=finding,limitation=limit,assessment=assess,status='正文完整阅读；核心图与参数核验')
add('L256','期刊PDF1-16全部',
 '图1-10及表1；图1、3-6、8-10与表1视觉复核',
 '全Maxwell十矩、对压力偏离各向同性的部分作Laplacian闭合，不是直接扩散完整温度；以Vlasov热流高阶矩作对照。',
 'GEM质量比25、256×128基准及1024×512加密；另流体质量比400/1836。'
 'k0s分别为GEM3/ds、100×50di WHBG的1/(3ds)、岛合并1/(2ds)；不是一组参数全场景。'
 '岛lambda5/10/15/25di，两套网格512×256到2048×1024。',
 '原松弛闭合的热流散度形状和符号在某些区域错误；梯度闭合改善上游假热流与电子非对角压力。'
 '岛合并平均0-1.5tA率标度约lambda^(-.73)，出现反弹且无二次岛。表1lambda5至25平均率.180→.052；两套网格差小。'
 'GEM高分辨梯度流体后期斜率近Vlasov，但启动仍迟；高分辨局地松弛反而更慢。',
 'k0按与动理学一致调节，尺寸标度也依赖k0；不能宣称无参预测。'
 '实际质量比只展示流体结构，不是同质量比完整动理学验证。'
 '显式Laplacian子循环中不交换块边界、不更新速度密度，作者承认块边界误差。'
 'GEM温度条件缺常规1/2，岛平衡坐标与边界文字不一致，复现需输入核对。',
 '重要改进是直接检查热流矩再验证非线性反弹；其成功同时有问题相关的校准与数值限制。')
add('E552','arXiv2008.06440v3 1-20全部，对应2021年期刊',
 '图1-9；闭合式、图4、6-9视觉复核',
 '全Maxwell五矩与十矩比较；压力偏离各向同性的梯度闭合chi3,k0s1/ds；Vlasov用于二维电流片不稳定性对照。',
 'CWENO+RK3，Maxwell FDTD，Laplacian二阶中心，每子循环交换压力边界，三维用8次；压力对角下限。'
 '三维100×25×6di、2400×600×150、mi/me100,c/VA30，Harris a.5,nb.2,Ti/Te5；磁通种子.1、电子密度噪1e-8。'
 '独立静电LHDI nb.001、Ti/Te10、a约.67、质量比36/100/250至流体1836。',
 '静电LHDI质量比100时Vlasov/十矩梯度/五矩/十矩松弛增长率2.2/2.4/3.2/.67 Omega_i；'
 '最快模随质量比变化，固定单一模比较会误导。电磁支Vlasov约.41、流体.21，均出现超过B0的磁扰动及强kink。'
 '三维较二维启动早、后期片变宽，出流湍动强而电子层相对适中；密度噪1e-10至1e-2使LHDI启动约30→4 Omega_i^-1。',
 '高质量比无同参数Vlasov验证；电磁支结构、启动与增长仍不同，异常高饱和原因未解释。'
 'CSSI只是形态相似的候选，未确诊。三维率是z平均电场代理；电子de约2.4格，未给全三维网格收敛。'
 '对角下限不等于完整压力正定保证；印刷Lap约+k0²应理解为负号Fourier符号。',
 '该工作同时检验重联与不稳定性并强调噪声/启动竞争，优于仅比较峰值；但不能把3D形态相近称为完整动理学等价。')
p.write_text(json.dumps(v,ensure_ascii=False,indent=2));print(len(v))
