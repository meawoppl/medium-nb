import os

import nose.tools

import nb
import nb.image


def load_test_image():
    img_path = os.path.join(os.path.dirname(nb.__file__), "testdata/16x16.png")
    return nb.image.MediumImage(img_path)


def test_image_basic():
    mi = load_test_image()
    nose.tools.assert_is_instance(mi.md5, str)
    nose.tools.assert_is_instance(mi.content, bytes)
