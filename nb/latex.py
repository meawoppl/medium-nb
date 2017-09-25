import os
import tempfile
import subprocess

LATEX_HEADER = r"""
\documentclass{article}
\usepackage{amsmath}

\begin{document}
\thispagestyle{empty}

  \begin{equation*}
"""

LATEX_FOOTER = r"""
  \end{equation*}
\end{document}
"""


def assert_call(*args):
    call_code = subprocess.check_call(args)
    assert call_code == 0, call_code


def assert_latex_exists():
    """
    TODO Package list:
    - texlive-extra-utils
    - texlive-latex-base
    """
    assert_call("pdflatex", "-version")
    assert_call("convert", "--version")
    assert_call("pdfcrop", "--version")


def render_in_tex(latex: str) -> bytes:
    """
    Render a latex equation into a minimal PNG
    graphic represented in bytes
    """
    assert_latex_exists()

    with tempfile.TemporaryDirectory() as td:
        latex_file = os.path.join(td, "base.tex")
        with open(latex_file, "w") as f:
            f.write(LATEX_HEADER)
            f.write(latex)
            f.write(LATEX_FOOTER)

        # NOTE GROSSSSS
        assert_call("pdflatex", "-output-directory", td, latex_file)
        pdf_file = os.path.join(td, "base.pdf")
        assert_call("pdfcrop", pdf_file, pdf_file)
        assert_call(
            "convert",
            "-density", "450",
            "-quality", "100",
            pdf_file,
            os.path.join(td, "base.png")
        )

        with open(os.path.join(td, "base.png"), "rb") as png:
            return png.read()
