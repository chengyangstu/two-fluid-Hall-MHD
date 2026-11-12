# 仓库结构与本轮维护范围

日期：2026-11-12。Git实际根目录经`git rev-parse --show-toplevel`核对为`D:/Hall-MHD-investigate`；远端为`https://github.com/chengyangstu/two-fluid-Hall-MHD.git`。现有说明中`HallMHD_双流体磁重联调研`／父级`Learning_process`是此前存放路径，不据此在父目录初始化仓库。

已先读根README、AGENTS及分卷README，核对初始Git状态为空，再检查main/preamble、章节入口、模型/数值/问题线与截图相关源文、书目/目录/全文记录/待办、近期研究记录及构建审计脚本。目的是理解全仓库组织、证据等级和维护链，不能把文件清点或机器读取称为通读全部324个历史原文PDF。

| 路径 | 理解与本轮处理 |
|---|---|
| main.tex、preamble.tex、sections/ | 合订源是科学正文主要入口；新增结论进入energy研究线和问题小节，保留历史批次日期。中文路径排版补齐等宽中文字体。 |
| 分卷/ | 三卷仍由build_split_reports生成，避免只改生成稿；同时构建以解析跨卷辅助引用。 |
| references.bib、paper_index.* | 由catalog与verified重建；新篇用稳定键，历史版本保留，增加本轮筛选入口。 |
| research/catalog.json、pdf_manifest.json | 元数据、版本、路径、页数与哈希；新增原文继续集中在papers/。 |
| research/reading_notes/verified.json | 只有完整正文/适用附录与关键PDF页面实际核验的17篇升级；旧读档不抹去，仅加复核指针。 |
| research/backlog.json | 从当前状态重建；未读候选不能进入科学结论。 |
| synthesis_continuation、twofluid_equations_revision、split_reports | 理解上一批研究线、推导与分卷来源；旧证据/快照保留，不盲跑固定内容重建脚本。 |
| scripts/ | 审查索引、研究线、分卷、合订审计及危险的历史重建边界；把122固定计数改为动态，修正Windows清单路径。 |
| specific problems/离子加热问题/ | 新独立专题，包含可维护TeX/PDF、读档、追引数据、证据矩阵、候选表、版本与访问缺口。 |

基线为122全文读档、324原文物理PDF、三卷94/162/20页。三条被明确授权的子代理分读流体、闭合与实验，主代理整合、补读F635并独立核对能量定义；另由闭合代理审查新专题方程与结论措辞。没有声称通读全仓库所有候选、运行原论文大规模模拟或复算全部原始数据。
