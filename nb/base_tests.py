import os
import tempfile

import nb.base


def test_is_nb_folder_valid():
    this_directory = os.path.dirname(nb.base.__file__)
    testdir = os.path.join(this_directory, "example_testdata")
    valid, reason = nb.base.is_nb_folder(testdir)
    assert valid, reason


def test_is_nb_folder_invalid():
    valid, reason = nb.base.is_nb_folder("foo")
    assert not valid, reason

    with tempfile.TemporaryDirectory() as td:
        valid, reason = nb.base.is_nb_folder(td)
        assert not valid, reason

