import nb.post


VALID_POST_INSTANCE = nb.post.Post(
    title="FooTitle",
    content="# FooTitle\nBodyText",
    contentFormat="markdown",
    canonicalUrl="http://foourl.com",
    tags=["footag1", "footag2"],
    publishStatus="draft",
)


def test_post_init_valid():
    nb.post_testlib.VALID_POST_INSTANCE.validate_post()

