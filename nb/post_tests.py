import tempfile

import nose.tools

import nb.post
import nb.post_testlib


def test_post_init_empty():
    nb.post.Post()


def test_post_init_invalid():
    with nose.tools.assert_raises(AssertionError):
        nb.post.Post().validate_post()

    with nose.tools.assert_raises(AssertionError):
        nb.post.Post(content="foo").validate_post()


def test_post_folder_util():
    with tempfile.TemporaryDirectory() as td:
        with nose.tools.assert_raises(AssertionError):
            nb.post.Post.from_folder(td)

        nb.post_testlib.VALID_POST_INSTANCE.to_folder(td)
        post = nb.post.Post.from_folder(td)
        post.validate_post()
