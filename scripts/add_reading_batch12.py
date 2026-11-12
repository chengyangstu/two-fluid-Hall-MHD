# coding: utf-8
import json
from pathlib import Path
P=Path(__file__).resolve().parents[1];p=P/'research/reading_notes/verified.json';v=json.loads(p.read_text())
def add(k,pages,fig,model,params,finding,limit,assess):
 v[k]=dict(pages_read=pages,figures_checked=fig,model=model,parameters=params,finding=finding,
 limitation=limit,assessment=assess,status='正文完整阅读；核心图与参数核验')
add('L263','arXiv1906.05961v2全文1-13页；版面自动日期2021不改期刊2019年',
 '图1-8正文图注；图2/4-8与模型页逐图视觉核验',
 '2.5D可压缩标量绝热Hall MHD，显式均匀电阻；无电子惯性、电子压力项、压力张量或欧姆热反馈。',
 '双周期8×.8，双Harris片，rho∞=T=B=1，a0=.02；4096×2048、dx.00195/dy.000391，eta1e-5、S1e5。'
 '谱微分、显式RK3；相同随机相位1-128模种子；di=0/.001/.002/.003/.004/.005/.01七组。种子幅度、去混叠和过滤细节未列。',
 '递归生岛、开放X点持续喷出次级岛、较强Hall开放无次级岛三种情形。Hall增大使启动提前、排气角约10至28度。'
 '固定归一化磁通斜率.032至.058；MHD晚期.034高于最弱Hall.032，不是Hall组在任意时段总更快。'
 '面内电流的电阻耗散占比由40%趋55%，平行占比约45%；这是eta Jperp²而非Hall项直接做功。'
 '中心线By谱由浅段约-.8及陡段-2转为近单幂-2.22；Ez谱不同且小尺度Ex可占主导。',
 '高阶最细片已到网格尺度；X点半长高di收敛到约.007仅3-4个dx，作者承认可能分辨率限制。'
 '没有独立网格/eta扫描，速率上限.06不宜普适化；谱是固定中心线和不同时间窗，不等于体积各向同性湍流谱。'
 '绝热压力不接收etaJ²，所以“耗散”是磁能移除诊断，不是自洽粒子加热分配。'
 '波数用周期频率N/L约定，角波数需乘2pi；没有3D及压力各向异性。',
 '补强Hall既能提前次级增长又能改变后期岛产生的证据；所谓Hall抑岛需明确阶段、几何、耗散和分辨率。')
add('L312','2026-11-04 Article in Press全文1-15页（含Methods）；下载49页透明同行评议文件，但不计为已逐页核读',
 '图1-9全部图注；图3/4/6-9、表1及式1-9视觉/数值核验',
 'MRX实验、MMS/PSP事件与VPIC全动理学对照；使用双流体电子动量分析，不是Hall MHD数值计算。',
 'MRX氢气3.5mTorr，320-340μs，约250个有清晰EBCS的重复放电平均，di2.5cm；高分辨一维探针z6di。'
 'MMS2017-06-19、PSP2021-04-29各一例。小PIC20×20di/1280²、mi/me1836、Ti/Te5；大PIC200×40di/4032×800、mi/me100、Ti/Te1、初始半厚5di，开放流出，均ωpe/ωce2、2000粒子/格。'
 'MRX几何PIC30×60di、200×448、质量比25、ωpe/ωce1、200粒子/物种/格、dtωpe.24。',
 '沿分离线延伸的双峰电流、电势井、离子加速和排气密度增强在三环境出现；MRX两侧片厚拟合.29/.70di，MMS排气约20di，PSP约4000di且边界约20di。'
 'MRX电势估算12/6V与测量11/5V近；MMS估算6/5kV与测量5/7kV量级近；PSP电场不确定无法检验。'
 '低beta .012大岛破坏长程边界，.12/.36局部延伸，1.2大域保持至边界。MMS扣除上游温度后的焓流占优，PSP体流能流占优。',
 '主数值为PIC，不能证明任意Hall/五矩闭合均能重现。实验按EBCS明显事件挑选，两个空间个例及假定Ti=Te的实验beta不构成普适阈值统计。'
 '漂移电流吻合只在强Ex分离线时窗；下游距离由几何长宽比推断；1D磁梯度诊断在多维区失效。'
 '式4的Delta B²应由磁压差积分理解；原文式1交叉项符号需连同坐标手性核查。'
 'PIC大/小盒同时改变质量比和温比，未给独立网格/质量比收敛；代码公开但自定义分析需索取。'
 '2026-11-10访问其Figshare API返回404，不能声称已取得源数据。',
 '新实验对照目标是分离线电流层的宏观延伸和能量分配差异；势井标度可用Hall/双流体检验，低杂波、束分布和准确加热仍需张量/动理学及3D。')
p.write_text(json.dumps(v,ensure_ascii=False,indent=2))
p=P/'research/catalog.json';c=json.loads(p.read_text());b={r['key']:r for r in c}
for k,z in [('F678','Cassak2005'),('F595','L271'),('F699','L295')]:
 b[k]['duplicate_of']=z;b[k]['identity_check']='PDF首页/作者、同一arXiv标识与期刊DOI映射核实，版本重复；2026-11-10。'
b['L271']['arxiv']='2104.12013';b['L271']['alternate_title']='Magnetic reconnection as an energy cascade process'
b['L295']['arxiv']='2307.05736';b['L295']['scope']='扩展边界：离子—中性双流体'
b['L312']['supplementary_files']=[{'path':'papers/L312_peer_review.pdf','type':'透明同行评议，未逐页核读','url':'https://static-content.springer.com/esm/art%3A10.1038%2Fs41467-026-79220-2/MediaObjects/41467_2026_79220_MOESM1_ESM.pdf'}]
b['L312']['identity_check']='出版商Article in Press首页题名作者DOI核对；2026-11-04，非最终排版。数值为PIC，实验/机制对照范围。'
b['L263']['identity_check']='arXiv1906.05961v2首页与期刊题名作者核对；自动排版2021日期不代表出版年。'
for k in ['L279','Simakov2008']:
 if not b[k].get('local_pdf') and b[k].get('sha256'):
  b[k]['mismatched_pdf_sha256']=b[k].pop('sha256')
p.write_text(json.dumps(c,ensure_ascii=False,indent=2));print('full reads',len(v))
