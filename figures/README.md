# 插图目录

将开题报告所需的 PDF、PNG、JPG 或 EPS 图片放在此目录中。正文中可直接使用：

```tex
\begin{figure}[htbp]
  \centering
  \includegraphics[width=0.8\textwidth]{文件名}
  \caption{图题}
  \label{fig:example}
\end{figure}
```

## 研究方法关系示意图

`wrist-visual-docking-estimation.pdf` 和同名 PNG 为该图的独立导出版本，可用于幻灯片或其他文档；报告通过同名 TikZ 源文件编译。

- `wrist-visual-docking-estimation.tex`：本课题自绘的腕部局部视觉停靠偏差估计说明图。依次展示固定观察位姿、标称与当前停靠条件下的彩色和深度观测、标称停靠坐标系中的平移与航向偏差。检测台边框与定位结构、百叶车立柱分别作为固定几何特征示例；观测图、深度着色和偏差均为概念示意，不来自实测数据，不表示已确定的配准算法或估计精度。蓝色虚线表示标称参考，橙色实线表示当前观测或关注的工装特征；独立参考测量不在图中作为视觉估计输入。

- `policy-risk-architecture.tex`、`policy-error-fusion-delta.tex`、`policy-risk-stop-delta.tex`、`policy-risk-scheduling-delta.tex`：本课题自绘的策略模型与三项研究方法结构图，对应正文图13、14、15、17。图13保留完整的数据流、训练关系和执行控制关系；后三图分别展示误差融合训练、风险判别与提前停止、风险驱动调度与RTC衔接。沿用原图的输入、VLM主干、动作专家及执行端结构，调整节点间距和走线；将前一序列尾部与当前候选序列的比较关系显式连入风险模型。橙色粗框突出当前研究关注的模块，蓝灰色表示沿用内容。
- `policy-progressive-common.tex`：上述四图共用的TikZ源文件，先定义误差融合策略与执行闭环，再按研究阶段添加风险判别支路、提前停止控制、步数调度及RTC引导。图13显示完整结构，派生图强调对应研究模块。图内连线均表达信息、训练或控制关系；各图为拟研究方法示意，不表示已验证效果。
- 图14按其模块数量采用紧凑布局：加宽状态输入框、收紧策略内部间距，执行框置于右侧中部，反馈线经下方返回图像输入；保留与原图一致的节点及连接关系。图13、15、17继续采用包含风险分支的布局。
- 图13、15、17保留完整风险分支，纵向收紧策略网络、序列比较、风险判别及训练框的间距，缩短上方反馈回路；加宽增广状态框以减少换行，保持原字号和节点连接关系，并通过编译后的页面渲染复核标注与箭头。

- `research-entry-route.tex`、`research-architecture.tex`、`risk-prediction-stop.tex`和`risk-driven-scheduling.tex`：本课题研究关系示意，已统一为开题研究思路表述。风险曲线与执行区间为概念示意，不表示实验数据；未预设固定阈值算法或退让动作模板。

## 文献引图来源

- `diffusion-policy-overview.pdf`：Chi 等，*Diffusion Policy: Visuomotor Policy Learning via Action Diffusion*，RSS 2023，原图 3。取自 RSS 正式论文 PDF，仅裁去论文正文和原英文图注，图内内容未作修改。
- `pi05-model-overview.png`：Black 等，*π0.5: A Vision-Language-Action Model with Open-World Generalization*，Physical Intelligence 技术报告 2025，原图 3。取自作者公开的 PDF 版本，仅裁去页边与原英文图注，图内内容未作修改。
- `colosseum-perturbations.pdf`：Pumacay 等，*THE COLOSSEUM: A Benchmark for Evaluating Generalization for Robotic Manipulation*，RSS 2024，原图 3。取自 RSS 正式论文 PDF，仅裁去论文正文和原英文图注，图内内容未作修改。

正文图题仅保留对应文献编号；原图号、版本与裁剪说明集中记录在本文件中。如后续对图形内容进行翻译、删改或重绘，应在本文件中补充记录修改内容。

## 研究背景组图来源

`background-illustrations/` 中的图片用于正文“课题来源与研究背景”的三组 2×2 子图。为减少组图内部空白，所有图片均以主体为中心等比例缩放并裁切为 1200×750 像素；未对图中的机器人、工艺设备或人物进行内容性增删。

- `ind-welding.jpg`：Balasubramaniam 等，“Refill friction stir spot welding robot CR HR”，CC BY 4.0，Wikimedia Commons：<https://commons.wikimedia.org/wiki/File:Refill_friction_stir_spot_welding_robot_CR_HR.jpg>。
- `ind-assembly.jpg`：Mixabest，“KUKA Industrial Robots IR”，CC BY-SA 3.0，Wikimedia Commons：<https://commons.wikimedia.org/wiki/File:KUKA_Industrial_Robots_IR.jpg>。
- `ind-palletizing.jpg`：KUKA Roboter GmbH, Bachmann，“Factory Automation Robotics Palettizing Bread”，由权利人释入公有领域，Wikimedia Commons：<https://commons.wikimedia.org/wiki/File:Factory_Automation_Robotics_Palettizing_Bread.jpg>。
- `ind-pcb.jpg`：Shixart1985，“Machine places components on a circuit board during manufacturing in a factory environment”，CC BY 2.0，Wikimedia Commons：<https://commons.wikimedia.org/wiki/File:Machine_places_components_on_a_circuit_board_during_manufacturing_in_a_factory_environment.jpg>。
- `emb-humanoid.jpg`：Nicholas-halodi，“Halodi Robotics' Perception Engineer With a Humanoid Collaborative Robot”，CC BY-SA 4.0，Wikimedia Commons：<https://commons.wikimedia.org/wiki/File:Halodi_Robotics%27_Perception_Engineer_With_a_Humanoid_Collaborative_Robot.jpg>。
- `emb-quadruped.jpg`：Sgt. Mallory S. VanderSchans，“Legged squad support system demonstration held 120910-M-LU710-074”，美国政府作品，Wikimedia Commons：<https://commons.wikimedia.org/wiki/File:Legged_squad_support_system_demonstration_held_120910-M-LU710-074.jpg>。
- `emb-mobile.jpg`：Auledas，“ER-FLEX mobile manipulator”，CC BY 4.0，Wikimedia Commons：<https://commons.wikimedia.org/wiki/File:ER-FLEX_mobile_manipulator.jpg>。
- `emb-bimanual.jpg`：Steve Jurvetson，“Rethink Robotics — Brooks and Baxter”，CC BY 2.0，Wikimedia Commons：<https://commons.wikimedia.org/wiki/File:Rethink_Robotics_%E2%80%94_Brooks_and_Baxter_(8000143255).jpg>。
- `mfg-tending.jpg`：EGU-Metall，“EGU-Metall CNC-Fräsen mit Roboterautomatisierung”，CC BY-SA 3.0，Wikimedia Commons：<https://commons.wikimedia.org/wiki/File:EGU-Metall_CNC-Fr%C3%A4sen_mit_Roboterautomatisierung.jpg>。
- `mfg-amr.jpg`：Rlistmedia，“Autonomous Mobile Robot AMR”，CC BY 4.0，Wikimedia Commons：<https://commons.wikimedia.org/wiki/File:Autonomous_Mobile_Robot_AMR.png>。
- `mfg-quality.jpg`：National Institute of Standards and Technology，“Real-time Quality Control for Welding”，条目标记为美国政府作品，摄影署名 Geoffrey Wheeler Photography，Wikimedia Commons：<https://commons.wikimedia.org/wiki/File:Real-time_Quality_Control_for_Welding_(5884928619).jpg>。正文图注已明确指向 NIST 的焊接质量监测工作，不作通用素材使用。
- `mfg-collab.jpg`：Jeff Green / Rethink Robotics，“Schramberg - Sawyer 3”，CC BY 4.0，Wikimedia Commons：<https://commons.wikimedia.org/wiki/File:Schramberg_-_Sawyer_3.jpg>。

## 工业具身机器人案例组图来源

- `agibot-longcheer/g2-station-operation.jpg`：智元精灵G2在龙旗科技南昌平板制造工厂检测工位作业。原图见 IT之家 2026-04-15 报道《全球首个具身智能工业产线规模落地：智元精灵 G2 连续 8 小时作业零失误》（新浪科技同日转载）：<https://www.ithome.com/0/939/194.htm>。为统一组图版式，以机器人和检测工位为中心等比例裁切并缩放为 1200×750 像素，未作内容性增删。
- `agibot-longcheer/g2-production-line.jpg`：智元精灵G2在龙旗科技工厂多机并线作业。原图见上海证券报 2026-06-30 报道《智元第15000台机器人交付至龙旗产线 机器人“工友”交出怎样的答卷？》：<https://paper.cnstock.com/html/2026-06/30/content_2237360.htm>。为统一组图版式，以产线中的机器人为中心等比例裁切并缩放为 1200×750 像素，未作内容性增删。
