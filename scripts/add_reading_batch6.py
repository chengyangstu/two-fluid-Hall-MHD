# coding: utf-8
import json
from pathlib import Path
P=Path(__file__).resolve().parents[1]
p=P/'research/reading_notes/verified.json';v=json.loads(p.read_text())
def add(k,pages,fig,model,params,finding,limit,assess):
 v[k]=dict(pages_read=pages,figures_checked=fig,model=model,parameters=params,finding=finding,limitation=limit,assessment=assess,status='正文完整阅读；核心图与参数核验')
add('Malyshkin2008','arXiv0810.3278v2 1-5全部，含发表后说明',
 '图1及式11-26，PDF3-4页视觉核验',
 '二维不可压、标量压力、均匀电阻、无导引无电子惯性Hall MHD；准稳态局地泰勒展开。',
 '没有新数值模拟；外给Bm及L²=-2Bm/(dyy By)_up；电阻用磁扩散单位；S=LVA/eta。',
 'Ez/(BmVA)约sqrt(sqrt(3)/S+2di²/L²)。Hall强时电子层delta约eta L/(VA di)、离子层Delta约di，率约di/L。'
 '注意电子层上游离子Vin约VA L/(Sdi)很小，而离子层外磁通输入VR约VA di/L；两者不能混称。',
 'L和Bm必须由全局解确定，未由本理论求出；小电阻极限电子电流发散且电子惯性/压力张量被删去。'
 '条件Ez远小于BmVA且无层内不稳定性；不能外推di/L约1。热化密度反馈仅讨论，没有求解能量方程。',
 '给出局地Hall层的连接标度，未解决全局率选择；正文中的collisionless不能读成X点无需非理想项。')
add('Malyshkin2009','arXiv0904.0660v3 1-4全部',
 '图1、式3-23与讨论；PDF2-3页视觉核验',
 '二维准中性常密度双流体，标量压力、有限电子惯性、均匀有效电阻、准稳态、无导引。',
 '无新模拟；扩展动量保留-de²(j·grad)j；全局Bext、Lext给定，局地电子半长L与离子尺度区分。',
 '惯性强支给delta约de、离子厚di、电子喷流约电子Alfven速度；Ez约eta Bext/de，L约VA de di/eta。'
 '离子在电子层内可很慢，在电子喷流减速区才继续加速；存在可同时容纳SP与较快支的参数窗。',
 '率显式正比电阻；collisionless命名指把eta解释为待动理学计算的有效电阻。'
 'Hall过渡支的长度未唯一求出，转变路径是假说；稳态模型不能描述迟滞过程。'
 '预测长度me^(1/2)与所引PIC的me^(3/8)不同；实验层宽约8倍差异仍未解释。',
 '这是有残余有效耗散的稳态惯性理论，不与Andres的非稳态无电阻拓扑变化等价。')
add('Simakov2009','LANL2008-09-29预稿PDF1-34全部，期刊2009年PoP扩展篇',
 '式1-25逐页图像核对、两页35算例表及图1-4全部视觉核验',
 '二维不可压高beta Hall MHD；无电子惯性、无导引；均匀电阻加超电阻；离散区域解析近似加非线性岛合并。',
 'Fadeev平衡epsilon=.2，35算例di=0至1、eta=0至1e-3；表中etaH最高7.6e-6（正文写7.6e-7不一致）。'
 '解析电流形状系数mu=16；在峰值时测电子片厚/长、上游Bin，比较半高宽与速度峰两定义。'
 '本文未列实际网格、时间步和边界截断，数值算法指向Chacon-Knoll2003。',
 '统一匹配SP与电子Hall极限，强Hall局地率约sqrt(2)di/w；'
 '电子层细长也可耗散系数不显含的快率，超电阻造成开放X形却仍可处于慢支；有限四极Bz本身不判快。'
 '35算例归一化率跨度约1200倍，理论比值范围.5-2.3；固定这组岛合并的强Hall区率大致随di上升。',
 '一般过渡公式是两渐近极限的插值，层长w和Bin从模拟取值，并未预测宏观驱动选择。'
 '忽略电子惯性产生过快电子喷流和大于动理学常见值的局地率；不能无条件推至di无限大。'
 '只比较峰值附近准稳态，未完成整段时史理论。预稿题名与PRL2008短文相近但不是同一篇。',
 '是电子层几何与率的有用定量检验，不是全部参数都由初值唯一预测的全局理论。')
p.write_text(json.dumps(v,ensure_ascii=False,indent=2));print(len(v))
