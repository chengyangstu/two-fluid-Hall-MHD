#!/usr/bin/env bash
set -euo pipefail
cd -- "$(dirname -- "$0")"
python3 scripts/build_report_index.py
if command -v latexmk >/dev/null 2>&1; then
  latexmk -xelatex -interaction=nonstopmode -halt-on-error main.tex
elif [[ -x /Library/TeX/texbin/latexmk ]]; then
  /Library/TeX/texbin/latexmk -xelatex -interaction=nonstopmode -halt-on-error main.tex
else
  echo '需要安装含 XeLaTeX、latexmk、ctex 和 Fandol 字体的 TeX Live / MacTeX。' >&2
  exit 1
fi
