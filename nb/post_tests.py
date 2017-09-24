import nose.tools

import nb.post


VALID_POST_INSTANCE = nb.post.Post(
    title="FooTitle",
    content="foo",
    contentFormat="markdown",
    canonicalUrl="http://foourl.com",
    tags=["footag1", "footag2"],
    publishStatus="draft",
)


def test_post_init_empty():
    nb.post.Post()


def test_post_init_invalid():
    with nose.tools.assert_raises(AssertionError):
        nb.post.Post().validate_post()

    with nose.tools.assert_raises(AssertionError):
        nb.post.Post(content="foo").validate_post()


def test_post_init_valid():
    VALID_POST_INSTANCE.validate_post()
