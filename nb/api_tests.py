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
    post = nb.post_testlib.get_valid_post_instance()

    user = nb.api_testlib.get_test_api()
    user.new_post(post)
    user.delete_post_unofficial(post.id)


# def test_update_post():
#     post = nb.post_testlib.get_valid_post_instance()
#     user = nb.api_testlib.get_test_api()
#     postid = user.new_post(post)
#     print(postid)
#     user.update_post(post)

def test_upload_image():
    import os
    test_image_path = os.path.join(os.path.dirname(nb.__file__), "testdata/16x16.png")
    user = nb.api_testlib.get_test_api()
    image_url, hash_like = user.upload_image(test_image_path)

    nose.tools.assert_is_instance(image_url, str)
    nose.tools.assert_in("https://", image_url)
    nose.tools.assert_is_instance(hash_like, str)


def test_do_it_all():
    import os
    test_md_path = os.path.join(
        os.path.dirname(nb.__file__),
        "example_testdata/posts/math-in-medium.md")

    user = nb.api_testlib.get_test_api()
    user.convert_upload_md(test_md_path)
