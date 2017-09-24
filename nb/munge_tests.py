import tempfile
import os

import nose.tools

import nb.munge


def test_load_content_file_simple():
    file_contents = "foo\nbar\nbaz\n"
    with tempfile.TemporaryDirectory() as td:
        md_file = os.path.join(td, "test.md")
        with open(md_file, "w") as f:
            f.write(file_contents)

        content, eqs = nb.munge.load_content_file(md_file)

        nose.tools.assert_equal(content, file_contents)
        nose.tools.assert_dict_equal(eqs, {})


def test_load_content_file_equation():
    file_contents = "foo\nbar\n$\na=1\n$\n"
    with tempfile.TemporaryDirectory() as td:
        md_file = os.path.join(td, "test.md")
        with open(md_file, "w") as f:
            f.write(file_contents)

        content, eqs = nb.munge.load_content_file(md_file)

        nose.tools.assert_in("EQUATION_PLACEHOLDER_0", content)
        nose.tools.assert_dict_equal(eqs, {0:"a=1"})
