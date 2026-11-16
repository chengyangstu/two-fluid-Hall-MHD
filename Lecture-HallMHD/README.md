# 双流体与 Hall MHD 入门讲义

[打开 PDF](main.pdf) · [主 TeX](main.tex) · [参考文献](references.bib) · [撕裂模伴随讲义](../Lecture-TM/README.md)

面向只修过等离子体导论的读者，从每个变量和算符的含义出发，逐项推导矩方程、Hall 约化和磁重联。所有量级分析都实际代入数字；附 8 张原创解析/示意图，11 道完整解答。

当前成稿：**57 页、8 张原创图、12 条实际引用书目**（2026-11-16）。

## 阅读路线

| 章节 | 学习内容 |
|---|---|
| 1 | 粒子、分布函数、流体三个层次；磁通函数与 Harris 平衡 |
| 2 | 从动力学方程逐次取矩；连续性、动量、压力张量、热能与总能量 |
| 3 | 分别列全电子与离子方程；五矩/十矩、Maxwell 演化及约束 |
| 4 | 低频、准中性、精确质心变换；广义欧姆定律和双温 Hall 模型 |
| 5 | 移动回路磁通、电子冻结、X 点、广义磁通、能量与物种加热 |
| 6 | 标量、十矩、CGL、热流及俘获电子闭合的来源与局限 |
| 7 | 四组教学等离子体；逐项计算惯性长度、回旋半径、碰撞、β 和欧姆项 |
| 8 | Sweet–Parker 推导与自洽性；Hall 层、电子层、四极场及磁通率 |
| 9 | 从线性方程推导两支 Hall 波色散关系，计算实际频率 |
| 10 | 方程到程序、归一化、时间步、收敛；GEM 基准与 MRX 实验 |
| 11 | 共 11 道完整解答与学习检查 |

先读 1、7、8 章建立图像，再逐项学习 2–6 章，最后用 9–11 章检验理解。四组 SI 输入分别代表高密度、实验室、磁层和日冕量级，均为明示的教学参数，不对应指定事件。大尺度与薄层分别进行排序；不能把表中的经典 SP 厚度自动当成可信物理预测。

## 数据与来源

- `scripts/build_figures.py` 同时重建 8 张矢量图、参数表及 `research/calculations.json`，并运行 7 项数值恒等式核验。
- `research/foundations_sources.json` 保存矩方程及闭合的来源和 7 项选定代数检查。
- `research/teaching_sources.json` 记录量级公式、GEM 与 MRX 的来源及本次核查边界。
- 文献是模型和观测的出处；原创教学图不冒充实验数据，未声称复现大型重联模拟。

这次整理不改动原库 146 篇全文核读计数。图中英文标记均在中文正文或图注解释。电子电荷写为 −e，电阻率 η 的单位为 Ω·m，磁扩散系数为 Dη=η/μ0。

## 重建与核验

TeX 编译需要 XeLaTeX、latexmk、BibTeX、ctex 和 Fandol 字体。源文件、书目与矢量图已齐全，只重编 PDF 不需要 Python。

```sh
cd Lecture-HallMHD
latexmk -xelatex -interaction=nonstopmode -halt-on-error main.tex
```

重新生成图和算例需要 Python 3、NumPy、Matplotlib；审计需要 PyMuPDF、Pillow，理论核验另需 SymPy、mpmath。依赖列在 `requirements.txt`。从项目根目录运行：

```sh
python3 Lecture-HallMHD/scripts/build_figures.py
latexmk -xelatex -interaction=nonstopmode -halt-on-error -cd Lecture-HallMHD/main.tex
python3 scripts/audit_lectures.py Lecture-HallMHD --render
```

`research/pdf_audit.json` 记录最终页数、PDF 哈希、引文/图片/标签检查；`research/editorial_review.json` 记录人工式版面与物理复核。审计程序优先尝试 Poppler；若其本地 CJK 映射不可用，则记录原因并使用 PyMuPDF 渲染。源码中的数学和中文文字均可在 PDF 中检索。渲染缓存不入库。
