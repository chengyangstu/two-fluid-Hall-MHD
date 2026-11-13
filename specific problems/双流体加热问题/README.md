# 双流体与流体闭合的离子、电子加热专题

调研更新：2026-11-14。本专题独立于[原加热报告](../离子加热问题/README.md)，以流体模型为主线，比较新增方程能带来什么结论、实验验证到哪一步，以及对不同 Hall MHD 基线的支持、修正与限制。

直接阅读：[42页专题 PDF](report.pdf)。可维护入口：[TeX 主文件](report.tex)、[书目](references.bib)、[21 篇证据矩阵](evidence_matrix.csv)、[逐篇核读笔记](reading_notes/records.json)。保持整个仓库的目录结构，PDF 内的原文链接才能找到 `../../papers/`。

## 主要判断

- 独立物种能量方程能给出温差、交换滞后及不同输运路径；完整压力张量进一步增加非对角压力、各向异性和应变功。优势要归因到新增方程，不能只归因于“双流体”名称。
- 热通量闭合会改变离子层、岛合并、温度结构和三维不稳定性。更多模态不一定意味着更多离子内能；Bradshaw 等的梯度闭合算例中，离子压力能和流能变化反而较局地闭合小。
- MAST、HIT-SI 提供温图与趋势约束；MRX 约束分物种电功和有限控制体能量预算；MMS 能检验电子各向异性闭合。当前证据没有给出跨装置、无调参的双物种不可逆加热比例。
- 两篇新增 MMS 研究既支持俘获电子状态方程的部分预测，也暴露上游来源拟合、局地俘获历史和垂直增温的遗漏。其数值证据包含混合模型，不能归作完整双流体离子加热验证。

## 内容与阅读顺序

1. 明确 H0–H4 比较基线：等温、单热力学、双温、电子惯性及张量压力模型。
2. 从物种连续性、动量、能量和 Maxwell 方程推到 Hall 约化；区分电功、流能、内能、温升、焓流、非热成分与不可逆热化。
3. 按问题串联共速双温激波、双温 Hall、五矩/十矩、非局地与梯度热流、各向异性 EoS、Landau/陀螺流体和电子来源分群。
4. 分装置检查诊断量、参数、匹配方式、不确定度及尚未解释的差异。
5. 给出按新增方程消融、统一能量账本、留出观测验证的研究设计。5%/1%数值门槛是本报告建议，不是已完成实验或文献结果。

附录逐篇列模型、参数、初边值与实现、发现、图式位置、局限以及对 Hall 比较的意义。

## 阅读计数、原文与实际缺口

本专题采用 **21 篇**已核读证据：19 篇复用旧记录，新增 **Wetherton2019、Wetherton2021 两篇**，主版本共43个物理PDF页（含封面、参考文献与重复图页）。全库由144增至146篇；本轮新增完整流体模拟论文为0篇。旧文定向图式复查不重复计数。

新增原文为 OSTI 的公开接收稿：[2019 年原文](../../papers/Wetherton2019.pdf)、[2021 年原文](../../papers/Wetherton2021.pdf)。身份、页数和哈希见[批次清单](batch_manifest.json)；来源入口分别为 [OSTI 1558071](https://www.osti.gov/servlets/purl/1558071) 与 [OSTI 1760625](https://www.osti.gov/servlets/purl/1760625)。正文、方法、结果、讨论、全部图表及参考文献均核读；两篇无文内附录。

Ohia2012 的 MIT PDF 入口返回429，Ohia2015 的出版PDF入口返回403，未完成正文与图式核验，不据摘要写入科学结论。Kaptanoglu2020 勘误、TenBarge2019MMS 正式PDF及十三/二十矩完整加热研究链仍有证据缺口。未重分析原始MMS数据，未运行或复现文献中的大规模等离子体模拟。

本轮为定向检索与追引，没有穷尽数据库或递归引文。记录见[检索式与边界](search/search_record.json)、[候选筛选](search/candidate_screening.csv)、[下载请求](search/download_requests.json)及[访问结果](search/download_attempts.json)。论文版权与许可按原文及来源页面处理。

## 构建与核验

在仓库根目录运行：

```sh
python3 scripts/build_twofluid_heating.py
python3 scripts/audit_twofluid_heating.py
```

构建需要 XeLaTeX、BibTeX、latexmk 和现有 ctex/Fandol 排版环境；审计需要 PyMuPDF、Pillow。脚本从本目录笔记与全库 catalog 生成附录、书目和矩阵，正文各章保留手工维护；不要直接修改生成的附录。

报告已做引文、原文路径、内部链接、缺字和页面边界检查；渲染与直接视觉检查另记录在 [visual_review.json](../../research/twofluid_heating/visual_review.json)。[topic_audit.json](../../research/twofluid_heating/topic_audit.json)保存最终页数与哈希，[algebra_check.json](../../research/twofluid_heating/algebra_check.json)保存选定代数核验；这些不代表全方程形式证明或模拟复现。
