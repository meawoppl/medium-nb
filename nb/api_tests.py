import nose.tools

import nb.api
import nb.api_testlib

import nb.post
import nb.post_testlib

import nb.image_tests


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
    img = nb.image_tests.load_test_image()
    user = nb.api_testlib.get_test_api()
    resp = user.upload_image("nb/testdata/16x16.png")
    import pprint
    pprint.pprint(resp)

    import base64
    print(base64.standard_b64decode(resp["md5"]))

    1/0
