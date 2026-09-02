# Repository Guidelines

## Project Structure & Module Organization

`report.tex` is the XeLaTeX entry point. Edit report metadata in `front/cover.tex` and the proposal text in `body/proposal.tex`; keep bibliography records in `reference.bib`. Store publication-ready images and TikZ sources in `figures/`, and document the provenance of borrowed figures in `figures/README.md`. The `scripts/` directory contains Python utilities for generating figures. Files under `reference/` are source material, while `tmp/` is working output for visual checks and should normally not be committed. Avoid modifying `hithesisart.cls`, `hithesisart.cfg`, or `hithesis.bst` unless the template itself must change.

## Build, Test, and Development Commands

- `latexmk`: compile `report.tex` with XeLaTeX and produce `report.pdf`.
- `latexmk -c report.tex`: remove intermediate LaTeX files while preserving the PDF.
- `latexmk -C report.tex`: remove intermediate files and the generated PDF.
- `python scripts/visualize_right_hand.py data.hdf5 --output-dir figures/right_hand_visualization`: regenerate the right-hand trajectory assets; requires `h5py`, `numpy`, and Pillow.

Run commands from the repository root. The build uses shell escape, as configured in `latexmkrc`.

## Coding Style & Naming Conventions

Keep TeX files UTF-8 encoded. Follow the existing two-space indentation inside environments and place one logical sentence or command per line when practical. Use descriptive, lowercase labels such as `fig:research-entry-route` and stable lowercase BibTeX keys such as `schulman2017ppo`. Name new figure files with lowercase kebab-case. Python follows PEP 8, four-space indentation, type hints, `snake_case` functions, and `UPPER_CASE` constants.

## Testing Guidelines

There is no automated test framework or coverage target. Every content or template change must pass `latexmk` without errors or unresolved-reference warnings. Open `report.pdf` and inspect changed pages for clipping, misplaced floats, font substitution, broken citations, and image readability. For Python utilities, run the script against a representative HDF5 episode and verify all expected PNG and README outputs.

## Commit & Pull Request Guidelines

Recent history uses brief Chinese summaries such as `精简正文` and `修复编译错误，新增数据集示例`. Keep commits focused and use a short imperative summary describing the result. Pull requests should explain the affected sections, list the validation command, and note any template or bibliography changes. Include screenshots or page numbers for layout-sensitive edits, and do not commit LaTeX intermediates or scratch renderings.
