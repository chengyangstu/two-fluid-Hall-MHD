# 离子与电子加热：Hall MHD／双流体能研究到哪一步

更新：2026-11-12。起点是《已解决与未解决的问题》原第1.4.5节的截图。

**可以研究，但要有独立物种能量或压力方程及合适闭合。** 双温 Hall MHD 和十矩模型已经计算了局地离子／电子温度、流能与内能预算，并与部分实验、空间观测比较。Hall 项本身不提供热化闭合，也不决定一个普适加热比例。

- [完整专题 PDF](report.pdf)：24页，包含定义与推导、模型能力比较、研究脉络、实验预算、已解决／未解决问题和研究设计。
- [可维护 TeX 源](report.tex)、[专题书目](references.bib)。
- [证据矩阵](evidence_matrix.csv)：26篇正文引用的已核读文献，记录模型身份、结论边界、版本与原文位置。
- [候选与引文追踪表](candidate_screening.csv)：397条合并记录；自动题名提示、定向追踪和全文状态分开，未读候选不作科学结论。
- [本轮计数与版本清单](batch_manifest.json)、[全仓库索引](../../paper_index.html)、[仓库主页](https://github.com/chengyangstu/two-fluid-Hall-MHD)。

## 最重要的研究结论

1. **直接流体进展确实存在。** Browning等（L223）给出MAST双温Hall的下游离子热点和不同电子热结构；Kaptanoglu2020给出HIT-SI三维双温Hall的温度及热预算；TenBarge2019MMS给出十矩两物种流能／热能。它们支持指定闭合下的条件性预测，尚未共同建立无参数、跨环境的不可逆加热定律。
2. **“加热比”必须先定义。** F674正式版图7的MRX离子／电子电场沉积功率约为0.71／0.35 MW，即约2:1；同图热能变化为0.27／0.26 MW，接近1:1，且含储存和边界焓流。它们都不能直接写成局地不可逆熵产比。非对称MRX的物种沉积更接近。
3. **实验支持部分空间机制。** MRX支持电势加速和下游升温的分离，有／无离子碰撞PIC对照显示多束展宽与Maxwell化不同。MAST观测到窄电子热点、下游离子热点与物种交换时间；它直接联系双温流体结果，但尚未唯一确认局地黏性／激波机制。
4. **模型身份不能混算。** Yoon2018是EMHD场加测试离子，后继2019／2023为PIC；E512是流体—动理学，Numata2015为双物种陀螺动理学；Finelli2021为动理学离子加流体电子。Che2014虽有“双流体”题名，实际PIC中未发生重联；TS6会议稿未展示独立Hall加热结果。
5. **未解决原因并不只有一种。** 有的是方程不含所需自由度，有的是热流／压力／耗散闭合未验证，还有数值残差、边界损失、驻留时间、仪器平均及未做相应研究。把温度相近、重联率相近或Hall四极图像当成整个热化模型获证，会高估证据。

## 截图对应的三篇原文

基线位置：`分卷/03_solved_open.pdf`物理第7页、印刷第4页；维护源为[`sections/08_solved_open.tex`](../../sections/08_solved_open.tex)。修订后保留同名小节，并增加本轮进展。

| 键 | 原文 | 本地版本与关键位置 |
|---|---|---|
| Yoo2013 | Yoo等，2013，*Observation of Ion Acceleration and Heating during Collisionless Magnetic Reconnection in a Laboratory Plasma* | [5页PDF](../../papers/Yoo2013.pdf)，图2–4；[DOI](https://doi.org/10.1103/PhysRevLett.110.215007) |
| L272 | Yoon与Bellan，2021，*How Hall electric fields intrinsically chaotize and heat ions during collisionless magnetic reconnection* | [正式版10页，含封面](../../papers/L272_published.pdf)，图1–7；[DOI](https://doi.org/10.1063/5.0040374) |
| E512 | Zocco与Schekochihin，2011，*Reduced fluid-kinetic equations for low-frequency dynamics, magnetic reconnection, and electron heating in low-beta plasmas* | [28页PDF](../../papers/E512.pdf)，式76–84、附录A/B；[DOI](https://doi.org/10.1063/1.3628639) |

## 全文核读与笔记

本轮新增17篇所记录版本的全文核读，主版本共300个PDF物理页。三分支另完整重读Yoo2013、L272、E512、L244共70页，主代理重读已核读F635共10页；合计22篇本轮全文阅读、380个物理页。页数含封面、参考文献及接收稿重复大图，不代表独立科学正文页数。原库其余已读文献只复用明确记录的档案，未声称全部重新通读。

| 阅读分支 | 新增全文核读 | 笔记与详细记录 |
|---|---|---|
| 直接Hall／两温输运 | L223、L164、Kaptanoglu2020、L247、TS6FEC2025 | [中文综述](reading_notes/hall_fluid_review.md)、[逐篇JSON](reading_notes/hall_fluid_records.json) |
| 实验与离子轨道链 | F679、F674、Yoo2017Heating、Yoon2018Heating、F743、Yoon2023PhaseSpace、Tanabe2015MAST | [中文综述](reading_notes/experiment_review.md)、[逐篇JSON](reading_notes/experiment_records.json) |
| 电子热化与闭合 | Loureiro2013Heating、Numata2015Heating、Finelli2021、Che2014Buneman、TenBarge2019MMS | [中文综述](reading_notes/closure_review.md)、[逐篇JSON](reading_notes/closure_records.json) |
| 原库电子多群十矩复查 | F635，不增计 | [复核笔记](reading_notes/F635_note.json) |

新增15个原文PDF，包含F674正式版及Kaptanoglu的两个版本；版本不重复计数。后者主读35页接收稿，较早21页稿只读1–11页，不算第二次全文。全库全文核读由122增至139篇；其中包括实验、PIC、混合、GK和会议稿，不能说成139次Hall模拟。

## 检索覆盖与实际限制

三个种子的OpenAlex一跳追引得到379条有向关系、363个去重节点。宽检索合并16020个元数据命中，含大量不相关工程传热结果，未全部人工筛完。第三个宽检索取得3800／15993条后遇HTTP 429，随后七式也受限；不是这些方向零命中。原始元数据压缩归档，保留检索式、日期、分页状态和引文边。

- [总检索日志](search/openalex_search.json)、[有向引用边](search/citation_edges.json)、[原始元数据归档](search/openalex_works.json.gz)、[分流说明](search/screening_summary.json)。
- 元数据返回的3处临时签名URL已移除认证查询参数，DOI和来源入口保留；[发布清理记录](search/publication_cleanup.json)记录字段、原URL哈希及归档前后哈希，未静默改写书目信息。
- 定向补充：[Hall分支](search/hall_fluid_search.json)、[实验分支](search/experiment_search.json)、[闭合分支](search/closure_search.json)。
- 优先缺口：Drake2009离子拾取加热、L046的2003年EMHD电子加热、Stanier学位论文及若干闭合前序；取得或核读未完成，不据摘要升级证据。
- Kaptanoglu2020的[勘误](https://doi.org/10.1063/5.0032632)正文未取得；TenBarge2019正式PDF受限，所读作者版与正式网页补查分别记录。不能说已经逐页核验所有正式版本。
- 未运行作者代码或复算原始数据，未取得的独立补充与前序方法逐篇保留缺口。本专题不声称穷尽全球文献。

## 重建与复核

在仓库根目录执行（Windows建议启用Python UTF-8模式）：

```text
python -X utf8 scripts/check_ion_heating_algebra.py
python -X utf8 scripts/build_ion_heating_report.py
python -X utf8 scripts/audit_ion_heating_report.py
```

后两步需要XeLaTeX、BibTeX、PyMuPDF和Pillow；代数核验需SymPy。`build_heating_screening.py`从现有检索归档重建候选表，不联网。`search_ion_heating.py`是可选重检脚本，可能触发数据库限流；`ingest_ion_heating.py`是明确批次导入，不是日常构建入口。

全局维护源、三卷和合订本也已同步。选定代数核验只检查Hall功、摩擦能量回收、十矩松弛迹及两束中心矩，不等于证明全部方程或验证物理闭合。渲染图片属于可再生检查缓存，不提交。
