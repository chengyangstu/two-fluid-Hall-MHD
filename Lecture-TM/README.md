# 撕裂模：理论推导、物理图像与实验

[打开 PDF](main.pdf) · [主 TeX](main.tex) · [参考文献](references.bib) · [Hall MHD 伴随讲义](../Lecture-HallMHD/README.md)

从等离子体导论水平出发，顺着磁岛几何、平衡、线性化、内外层匹配、非线性演化和实验诊断逐步学习。含 8 张原创解析/示意图、理论推导内的完整数例，以及末章 6 组诊断与量级算例。

当前成稿：**43 页、8 张原创图、10 条实际引用书目**（2026-11-16）。

## 阅读路线

| 章节 | 学习内容 |
|---|---|
| 1 | 磁通/流函数、X/O 点、磁岛全宽；从 MHD 推导磁通与涡量方程 |
| 2 | 逐项线性化、共振面、时间排序；Harris 外解与 Δ′ 的解析推导 |
| 3 | 常磁通 FKR 标度及 0.5474367 系数；正弦变换、Bessel 函数、Coppi 大 Δ′ 支、最快模与数值自洽性 |
| 4 | 线性失效、磁面平均、Rutherford 全宽系数 0.8227058、非线性算例、plasmoid 与理想撕裂标度 |
| 5 | 有理面、Mirnov/ECE/软 X 射线诊断、NTM；DIII-D、MRX、OMEGA EP 三类原始实验 |
| 6 | 从扰动场求岛宽；模数与有理面；增长率及误差；Hall/电阻排序；激光分辨率；ECCD 对齐 |

本讲义固定 x 横穿电流片、y 沿片，B⊥=ẑ×∇ψ；磁岛 W 始终指全宽。γ 是磁通扰动增长率，线性阶段岛宽按 exp(γt/2) 增长。先理解每个等号的假设，再比较论文中的系数。

## 实验与证据边界

- DIII-D：局地 ECCD 控制新经典撕裂模，区分直接测量、平衡反演和 CQL3D 推断。
- MRX：碰撞性电子电阻与 Hall 尺度可以同时重要，岛形成与重联率的关系来自事件统计。
- OMEGA EP：质子照相及反演支持快速演化高 β 电流片中的 plasmoid；有限时间/空间分辨率限制增长率测定。

原文版本、页数、图号、实测/推断参数、限制与哈希见 `research/experiment_sources.json`。新取得的两份原文见 `research/source_pdfs/`；第三方论文版权归原作者和出版方。所绘图均为教学图，不使用虚构的实验曲线。原始实验图请按讲义给出的图号回查。

`research/theory_sources.json` 区分经典原始出处、定向核对的作者讲义、已核读记录复用与未取得全文的边界；`research/theory_checks.json` 包含 Harris 外解、FKR 常数、Rutherford 积分和数值例。没有运行完整有限 S 本征求解或复现实验；本次讲义不改变原库 146 篇核读计数。

## 重建与核验

TeX 编译需要 XeLaTeX、latexmk、BibTeX、ctex 和 Fandol 字体。源文件、书目与矢量图已齐全，只重编 PDF 不需要 Python。

```sh
cd Lecture-TM
latexmk -xelatex -interaction=nonstopmode -halt-on-error main.tex
```

重新生成图和算例需要 Python 3、NumPy、Matplotlib；审计需要 PyMuPDF、Pillow，理论核验另需 SymPy、mpmath。依赖列在 `requirements.txt`。从项目根目录运行：

```sh
python3 Lecture-TM/scripts/build_figures.py
python3 Lecture-TM/scripts/verify_theory.py
latexmk -xelatex -interaction=nonstopmode -halt-on-error -cd Lecture-TM/main.tex
python3 scripts/audit_lectures.py Lecture-TM --render
```

`research/pdf_audit.json` 记录最终页数、PDF 哈希、引文/图片/标签检查；`research/editorial_review.json` 记录人工式版面与物理复核。审计程序优先尝试 Poppler；若其本地 CJK 映射不可用，则记录原因并使用 PyMuPDF 渲染。源码中的数学和中文文字均可在 PDF 中检索。渲染缓存不入库。
