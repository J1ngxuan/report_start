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
