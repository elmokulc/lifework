#!/bin/bash
eval "$(conda shell.bash hook)" && /
conda activate jupyter_book && /
jupyter-book clean book --all && /
jupyter-book build book && /
firefox ./book/_build/html/index.html &
