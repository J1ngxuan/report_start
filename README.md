# 哈尔滨工业大学开题报告模板

当前项目已整理为 hithesis 的开题报告结构，默认生成“哈尔滨校区硕士学位开题报告”。

## 开始填写

1. 在 `report.tex` 的 `\documentclass` 选项中确认学位类型和校区：
   - `type=doctor|master|bachelor`
   - `campus=harbin|shenzhen|weihai`
   - 开题阶段保持 `stage=opening`
2. 在 `front/cover.tex` 填写题目、学院、学科、姓名、学号和导师。
3. 在 `body/proposal.tex` 替换灰色填写提示，并按学院要求增删小节。
4. 在 `reference.bib` 添加 BibTeX 文献条目，并在 `body/proposal.tex` 末尾取消文献命令
   的注释；图片放入 `figures/`。

## 编译

项目使用 XeLaTeX：

```bash
latexmk
```

输出文件为 `report.pdf`。清理中间文件使用 `latexmk -c report.tex`；连同 PDF
一并清理使用 `latexmk -C report.tex`。

## 主要文件

```text
report.tex             主文件与报告类型配置
front/cover.tex        封面信息
body/proposal.tex      开题报告正文骨架
reference.bib          参考文献数据库
figures/               插图
hithesisart.cls/.cfg   hithesis 开题/中期报告类
```

模板类文件来自 hithesis v3.1e 的开题/中期报告实现。提交前请以所在学院当年发布的
Word 表格或通知为准，尤其核对封面字段、章节顺序和签字页要求。
