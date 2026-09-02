> 状态：本大纲对应旧课题，已被 description.md 取代，仅作历史参考。

# 工业具身策略学习开题报告大纲

## 一、总体定位

- 暂定研究主线：针对具体工业具身操作任务，研究如何利用示教数据形成策略先验，并考察以 PPO 类强化学习进一步优化任务性能的可行性。
- VLA、示教约束、奖励设计和 PPO 改进均作为“候选方案”，不能写成已经确定有效的方法。
- 暂定题目可表述为：**面向工业具身任务的示教先验与强化学习联合策略学习方法研究**。待任务对象和技术路线稳定后再决定是否在题目中加入“VLA”或“PPO”。
- 保留哈工大开题模板的十个一级栏目；文献综述改为按研究问题和方法主题组织，不机械区分国内外。
- 《章节设计.md》中第二至第五章分别映射为任务建模、模仿策略、强化优化和实验验证，但不直接复制为开题报告目录。

## 二、建议大纲

### 1. 课题来源及研究的目的和意义

#### 1.1 课题来源

说明项目、实验室研究方向或工程需求来源；来源尚未确认时保留待填项，不虚构项目背景。

#### 1.2 研究背景与问题情境

界定具体工业任务、机器人形态、感知输入、动作输出和工作环境；结合文献说明示教成本、强化学习交互成本、稀疏奖励、安全要求、节拍要求等矛盾是否确实存在。

#### 1.3 研究目的

提出“示教策略能否提供有效初始先验”“强化学习能否在保留先验的同时进一步优化”“所得策略能否适应真实工业扰动”等待回答的问题。

#### 1.4 研究意义

分别讨论示教先验与强化学习结合的理论或方法价值，以及对具体工业任务部署效率、性能和可靠性的潜在工程价值；不预设性能必然提升。

### 2. 国内外研究现状及分析（调研后写作方案）

本章不把“国内研究”和“国外研究”机械拆成两份文献清单，而是围绕工业具身任务中的关键问题组织正文，并在各小节内比较国内外代表性工作。这里的“国内/国外”按论文发表时第一作者或主要研究团队的机构所在地判断，不按作者姓名判断；跨国联合工作单列为国际合作。计划形成约 6000—8000 字的综述，篇幅可在学校另有字数要求时调整。

#### 2.1 工业具身任务的对象边界与技术演进

本节回答“本文所称工业具身任务是什么，以及它与一般机器人轨迹控制、家庭服务机器人任务有何区别”。拟按三段展开：

1. **任务边界**：将对象限定为机器人通过视觉、力觉、触觉和本体状态感知环境，并在装配、插接、精密操作等任务中闭环产生动作的策略学习问题；突出接触动力学难建模、装配公差小、失效代价高和节拍受限等工业特征。
2. **技术演进**：从接触丰富操作的引导策略搜索、深度强化学习和技能形式化，写到残差强化学习、元强化学习、操作原语序列和视觉—触觉策略。重点使用 ICRA/IROS 的真实机器人结果说明“学习策略”如何逐步从单任务控制器扩展到可迁移策略。
3. **本节判断**：已有研究证明了学习方法处理未建模接触和环境不确定性的可能性，但任务定义、传感模态、控制接口和成功判据差异较大，论文结果不能仅按成功率横向排序。

核心依据包括 Levine 等的 ICRA 2015 接触丰富操作研究、Inoue 等的 IROS 2017 高精度装配研究、Johannink 等的 ICRA 2019 残差强化学习、Schoettler 等的 IROS 2020 工业插接元强化学习，以及 Nguyen 等的 ICRA 2024 部分可观测装配研究。

#### 2.2 示教学习、视觉动作策略与VLA

本节回答“示教先验能够提供什么，以及从行为克隆发展到 VLA 后新增了哪些能力和约束”。拟按四类工作比较：

1. **显式技能表示与传统模仿学习**：讨论动态/概率运动原语、接触技能和分阶段策略如何利用少量示教，并分析其对任务坐标系、人工分段和先验结构的依赖。IROS 2019 的机器人无关接触技能、ICRA 2021 的操作原语序列，以及哈工大团队基于 ProMPs 的轴孔装配工作可用于国内外对照。
2. **端到端视觉动作策略**：介绍 ACT 和 Diffusion Policy 对动作序列、多峰动作分布及误差累积问题的处理，比较其示教数量、动作频率、闭环反馈与真机任务设置。该部分用于建立强模仿学习基线，而不是把所有 Transformer 或扩散模型统称为 VLA。
3. **跨任务、跨本体与语言条件策略**：以 ICRA 2024 Open X-Embodiment/RT-X 为国际合作代表，以国内团队在 ICRA 2024 发表的对象中心指令增强、快慢思考语言条件策略及后续 RDT-1B、TinyVLA 为对照，分析指令表达、大规模预训练、统一动作空间、模型规模和推理延迟之间的权衡。
4. **本节判断**：VLA 在语言条件、跨对象和跨场景泛化方面扩展了策略能力，但尚不能由通用基准表现直接推出其适合高精度、强接触、低延迟的工业任务。本课题只有在语言输入或跨任务迁移确为必要条件时，才把 VLA 确定为核心模型。

#### 2.3 面向工业操作的强化学习与PPO类方法

本节回答“强化学习解决了模仿策略的哪些不足，以及为什么不能直接把 PPO 写成既定最优方案”。拟按四段展开：

1. **直接策略学习**：以 IROS 2017 高精度装配为起点，说明强化学习能够依据传感反馈形成接触策略，同时指出真机探索代价、奖励稀疏和超参数敏感性。
2. **结构先验与控制融合**：比较引导策略搜索、残差强化学习、低维操作原语、柔顺/力控接口和对称性先验。这类研究的共同特点是保留传统控制或任务结构，仅让学习器优化难以建模的部分。
3. **奖励、迁移与安全**：结合 ICRA 2021 稠密奖励学习、ICRA 2018 动力学随机化、ICRA 2019 SimOpt、IROS 2020 元强化学习和 IEEE RA-L 的安全力控研究，分析样本效率、仿真—真机差异及安全边界。
4. **PPO的定位**：引用 PPO 原始算法说明裁剪目标与 on-policy 更新机制；随后只评述与目标任务直接相关的机器人应用证据。PPO、SAC、TD3 等应在相同观测、动作、奖励和交互预算下比较，不能由算法流行度预先确定最终路线。

本节结论应落到可检验问题：标准 PPO 在目标任务上是否出现样本效率低、稀疏奖励难探索、动作抖动或先验遗忘；只有观察到相应问题后，才提出对应改进项。

#### 2.4 模仿学习与强化学习的联合优化

本节回答“示教先验以什么机制进入强化学习，以及各机制的收益边界是什么”。按以下机制而非作者年份分类：

1. **示教初始化或预训练**：先训练行为克隆策略，再以强化学习优化；需关注初始性能、探索覆盖和灾难性退化。
2. **示教数据参与强化学习更新**：包括示教回放、辅助行为克隆损失、奖励/进度学习等；重点比较示教质量、示教数量和训练阶段。
3. **残差、门控或集成策略**：让学习策略修正传统控制器或模仿策略，或者在模仿、柔顺控制与强化动作之间融合；适合讨论工业任务的安全性和可解释降级路径。
4. **离线到在线与仿真到真机**：区分“仅在仿真中优化后真机推理”“少量真机自适应”和“真机在线训练”，比较真实交互次数及安全保护。

国内研究可重点写中国科学院自动化研究所团队的精密装配技能学习与示教加速强化学习、哈工大团队的几何表示模仿学习，以及 2026 年《Robotics and Computer-Integrated Manufacturing》中两项示教—强化联合装配工作；国外研究可用 Nair 等的 ICRA 2018 示教增强强化学习、Johannink 等的 ICRA 2019 残差强化学习和 Schoettler 等的 IROS 2020 元强化学习形成对照。收束时应指出：现有论文所用算法、控制接口、真实交互预算和任务公差并不一致，不能把某篇论文的性能提升直接视为“示教先验对 PPO 有效”的证据。

#### 2.5 策略评价、泛化与工业部署指标

本节回答“如何公平评价策略，而不只报告一次成功率”。拟建立四层评价框架：

1. **任务完成层**：成功率、完成时间/节拍、插入深度或装配质量、末端位姿误差、峰值/均方接触力、碰撞或卡滞次数。
2. **学习过程层**：示教数量与时长、环境交互步数、达到阈值性能所需样本、训练方差、计算与显存开销；PPO 类方法还需报告多随机种子结果。
3. **泛化与鲁棒性层**：工件位置和姿态偏差、尺寸与公差、摩擦/刚度变化、光照与背景、相机位姿、传感噪声、未见对象和仿真—真机迁移。每种扰动分级设置，报告性能随扰动强度的退化曲线。
4. **部署与可靠性层**：控制频率、端到端推理延迟、安全违规次数、人工接管率、失败类型及恢复能力。真机结果报告试验次数、均值和离散程度，避免用少量演示视频代替统计结果。

RLBench、CALVIN、RoboMimic、THE COLOSSEUM 和 CloudGripper-Push-1K 用于说明通用机器人学习中的任务、长时序和扰动评价方法；它们不能替代本课题的工业任务协议。本课题最终应固定训练/测试划分、初始状态分布、最大步数、成功判据、失败判据和交互预算，再比较纯模仿、从零 PPO、模仿初始化 PPO 及候选联合方法。

#### 2.6 国内外比较与研究现状评述

本节采用“共同进展—路线差异—目标场景缺口—本研究切入点”的三至四段结构：

- **共同进展**：国内外研究均已从预编程轨迹扩展到视觉/力觉闭环策略，并通过示教、仿真、控制先验或大规模预训练降低策略学习难度。
- **路线差异**：国外 ICRA/IROS 代表工作较早系统讨论策略搜索、残差学习、元学习、跨本体数据和标准化评价；国内团队在精密轴孔装配、微装配、几何先验、轻量 VLA 和示教—强化融合方面形成了针对性较强的研究。该比较只描述本次检索样本，不外推为整个国内外研究水平的定论。
- **拟保留缺口一**：通用视觉/VLA 策略与高精度接触控制之间仍有接口和评价尺度差异，模型泛化能力未必转化为工业公差下的稳定闭环性能。
- **拟保留缺口二**：示教初始化、示教约束与强化优化经常同时出现，示教先验究竟改善初始性能、探索效率还是最终策略质量，缺少在统一预算和统一控制接口下的消融证据。
- **拟保留缺口三**：不少研究侧重成功率，未同时给出节拍、接触力、安全违规、样本成本和扰动边界，难以支持多目标工业部署判断。

以上缺口仍需在具体工业任务、平台和前期基线确定后复核。若前期实验不支持某一缺口，应删除或收窄，不能为迎合预设方法而保留。

### 3. 前期研究基础

#### 3.1 任务与实验平台基础

仅列出实际具备的机器人、相机、末端执行器、仿真环境和安全设施。

#### 3.2 数据与软件基础

说明已采集示教数据、已有算法代码、模型、算力和仿真资产的真实状态。

#### 3.3 已完成的预研工作

按“完成事项—方法或材料—可核验状态—对后续研究的支撑”组织。《章节设计.md》本身不作为已完成研究的证据。

### 4. 主要研究内容与研究目标

#### 4.1 主要研究内容

- 任务一：界定工业任务，建立观测、动作、约束、扰动因素及评价协议。
- 任务二：构建并评估候选模仿策略，研究示教数据预处理、多模态输入及噪声处理。
- 任务三：研究示教先验引导的 PPO 优化方法；具体约束项、奖励项或训练机制根据标准 PPO 暴露的问题确定。
- 任务四：开展仿真和真机验证，分析性能收益、适用条件、失败模式和局限性。

#### 4.2 研究目标

- 形成可复现的任务模型和评价基准。
- 获得可完成目标任务的模仿策略基线。
- 判断示教先验对 PPO 收敛、样本效率和策略性能的实际作用。
- 通过对比、消融及扰动实验确定候选方法的收益边界，而非预设其必然优于基线。

#### 4.3 拟解决的关键问题

- 如何将示教先验引入后续强化学习，同时避免策略退化或过度限制探索。
- 如何协调成功率、任务节拍、安全性和动作平滑等可能冲突的目标。
- 如何降低视觉噪声、位姿偏差、工件公差及仿真—真机差异对策略的影响。

### 5. 研究方案及可行性论证

#### 5.1 总体技术路线

任务定义与评价协议 → 示教数据采集和处理 → 模仿策略基线 → 标准 PPO 基线 → 候选联合优化方法 → 仿真对比与消融 → 安全审查 → 真机验证 → 失败分析。

#### 5.2 方法选择决策点

- 只有在语言或多模态预训练能力与目标任务相关、且算力和数据条件可满足时，才将 VLA 确定为核心模型；否则降级为较轻量的多模态行为克隆策略。
- PPO 改进项必须对应标准 PPO 中实际观察到的问题，不预先把课程学习、示教约束、节拍奖励等全部写成必要组成。
- 真机在线训练须以安全条件为前提；条件不足时采用仿真训练、真机推理验证或有限参数微调。

#### 5.3 实验设计

- 基线原则上包括：纯模仿策略、从零训练的标准 PPO、模仿初始化加标准 PPO、模仿先验加候选优化方法。
- 指标包括：任务成功率、完成时间或节拍、训练样本量与收敛速度、鲁棒性、安全违规次数及动作平滑度。
- 消融实验只针对最终保留的组件逐项移除；多模态融合、示教约束、节拍奖励、课程学习等当前仅为候选项。
- 鲁棒性测试覆盖实际任务中有依据的扰动，不为丰富实验数量而虚构测试条件。

#### 5.4 可行性分析

分别论证理论依据、数据条件、软硬件条件、训练成本、真机安全条件和时间条件；每项均对应具体研究任务。

### 6. 研究进度与预期成果

#### 6.1 进度安排

按“研究边界与综述—平台和评价协议—模仿基线—强化学习基线与方法选择—仿真实验—真机验证—论文撰写”分阶段安排。具体年月待培养计划和开题节点确认后填写，并预留实验失败与设备维护缓冲。

#### 6.2 预期成果

形成任务模型与评价协议、模仿学习基线、经验证的联合优化方法或适用性结论、仿真与真机实验结果及学位论文。论文、专利等仅在确有计划时列入。

### 7. 预期创新点

改写为“拟验证的创新假设”，最多保留两项：

- 示教先验在 PPO 优化中的保持和利用机制可能改善训练效率或稳定性。
- 面向工业任务多目标约束的训练方法可能改善成功率、节拍与安全性的综合表现。

每项必须给出对应文献差异、比较基线、评价指标和消融实验；证据不足时降级为研究特点，不强称创新。

### 8. 研究条件、外协计划及经费

按机器人平台、感知与末端设备、仿真软件、计算资源、示教数据、场地安全条件、外协和经费逐项填写，并区分“已具备”和“尚需补充”。

### 9. 可能的困难、风险及解决措施

重点覆盖 VLA 数据或算力不足、PPO 训练不稳定、奖励设计偏差、仿真—真机差异、真机探索风险、实验范围过宽等风险。每项按“触发条件—影响—预防措施—降级方案”编写。

### 10. 主要参考文献

建立“论点—主题—代表文献—适用条件—局限—正文位置”文献矩阵；优先收集具身策略学习、VLA/模仿学习、机器人强化学习、联合优化及工业验证方面的原始论文，不补造引用。

## 三、结构验收与 LaTeX 落地

- 检查“研究缺口—问题—目标—任务—方法—指标—成果”是否逐项对应。
- 全文区分“已完成、拟开展、预期获得”，所有暂定路线使用“拟、候选、待验证”等表述。
- 后续仅调整 `body/proposal.tex` 的正文层级和内容，不修改文档类；使用 XeLaTeX 编译并检查目录、表格、参考文献和分页。
- 当前未确定且必须保留占位的内容包括：正式题目、具体工业任务、机器人平台、前期实验结果、目标阈值、进度日期及课题来源。

## 四、研究现状调研与写作执行计划

### 1. 检索范围

- **检索截止日**：2026 年 8 月 25 日。
- **重点来源**：IEEE International Conference on Robotics and Automation（ICRA）、IEEE/RSJ International Conference on Intelligent Robots and Systems（IROS）。
- **补充来源**：IEEE Robotics and Automation Letters、IEEE Transactions on Robotics、IEEE/ASME Transactions on Mechatronics、IEEE Transactions on Industrial Informatics、IEEE CASE，以及 Elsevier 旗下 Robotics and Computer-Integrated Manufacturing、Engineering Applications of Artificial Intelligence、Robotics and Autonomous Systems。
- **必要的交叉来源**：RSS、CoRL、ICLR 和经同行评审的机器人学习基准论文，用于补足 ACT、Diffusion Policy、RoboMimic、RDT 等无法由 ICRA/IROS 完整覆盖的关键路线。
- **时间分层**：2015—2020 年选取奠定方法脉络的工作，2021—2026 年作为主体；若同一工作同时存在预印本和正式版本，只引用正式版本。

### 2. 检索式与筛选标准

建议组合以下英文检索词，并在 IEEE Xplore、ScienceDirect、Crossref、DBLP 和会议官网交叉查询：

- `robotic assembly` / `industrial insertion` / `peg-in-hole` / `contact-rich manipulation`；
- `policy learning` / `reinforcement learning` / `imitation learning` / `learning from demonstration`；
- `PPO` / `residual reinforcement learning` / `meta reinforcement learning` / `reward learning`；
- `vision-language-action` / `diffusion policy` / `action chunking` / `cross-embodiment`；
- `benchmark` / `evaluation` / `generalization` / `robustness` / `sim-to-real` / `safety`。

纳入标准：与机器人真实动作策略直接相关；提供明确任务、输入、动作、训练方式和评价；正式发表信息可核验；对于方法类论文，至少有仿真或真机操作实验。排除仅做目标检测、纯文本规划、无机器人动作输出的“具身”论文，以及只有摘要、二次转载或无法确认正式出处的条目。

### 3. 文献阅读卡片

每篇文献建立一行记录，字段固定为：

`文献键｜国内/国外/国际合作｜任务与平台｜观测模态｜动作/控制接口｜示教规模｜学习算法｜是否真机｜训练预算｜成功判据｜主要指标｜对比与消融｜贡献｜适用条件｜局限｜拟放正文位置｜DOI/官方链接`。

阅读时先摘录论文实际报告的实验设置和结论，再写作者评述。没有报告的数据填“未报告”，不根据图像或摘要估算；宣传性项目页面只用于寻找正式论文，不作为性能数字的最终来源。

### 4. 落笔顺序与阶段产出

1. **任务与评价先行**：先确定具体工业任务、观测/动作、控制频率和成功判据，形成 2.1 与 2.5 初稿；产出一页任务定义表和一页指标表。
2. **方法谱系梳理**：完成示教学习、强化学习和联合优化三张文献矩阵，分别形成 2.2、2.3、2.4 初稿。
3. **国内外比较**：以机构信息已核验的论文为依据，在每个主题内比较国内外路线；跨国联合论文不强行归类。
4. **凝练研究缺口**：把文献局限映射到目标任务，只保留能由本课题实验回答的两至三个缺口。
5. **引文与语言核查**：逐句检查事实性判断是否有引文，统一术语和结论强度；将正式采用的条目写入 `reference.bib`，正文使用 `\cite{}`。
6. **LaTeX 验收**：转写 `body/proposal.tex` 后使用 XeLaTeX 编译，检查引文—文后条目对应、长表格跨页、英文标题断行和目录层级。

## 五、已核验的核心文献池

下表中的 ICRA/IROS 条目均已通过 IEEE Xplore、DOI 或正式会议记录核验，可作为本章的主干证据。表中“用途”是写作角色，不代表论文结论可无条件外推到本课题。

### 1. ICRA/IROS主干文献

| 文献 | 正式出处 | 核验链接 | 主要写作用途 |
| --- | --- | --- | --- |
| Levine, Wagener, Abbeel, *Learning Contact-Rich Manipulation Skills with Guided Policy Search* | ICRA 2015 | [DOI](https://doi.org/10.1109/ICRA.2015.7138994) | 接触丰富操作与引导策略搜索的早期代表 |
| Inoue et al., *Deep Reinforcement Learning for High Precision Assembly Tasks* | IROS 2017 | [DOI](https://doi.org/10.1109/IROS.2017.8202244) | 高精度轴孔装配的直接深度强化学习 |
| Nair et al., *Overcoming Exploration in Reinforcement Learning with Demonstrations* | ICRA 2018 | [DOI](https://doi.org/10.1109/ICRA.2018.8463162) | 示教缓解稀疏奖励探索困难 |
| Peng et al., *Sim-to-Real Transfer of Robotic Control with Dynamics Randomization* | ICRA 2018 | [DOI](https://doi.org/10.1109/ICRA.2018.8460528) | 动力学随机化与仿真到真机迁移 |
| Johannink et al., *Residual Reinforcement Learning for Robot Control* | ICRA 2019 | [DOI](https://doi.org/10.1109/ICRA.2019.8794127) | 传统控制与学习残差融合，含真实装配任务 |
| Ramos et al., *Closing the Sim-to-Real Loop: Adapting Simulation Randomization with Real World Experience* | ICRA 2019 | [DOI](https://doi.org/10.1109/ICRA.2019.8793789) | 用少量真机经验更新仿真分布 |
| Johannsmeier, Gerchow, Haddadin, *A Framework for Robot Manipulation: Skill Formalism, Meta Learning and Adaptive Control* | ICRA 2019 | [DOI](https://doi.org/10.1109/ICRA.2019.8793542) | 技能形式化、元参数学习与工业公差评价 |
| Scherzinger, Roennau, Dillmann, *Contact Skill Imitation Learning for Robot-Independent Assembly Programming* | IROS 2019 | [DOI](https://doi.org/10.1109/IROS40897.2019.8967523) | 接触技能模仿和跨机器人执行 |
| Hamaya et al., *Learning Robotic Assembly Tasks with Lower Dimensional Systems by Leveraging Physical Softness and Environmental Constraints* | ICRA 2020 | [DOI](https://doi.org/10.1109/ICRA40945.2020.9197327) | 物理柔顺性、环境约束与低维学习 |
| Schoettler et al., *Meta-Reinforcement Learning for Robotic Industrial Insertion Tasks* | IROS 2020 | [DOI](https://doi.org/10.1109/IROS45743.2020.9340848) | 工业插接的仿真元训练和少量真机适应 |
| Wu et al., *Learning Dense Rewards for Contact-Rich Manipulation Tasks* | ICRA 2021 | [DOI](https://doi.org/10.1109/ICRA48506.2021.9561891) | 从高维观测学习任务进度和稠密奖励 |
| Vuong, Pham, Pham, *Learning Sequences of Manipulation Primitives for Robotic Assembly* | ICRA 2021 | [DOI](https://doi.org/10.1109/ICRA48506.2021.9561029) | 强化学习发现操作原语序列及直接迁移 |
| Gai et al., *Model-Driven Reinforcement Learning and Action Dimension Extension Method for Efficient Asymmetric Assembly* | ICRA 2022 | [DOI](https://doi.org/10.1109/ICRA46639.2022.9811792) | 清华团队的模型先验、动作维度扩展与非对称装配 |
| Braun, Wrede, *Grey-Box Learning of Adaptive Manipulation Primitives for Robotic Assembly* | ICRA 2023 | [DOI](https://doi.org/10.1109/ICRA48891.2023.10161077) | 灰盒先验与自适应操作原语 |
| Le et al., *Learning Robotic Assembly by Leveraging Physical Softness and Tactile Sensing* | IROS 2023 | [DOI](https://doi.org/10.1109/IROS55552.2023.10341471) | 柔性腕、触觉和不确定装配评价 |
| Nguyen et al., *Symmetry-Aware Reinforcement Learning for Robotic Assembly under Partial Observability with a Soft Wrist* | ICRA 2024 | [DOI](https://doi.org/10.1109/ICRA57147.2024.10610103) | 部分可观测装配、对称先验与真机样本效率 |
| Wen et al., *Object-Centric Instruction Augmentation for Robotic Manipulation* | ICRA 2024 | [DOI](https://doi.org/10.1109/ICRA57147.2024.10609992) | 国内团队的对象位置增强指令与模仿策略 |
| Zhu et al., *Language-Conditioned Robotic Manipulation with Fast and Slow Thinking* | ICRA 2024 | [DOI](https://doi.org/10.1109/ICRA57147.2024.10611525) | 国内团队的语言任务分流、视觉语言推理与策略对齐 |
| Open X-Embodiment Collaboration, *Open X-Embodiment: Robotic Learning Datasets and RT-X Models* | ICRA 2024 | [DOI](https://doi.org/10.1109/ICRA57147.2024.10611477) | 跨本体数据、通用策略和评价边界 |
| Burns et al., *GenCHiP: Generating Robot Policy Code for High-Precision and Contact-Rich Manipulation Tasks* | IROS 2024 | [DOI](https://doi.org/10.1109/IROS58592.2024.10801525) | 大模型生成高精度接触策略代码及顺应动作空间 |
| Jin et al., *How Physics and Background Attributes Impact Video Transformers in Robotic Manipulation: A Case Study on Planar Pushing* | IROS 2024 | [DOI](https://doi.org/10.1109/IROS58592.2024.10802583) | 数据属性、视觉策略泛化和 CloudGripper-Push-1K |

### 2. 国内团队与IEEE/Elsevier补充文献

以下条目用于补充国内研究和工业期刊证据。正式写作时只在论文首页或作者机构官方页面已确认的情况下使用“国内团队”表述。

| 文献 | 正式出处 | 核验链接 | 主要写作用途 |
| --- | --- | --- | --- |
| Yang et al., *A Learning Framework of Adaptive Manipulative Skills From Human to Robot* | IEEE TII, 2019 | [DOI](https://doi.org/10.1109/TII.2018.2826064) | 国内外合作的示教技能分段、调节与泛化 |
| Qin et al., *Robotic Skill Learning for Precision Assembly With Microscopic Vision and Force Feedback* | IEEE/ASME T-Mech, 2019 | [DOI](https://doi.org/10.1109/TMECH.2019.2909081) | 中国科学院自动化所的微装配多模态技能学习 |
| Wu et al., *Deep Reinforcement Learning of Robotic Precision Insertion Skill Accelerated by Demonstrations* | IEEE CASE 2019 | [DOI](https://doi.org/10.1109/COASE.2019.8842940) | 中国科学院自动化所的示教加速精密插接强化学习 |
| Beltran-Hernandez et al., *Learning Force Control for Contact-Rich Manipulation Tasks With Rigid Position-Controlled Robots* | IEEE RA-L, 2020 | [DOI](https://doi.org/10.1109/LRA.2020.3010739) | 强化学习与力控接口、失效保护和真机安全训练 |
| Zang et al., *Peg-in-Hole Assembly Skill Imitation Learning Method Based on ProMPs under Task Geometric Representation* | Frontiers in Neurorobotics, 2023 | [DOI](https://doi.org/10.3389/fnbot.2023.1320251) | 哈工大团队的几何表示、ProMPs 与行为克隆 |
| Gai et al., *Local Connection Reinforcement Learning Method for Efficient Robotic Peg-in-Hole Assembly* | Elsevier EAAI, 2024 | [DOI](https://doi.org/10.1016/j.engappai.2024.108520) | 清华团队的状态—动作局部连接与训练效率 |
| Wen et al., *TinyVLA: Toward Fast, Data-Efficient Vision-Language-Action Models for Robotic Manipulation* | IEEE RA-L, 2025 | [DOI](https://doi.org/10.1109/LRA.2025.3544909) | 国内高校与企业团队的轻量 VLA、推理速度和数据效率 |
| Ding et al., *An Ensemble Reinforcement Learning Framework for Robotic High-Precision Peg-in-Hole Assembly via Human Demonstrations* | Elsevier RCIM, 2026 | [DOI](https://doi.org/10.1016/j.rcim.2026.103279) | 哈工大团队的示教、SAC、混合力/位控制和跨几何迁移 |
| Su, Zheng, Shen, *Robot Assembly Using Variable Admittance Control with Reinforcement Learning from Demonstrations in a Constrained Region* | Elsevier RCIM, 2026 | [DOI](https://doi.org/10.1016/j.rcim.2026.103259) | 中国科学院自动化所团队的受限域示教、变导纳与在线适应 |

### 3. 方法与评价的必要补充文献

| 文献 | 正式出处 | 核验链接 | 主要写作用途 |
| --- | --- | --- | --- |
| Schulman et al., *Proximal Policy Optimization Algorithms* | arXiv, 2017，预印本 | [arXiv](https://arxiv.org/abs/1707.06347) | 仅用于 PPO 算法原理，不作为工业有效性证据 |
| Mahmood et al., *Benchmarking Reinforcement Learning Algorithms on Real-World Robots* | CoRL 2018 | [PMLR](https://proceedings.mlr.press/v87/mahmood18a.html) | 真机算法评测、超参数敏感性和可复现性 |
| James et al., *RLBench: The Robot Learning Benchmark & Learning Environment* | IEEE RA-L, 2020 | [DOI](https://doi.org/10.1109/LRA.2020.2974707) | 多任务、多模态观测和示教基准 |
| Mandlekar et al., *What Matters in Learning from Offline Human Demonstrations for Robot Manipulation* | CoRL 2021/正式论文集 2022 | [PMLR](https://proceedings.mlr.press/v164/mandlekar22a.html) | RoboMimic、示教质量和离线策略公平比较 |
| Mees et al., *CALVIN: A Benchmark for Language-Conditioned Policy Learning for Long-Horizon Robot Manipulation Tasks* | IEEE RA-L, 2022 | [DOI](https://doi.org/10.1109/LRA.2022.3180108) | 语言条件长时序评价 |
| Zhao et al., *Learning Fine-Grained Bimanual Manipulation with Low-Cost Hardware* | RSS 2023 | [DOI](https://doi.org/10.15607/RSS.2023.XIX.016) | ACT、动作分块和低成本双臂真机示教 |
| Chi et al., *Diffusion Policy: Visuomotor Policy Learning via Action Diffusion* | RSS 2023 | [DOI](https://doi.org/10.15607/RSS.2023.XIX.026) | 多峰动作分布、动作序列和模仿学习强基线 |
| Pumacay et al., *THE COLOSSEUM: A Benchmark for Evaluating Generalization for Robotic Manipulation* | RSS 2024 | [正式会议论文](https://www.roboticsproceedings.org/rss20/p133.html) | 多扰动轴、性能退化与泛化评价 |
| Liu et al., *RDT-1B: A Diffusion Foundation Model for Bimanual Manipulation* | ICLR 2025 | [ICLR论文](https://proceedings.iclr.cc/paper_files/paper/2025/file/49f80e4d2471ad4f2edf4f5f1ab62339-Paper-Conference.pdf) | 国内团队的跨机器人预训练、统一动作空间和双臂策略 |
| Elguea-Aguinaco et al., *A Review on Reinforcement Learning for Contact-Rich Robotic Manipulation Tasks* | Elsevier RCIM, 2023 | [DOI](https://doi.org/10.1016/j.rcim.2022.102517) | 用于核对接触丰富强化学习分类；正文结论仍回到原始论文 |

### 4. 真实性与引用控制

- 正式论文以 DOI、IEEE Xplore、ScienceDirect、PMLR、RSS 或 ICLR 正式论文页为准；DBLP 和项目主页仅作交叉核验。
- 预印本必须标注“预印本”，不能与正式 ICRA/IROS/期刊论文并列作为强结论依据。若后续找到正式版本，应替换为正式版本。
- 性能数字必须回到论文表格、实验段或补充材料核对，并同时记录任务、试验次数和比较条件；不从二次综述复制数字。
- 国内外归类必须核对论文发表时的作者机构；国际合作论文单列，不依据作者姓名推断国别。
- 不以会议级别代替方法有效性判断，也不以“最新”“大模型”“VLA”等标签替代对任务条件和评价协议的分析。
- 在正文形成强判断前至少需要一篇原始论文直接支撑；涉及领域总体趋势时，原则上需要两篇以上相互独立的研究或一篇高质量综述与原始论文交叉支撑。


[$write-thesis-proposal](/home/njx-10096304/.codex/skills/write-thesis-proposal/SKILL.md) 撰写第三章，首先开始要根据本文研究方法，用大量公式推导说明