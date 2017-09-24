import nose.tools

import nb.api
import nb.api_testlib

import nb.post
import nb.post_testlib


def test_get_user_info():
    user = nb.api_testlib.get_test_api()

    nose.tools.assert_is_instance(user.id, str)
    nose.tools.assert_is_instance(user.name, str)
    nose.tools.assert_is_instance(user.username, str)
    nose.tools.assert_is_instance(user.url, str)
    nose.tools.assert_is_instance(user.imageUrl, str)


def test_get_my_posts():
    user = nb.api_testlib.get_test_api()

    posts = user.get_my_posts()
    nose.tools.assert_is_instance(posts, list)

    for post_json in posts:
        print(nb.post.Post.from_json(post_json))

def test_publish_post():
    user = nb.api_testlib.get_test_api()
    user.new_post(nb.post_testlib.VALID_POST_INSTANCE)
