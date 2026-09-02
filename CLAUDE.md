# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 项目性质

哈工大（哈尔滨校区）**硕士学位开题报告**，基于 hithesis v3.1e 的开题/中期报告类。题目为「面向PCBA上下料的轮式双臂模仿学习策略鲁棒性改进研究」：轮式双臂机器人（腰 4 + 双臂各 7 + 头 2 DoF）经激光雷达导航在五个工位间停靠，由 VR 遥操作示范微调的 \(\pi_{0.5}\)（OpenPI 部署，ACT 作对照）执行上下料。研究沿「停车误差 → 精细阶段放大 → 错误动作持续」的误差传递链设三层防线：事前（停车残差进状态 + ±3 cm 随机停车数据）、事中（分阶段动作块执行）、事后（时序集成不一致度失败检测 + 模板恢复），按「基线 / +一 / +一二 / +一二三」四配置叠加验证。

这是一个**写作仓库**，不是软件项目：产物是 `report.pdf`，`scripts/` 只是插图生成工具。

## 构建

```bash
latexmk                 # 编译 report.tex → report.pdf（latexmkrc 已指定默认文件）
latexmk -c report.tex   # 清理中间文件，保留 PDF
latexmk -C report.tex   # 连同 PDF 一并清理
```

必须从仓库根目录运行。`latexmkrc` 把 `$pdflatex` 覆写为 `xelatex --shell-escape -synctex=1`，走 xelatex → `.xdv` → xdvipdfmx 的路径；**引擎必须是 XeLaTeX**，`hithesisart.cls:156` 对非 XeTeX 引擎直接 `\ClassError`。参考文献走 **BibTeX + `hithesis.bst`**（`$bibtex_use = 2`），不是 biber——仓库里没有 biblatex 也没有 `.bcf`。

没有 Makefile、没有 CI、没有自动化测试。验证方式是：`latexmk` 无 error 且无 undefined reference、`grep Overfull report.log` 为空，然后 `pdftoppm -png -r 80 report.pdf tmp/pdfs/<批次>/page` 渲染，目视检查改动页的浮动体位置、TikZ 标注重叠、截断和引用编号。

`report.blg` 里大量 `Warning--Require citedate` 是 bib 条目缺 `citedate` 字段所致，属已知噪声，不影响出 PDF。`hithesis.bst` **没有 `misc` 函数**，arXiv 预印本一律写成 `@techreport`（`institution`、`number={arXiv:...}`、`url`），照 `black2024pi0` 的格式。

### 插图脚本

```bash
/home/njx-10096304/miniconda3/envs/scripts/bin/python scripts/visualize_right_hand.py <episode.hdf5>
```

**默认 `python3`（miniconda base）没有 h5py**，只有 `envs/scripts` 这个环境满足 `h5py` + `numpy` + `Pillow`。`--output-dir` 默认值 `figures/right_hand_visualization` 是相对路径，必须在根目录运行。脚本会重写该目录下的 `README.md`（记录数据源、帧数、轨迹长度、夹爪切换帧），**那份 README 是自动生成的，不要手工编辑**。

## 文档架构

### 规划文档 → 正文的映射

根目录 md 各有分工，不要混用：

- `description.md`——**研究内容的单一事实来源**：场景、误差传递链、三个改进点的做法与消融设计、四配置验证、设备条件。改正文前先看它；正文与它冲突时以它为准。
- `outline.md`——**旧课题（示教先验 + 强化学习）的大纲遗留**，首行已标注「已被 description.md 取代」。其中的文献池部分仍可查，研究内容部分不要再参考。
- `研究内容与代码边界.md`——旧课题的范围文档。平台构型、VR 映射、示范采集与两条流水线的描述仍然成立（对应正文第 5 节）；涉及强化学习、残差策略的段落已作废。
- `章节设计.md`——旧课题的学位论文六章规划，**已删除**。
- `README.md`——模板填写与编译说明，与研究内容无关。

`reference_papers/`（untracked，约 250 MB）是新课题的文献库：按六个主题目录存放 34 篇论文的 PDF 与中文笔记，根下的 `references.bib` 是 Zotero 导出的合集，`manifest.csv` 列出全部条目。`reference.bib` 里的新课题条目都是从那里复制并清洗（删 `annote/keywords/file/abstract`、去标题保护括号、`@misc`→`@techreport`）而来。笔记里「按阶段自适应 chunk」之类的建议是笔记作者的推断，不是论文原文观点，正文里不要写成文献主张。

`reference/硕士开题报告-王旭.{docx,md}` 是**他人的样例开题报告**（无人机方向），仅作栏目顺序参考，非本课题内容。

### TeX 文件组织

`report.tex` 是入口，只有两个 `\input`：`front/cover` 和 `body/proposal`，无 `\include`。

- `front/cover.tex` 仅做 `\hitsetup{...}` 键值赋值，不产生排版输出；封面由随后的 `\makecover` 绘制。该文件内**不能出现空行**（文件第 4 行有此硬性注释）。题目已填，学院、学科、姓名、学号、导师仍是「请填写…」占位。
- `body/proposal.tex`（约 780 行）是唯一正文文件。基类是 **ctexart**，所以顶层是 `\section` 而非 `\chapter`，层级为 `\section` → `\subsection` → `\paragraph`。
- 九个 `\section` 对应学院规定的开题报告栏目，顺序固定，现已全部写满。第 3 节「主要内容及方案」七个小节是核心（3.2 任务定义、3.3–3.5 三个改进点、3.6 整体验证）；第 5 节「已完成」只写两条流水线与平台，**不把三个改进点写成已完成**。
- 跨节引用用 `sec:completed`（第 5 节）、`sec:risks`（第 8 节）、`subsec:task-definition`、`subsec:improvement-one/two/three`。

### 学位/校区/阶段由 documentclass 选项决定

```latex
\documentclass[fontset=fandol,toc=true,type=master,stage=opening,campus=harbin]{hithesisart}
```

`type`（bachelor/master/doctor）和 `stage`（opening/midterm）**缺失即 `\ClassError`**；`campus` 为 harbin/shenzhen/weihai。`hithesisart.cfg` 里有针对「harbin + master + opening」的特例分支——学院栏标题变为「学院（部）」、学科栏变为「学科/专业学位类别」、`\hit@cthesisname` 取「学位」而非「学位论文」。改动这三个选项会静默改变封面字段名，不只是换个字。

`bibmaxauthor` 默认 3（作者超 3 人显示「等/et al」），`report.tex` 未覆盖。

### 模板定制只在 report.tex，不在 cls/cfg

`hithesisart.cls`、`hithesisart.cfg`、`hithesis.bst` 自 init commit 起**零改动**，是 upstream 原样文件——除非模板本身必须改，否则不要动它们。本仓库真正的定制全在 `report.tex:12-30`：四级标题（「项」）按学校规范配置为全角括号编号 `（1）`、缩进 2 字宽、标题后接排（`runin=true`），并用 `\@addtoreset{paragraph}{subsection}` 让编号在每个 subsection 内重置。

## 写作约定

以下约定来自正文既有代码，新增内容必须沿用。

### 引用

natbib 已配置为**上标数字**（`hithesisart.cls:661` 的 `\bibpunct` 第 4 参数为 `s`）。**正文只写 `\cite{}`，不要手写 `\upcite` 或上标**——全文 68 处 `\cite`，`\upcite` 出现 0 次。多篇合并写进一个 `\cite`：

```latex
\cite{fu2024mobilealoha,honerkamp2023n2m2,yang2023momaforce}
```

需要行内方括号引用时用 cls 提供的 `\inlinecite` / `\onlinecite`。BibTeX key 为小写「作者姓+年份+短标签」：`zhao2023act`、`black2025pi05`、`xu2025faildetect`。`reference.bib` 中未被引用的旧课题条目（PPO、残差 RL 等）保留不删，不引用即不出现。

### 编号与交叉引用

`hithesisart.cls:288-290` 把图/表/公式编号重定义为 `节号-序号` 格式，但在当前 harbin/master/opening 配置下实际渲染为全文连续编号（`图 5`、`式 (6)`），这是模板行为，不要在正文里改。引用公式用 **`式\eqref{...}`**（前面带「式」字）：

```latex
式\eqref{eq:station-frame-residual}和式\eqref{eq:residual-planar}……
```

label 前缀 `fig:` / `tab:` / `eq:` + 小写 kebab-case。

### 数学与记号

行内数学一律用 `\(...\)`，**不用 `$...$`**。标题中出现数学必须包 `\texorpdfstring`：

```latex
\subsection{ACT对照基线与基于OpenPI的\texorpdfstring{\(\pi_{0.5}\)}{pi0.5}推理闭环}
```

公式后的变量解释固定以「式中，」或「其中，」开头。过宽的公式用 `equation` 内套 `aligned` 拆成两行（`eq:residual-augmented-state`、`eq:temporal-ensemble` 即如此处理），不要靠缩小字号。

全文共用一套记号，新增公式必须沿用：`\mathbf x_t` 本体状态（14 维），`\tilde{\mathbf x}_t` 拼入归一化停车残差后的状态（17 维），`\mathbf o_t`/`\tilde{\mathbf o}_t` 观测，`\widehat{\mathbf A}_t` 长度 `H` 的动作块，`h` 实际执行步数，`\boldsymbol\delta_k=(\delta x_k,\delta y_k,\delta\theta_k)` 第 `k` 工位停车残差，`\{S_k\}` 名义工位系、`\{B\}` 基座系，`\phi_t\in\{\mathrm{fine},\mathrm{free}\}` 阶段，`\mathcal C_t` 覆盖时刻 `t` 的重叠块集合，`s_t`/`\tilde s_t` 不一致度及其滑窗均值，`\eta_\phi` 分阶段阈值，`\ell_t\in\mathcal L` 子任务指令。

### 图表

- **TikZ 图是裸片段**（`\begin{tikzpicture}` 开头，无 `\documentclass`），用 `\input{figures/xxx}` 内联，**带 `figures/` 前缀**；所需的 `\usepackage{tikz}` 和 `\usetikzlibrary` 由 `report.tex:8-9` 统一提供，**只有 `arrows.meta,positioning,fit,calc` 四个库**，图文件脱离主文档无法单独编译。七张 TikZ 图沿用同一套样式（`font=\small`，`flow/plant/constraint` 三类圆角节点，`mainarrow/feedback/influence` 三类箭头）。
- **位图/PDF 用 `\includegraphics`，只写文件名不带目录**（靠 `report.tex:10` 的 `\graphicspath{{figures/}}` 解析）。两种路径风格并存，别写混。
- 所有 `figure` 用 `[htbp]`，TikZ 图后常紧跟 `\FloatBarrier`。
- caption 为**单语中文**，无双语、无可选短标题。**引用他人的图时，caption 末尾直接挂 `\cite`**：

```latex
\caption{扩散视觉动作策略的观测条件化与动作序列生成框架\cite{chi2023diffusion}}
\caption{\(\pi_{0.5}\)模型结构及两阶段训练流程\cite{black2025pi05}}
```

- 表格用 `longtable` + `booktabs`（`\toprule/\midrule/\bottomrule` + `\endfirsthead`/`\endhead`，续页头写 `\multicolumn{n}{c}{续表~\thetable}`），正文中没有 `table` 环境。列宽之和保持 13.4 cm（`@{}p{…}…@{}`），否则会溢出版心。

### 引图溯源制度

`figures/README.md` 是引用图的**来源登记册**。正文图题只保留文献编号，原图号、版本与裁剪说明集中记在该文件。新增外部来源的图时必须补一条记录；对图形做翻译、删改或重绘也要补充说明。

### 中文表达

- 术语首现用「中文全称（English Full Name, ABBR）」，后文只用缩写，括号内用半角逗号 + 空格。正文残留 3 处全角逗号（PCBA、VLM、VLA 的首现），新增内容不要沿用。
- 连字破折号用 LaTeX 的 `--`：`Denavit--Hartenberg`、`视觉--语言--动作`。
- `\placeholder{...}` 输出灰色「【填写提示：…】」，标记待填位置，正文现存 1 处（`body/proposal.tex:6` 课题来源）。预期目标一节按用户要求**只写定性目标**，不要补数值或数值占位。

## 仓库卫生（现存问题）

`.gitignore` 只列了 27 个 LaTeX 中间扩展名，缺 Python 与临时目录规则，导致以下已知不一致——改动相关文件时留意：

- **`report.pdf` 是被 git 跟踪的**（`.gitignore` 不含 `*.pdf`，因为 `figures/*.pdf` 是需要跟踪的插图资源）。每次编译都会让它变脏，`latexmk -C` 会删掉一个已跟踪文件。正文改动应连同重新编译的 PDF 一起提交。
- `tmp/` 是排版校对的页面截图，按约定不应提交，但 `tmp/pdfs/fourth-level-headings/` 下已有 12 个文件被跟踪；`tmp/pdfs/restructure/`、`tmp/pdfs/pcba-scene/` 保持 untracked。
- `scripts/__pycache__/*.pyc` 和 LibreOffice 锁文件 `reference/.~lock.*.docx#` 已被误提交。
- `reference_papers/`（34 篇论文的 PDF 与笔记）和 `AGENTS.md` 保持 untracked。

提交信息沿用现有习惯：简短中文短语，无 conventional-commit 前缀（如 `精简正文`、`重构开题为PCBA双臂鲁棒性课题`）。

## 相关文件

仓库根目录另有一份 `AGENTS.md`（untracked），内容为通用仓库指南，与本文件互补。
