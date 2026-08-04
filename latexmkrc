# vim: set ft=perl:
@default_files = ('report.tex');

$pdf_mode = 1;
$bibtex_use = 2;
$recorder = 1;
$clean_ext = 'xdv thm';
$pdflatex = 'xelatex -file-line-error --shell-escape -synctex=1 -interaction=nonstopmode %O %S';
$pdf_update_method = 0;
