import nose.tools

import nb.latex


def test_latex_trivial():
    nb.latex.render_in_tex("a=1")


def test_latex_harder():
    nb.latex.render_in_tex(r"a_2=1^{\inf}")


def test_latex_trivial_dump():
    result = nb.latex.render_in_tex("a=1")

    nose.tools.assert_is_instance(result, bytes)
    with open("local.png", "wb") as f:
        f.write(result)
