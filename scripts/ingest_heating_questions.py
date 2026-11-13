"""Record the four main versions actually read on 2026-11-13; not a downloader."""
from pathlib import Path
import json, hashlib
P = Path(__file__).resolve().parents[1]
T = P/'specific problems/离子加热问题'
Q = P/'research/ion_heating/questions_20261113'
Q.mkdir(exist_ok=True)
def read(p): return json.loads(p.read_text(encoding='utf-8'))
def write(p, x): p.write_text(json.dumps(x, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
if not (Q/'baseline.json').exists():
    write(Q/'baseline.json', {n:read(P/'research/ion_heating'/n) for n in ['progress.json','visual_review.json','updated_render_manifest.json','topic_audit.json']})
rows = [
dict(key='Haggerty2015Partition',title='The competition of electron and ion heating during magnetic reconnection',authors=['C. C. Haggerty','M. A. Shay','J. F. Drake','T. D. Phan','C. T. McHugh'],year=2015,journal='Geophysical Research Letters',doi='10.1002/2015GL065961',arxiv='1504.02110',pages=23,
version='arXiv:1504.02110v3作者稿，23页；期刊2015，arXiv v3为2016；PDF内部DRAFT时间戳不当作发表年',
pages_read='PDF 1–23全部：正文1–15，致谢/参考文献16–19，独立大图20–23；无文内附录。独立Supporting Information未取得。',
figures_checked='图1–4（PDF 20–23）全部直接查看；PDF 10–11式(1)–(4)直接查看；图3未修正、图4电势修正后的散点不可互换。',
model='2.5D P3D全动理学PIC，反平行、对称、零导引场；离子束与电子约束电势解析解释，不是Hall两温闭合',
parameters='双周期204.8×102.4 di0，入流约100粒子/格，质量比25与100；扫描上游B、n、温度；稳态平均100步约50/ωpe。完整参数表、网格、时间步和部分平均方法依赖未取得的补充材料。',
finding='扫描中Δ(Te+Ti)约0.15 mi VA²，分配随上游电子温度变化，部分Te/Ti=9算例电子增温更大；电子压力相关大尺度平行电势减慢离子入流束，ΔTi≈(mi v0²−2eΔφn)/3改进原冷束拾取标度。电势也约束电子、支持多次Fermi增能。',
limitation='图4使用模拟测得电势，不是无输入闭合预测。Δφn仅密度梯度项，不是整条轨道总电势；完整电子温升模型未导出。简单慢激波总温升0.25W与扫描0.15W不同。对称2D/质量比有限，未证明熵增或普适导场/三维比例。SI Table S1、Texts S1–S4、Figs S1–S3访问403，未核读。',
assessment='提供电子约束反作用于离子分配的条件性机制；温升标度不是15%不可逆加热效率。正文W的一个写法量纲不一致，报告统一采用W=mi VA²=Brec²/(μ0 n)。电势能守恒只用于移动场线参考系、冷束与正vb²适用域。'),
dict(key='Dahlin2014Mechanisms',title='The mechanisms of electron heating and acceleration during magnetic reconnection',authors=['J. T. Dahlin','J. F. Drake','M. Swisdak'],year=2014,journal='Physics of Plasmas',doi='10.1063/1.4894484',arxiv='1406.0831',pages=19,
version='arXiv:1406.0831v2作者稿，19页；期刊2014，PDF内部Dated 2018不作为发表年',
pages_read='PDF 1–19全部：正文1–5，参考文献6，图页7–19；无文内附录。',
figures_checked='图1–13全部直接查看（PDF 7–19）；图5/6渠道预算，图7/8空间分布及色标，图9–11积分/岛合并，图12/13尾部与磁矩。正文个别图号/时刻描述与图注不一致，采用图注并保留定位。',
model='二维P3D全PIC；磁化电子导引中心能量分解，非独立流体闭合',
parameters='双Harris、周期204.8×102.4 di，强导场另819.2×409.6 di；Bg/B0=0.2、1；质量比25，c/cA=15，背景密度0.2n0，Ti=Te=0.25mi cA²，半宽0.25di，网格de/4。本文未明确找到时间步和每格粒子数，不补造。',
finding='弱导场0.2时Fermi/曲率项主导电子增能；导场1时平行电场和Fermi可相比，betatron净贡献较小且可冷却。高能尾主要平行；强局地Eparallel不保证大的空间积分净增能。',
limitation='导引中心分解要求电子磁化；早期小岛/合并尖锐结构中与真实增能有差异。局地渠道和参考系相关，积分正负抵消。仅二维、低质量比，未建立电子/离子比例或不可逆熵增；垂直散射机制仍未确定。',
assessment='导场改变渠道权重，不能以固定单项作为全参数电子热源。Fermi、betatron、Eparallel是粒子能量账的分解，与流体J·E不可重复相加；单粒子总能量不是热核心温度。'),
dict(key='Dahlin2015ThreeD',title='Electron acceleration in three-dimensional magnetic reconnection with a guide field',authors=['J. T. Dahlin','J. F. Drake','M. Swisdak'],year=2015,journal='Physics of Plasmas',doi='10.1063/1.4933212',arxiv='1503.02218',pages=13,
version='arXiv:1503.02218v5作者稿，13页；独立补充视频/图未取得',
pages_read='PDF 1–13全部：正文1–8，图1–4在8–11，参考文献9–13；无文内附录。',
figures_checked='图1–4（PDF 8–11）全部直接查看；图2必须同时读能谱与释放磁能，图4最强750粒子的选择不能代表全部电子。',
model='三维/二维P3D全PIC，对比含导场的电子轨道输运与非热尾；不是十矩或Hall加热结果',
parameters='无力场双电流片，渐近Bg=B0，主域51.2×25.6×25.6 di；另较大域102.4×51.2×25.6及质量比100小域；主质量比25，dx=de/4，dt=0.01/Ωci=0.25/Ωce，w=1.25de；3D至少50粒子/格/物种，2D 1600；噪声触发。初始仅压力平衡非精确动理学平衡。',
finding='t=50/Ωci时2D释放磁能约多15%，但3D超过0.5me c²的电子占比约2×10^-4，相对2D约2×10^-5高一个量级。三维随机磁场使电子脱离二维岛芯限制，接触更多加速区；高能Fermi更强、低能Eparallel较重要。',
limitation='没有稳健幂律；周期边界不允许实际逃逸，系统尺寸、质量比和c/cAe=3有限。电子仍各向异性，强导场未触发firehose。补充视频/各向异性图未取得。方法段Te=Ti=0.25mi cA²与后文Te0=mi cA²/8不一致，不给出唯一无疑义初温。',
assessment='十倍指特定阈值以上的粒子数份额，不是总电子热量十倍。图4典型轨道及最强750粒子存在选择范围；支持输运/驻留效应，尚未给出开边界通用逃逸闭合或离子电子熵产比例。'),
dict(key='F627',title='The Enhancement of Ion Heating in Kinetic, Antiparallel Reconnection in the Presence of a Flow Shear',authors=['Colby C. Haggerty','Derek Sikorski','Michael A. Shay','Tai D. Phan','Paul A. Cassak','Giulia Murtas','Prayash S. Pyakurel'],year=2025,journal='The Astrophysical Journal',doi='10.3847/1538-4357/ae2014',arxiv='2508.09424',pages=14,
version='arXiv:2508.09424v1，14页；已登记2025-12-12期刊身份，但未逐页核读正式版',
pages_read='PDF 1–14全部：正文1–13、参考文献13–14；无文内附录。',
figures_checked='图1–6全部直接查看（PDF 4、5、7、9、10、12）；式(2)动量预算、图3温度分量与误差定义、图5/6理论扫描适用域。',
model='2.5D反平行P3D PIC + 出流参考系离子束选择/混合解析；非Hall MHD结果',
parameters='零导场、双周期81.92×40.96di，dx=di/50，dt=1/(200Ωci)，500粒子/格，mi/me=25，c/VA=7，βi=0.1，Te=Ti=0.05mi VA²，w=di/2；6组Vs/VA=0、0.2、0.4、0.6、0.8、1，末组实际上游剪切会衰减；非严格Harris平衡，稳态且岛未撞边时统计。',
finding='扫描中离子ΔTixx约0.11→0.35mi VA²、Vo约0.62→0.17VA；流能转入离子随机运动、热压反作用使出流减速。等效模型取nout≈1.6nup、ε≈1，有(nout/nup)(Vo²+2ΔTixx/mi)≈εVA²。',
limitation='约3.2倍是Txx增量而非标量温度/熵产；电子加热变化小仅文字陈述未展示图。平均边界人工选择，误差为区间标准差；散射/各向同性化过程尚未完整量化。只验证βi=0.1，其他β理论分支未验证。约0.88归一焓流分母未含上游流能，不是88%磁能不可逆转热。',
assessment='不能把较慢喷流直接判作无重联，也不能凭高温判重联。联系PSP弱喷流是待验证解释，不是本篇新的观测检验。需独立记上游流能、压力反馈、电子通道及3D/导场/质量比收敛；正式版未核读。')
]
c=read(P/'research/catalog.json'); v=read(P/'research/reading_notes/verified.json'); by={r['key']:r for r in c}
records=[]
for r in rows:
    k=r['key']; pdf=P/'papers'/f'{k}.pdf'; sha=hashlib.sha256(pdf.read_bytes()).hexdigest()
    url='https://arxiv.org/pdf/'+r['arxiv']
    note={a:r[a] for a in ['key','pages_read','figures_checked','model','parameters','finding','limitation','assessment']}
    note.update(date='2026-11-13',version=r['version'],status='全文及关键图表已核读',source=url,doi=r['doi'],sha256=sha,independent_reproduction='未运行作者代码、原始数据或重算粒子轨道；未取得的独立补充不算已读')
    note_path=f'specific problems/离子加热问题/reading_notes/{k}_note.json';write(P/note_path,note)
    v[k]={a:note[a] for a in ['pages_read','figures_checked','model','parameters','finding','limitation','assessment','status']}
    if k not in by:
        by[k]={a:r[a] for a in ['key','title','authors','year','journal','doi','arxiv','pages']};c.append(by[k])
        by[k].update(id=k,source='2026-11-13新增电子离子加热问题的定向检索',urls=[url],landing_urls=['https://doi.org/'+r['doi'],'https://arxiv.org/abs/'+r['arxiv']])
    by[k].update(read_status=note['status'],scope=r['model'],selection='问题驱动全文核读；动理学参照，不混作Hall闭合成果',download_status='匹配全文与关键PDF页面已人工核验',local_pdf=f'papers/{k}.pdf',pages=r['pages'],sha256=sha,heating_review_record=note_path,heating_review_version=r['version'])
    records.append(dict(key=k,new_full_read=True,pages=r['pages'],version=r['version'],local_pdf=f'papers/{k}.pdf',note=note_path,doi=r['doi'],sha256=sha))
write(P/'research/catalog.json',c);write(P/'research/reading_notes/verified.json',v)
write(T/'questions_manifest.json',dict(date='2026-11-13',baseline_commit='2863996f0e82335a14d593299c11520e3a90d5d6',baseline_full_reads=140,new_full_reads=4,current_full_reads=len(v),new_full_read_main_version_pages=69,new_pdf_files=['papers/Haggerty2015Partition.pdf','papers/Dahlin2014Mechanisms.pdf','papers/Dahlin2015ThreeD.pdf'],records=records,scope='四篇主版本全部核读，69个物理页含参考文献及独立大图；独立补充材料未计入。复用的旧文笔记不重复计数。'))
write(Q/'search_record.json',dict(date='2026-11-13',method='问题驱动网络检索、DOI/出版社书目与arXiv全文核对；不是系统综述或穷尽引用图',query_topics=['electron ion heating partition reconnection parallel potential Haggerty','Dahlin mechanisms electron heating acceleration guide field','three dimensional electron acceleration magnetic reconnection Dahlin','flow shear ion heating Haggerty Sikorski 2025','2026 ion acoustic instability reconnection heating','2026 non Maxwellian ion populations reconnection magnetopause'],query_note='保留检索主题摘要，不伪称逐字完整请求日志',accepted=[dict(key=r['key'],doi=r['doi'],source='https://arxiv.org/pdf/'+r['arxiv']) for r in rows],pending=[dict(title='Role of ion acoustic instability in magnetic reconnection',doi='10.1017/S002237782510113X',status='2026题名/检索摘要候选，未全文核读，不支持报告科学结论'),dict(title="Quantifying Non-Maxwellian Properties of Ion Populations During Reconnection at Earth's Magnetopause",doi='10.1029/2026GL122882',status='2026题名候选，未全文核读，不支持报告科学结论'),dict(title='Electron heating during magnetic reconnection: A simulation scaling study',doi='10.1063/1.4904203',source='https://www.physics.udel.edu/~shay/papers/ShayM.2014.PhPl.21.122902.pdf',status='前序参数扫描候选，未全文核读')],access_limits=[dict(key='Haggerty2015Partition',url='https://agupubs.onlinelibrary.wiley.com/doi/suppl/10.1002/2015GL065961/supinfo/grl53700-sup-0001-supinfo.pdf',result='HTTP 403；未取得SI，不绕过访问限制'),dict(key='Dahlin2015ThreeD',result='独立补充视频/图未取得')],download_note='前两篇首次60秒超时，续传后成功；三份新PDF可完整解析且图页人工查看；F627使用原库PDF，不新增下载计数'))
print('Recorded',len(records),'new full reads;',len(v),'total')
