import nb.post


def get_valid_post_instance():
    return nb.post.Post(
        title="FooTitle",
        content="# FooTitle\nBodyText",
        contentFormat="markdown",
        canonicalUrl="http://foourl.com",
        tags=["footag1", "footag2"],
        publishStatus="draft",
    )


def test_post_init_valid():
    get_valid_post_instance().validate_post()

