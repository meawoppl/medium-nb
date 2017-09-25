import json
import os
import pprint

import nb.post


def is_nb_folder(path: str) -> tuple:
    """
    Return True if "path" appears to be medium
    markdown notebook folder this includes:
     - validation of folder structure
     - load of credentials
     - structure of post folders
    """
    if not os.path.exists(path):
        return False, "Not a path: " + path
    if not os.path.isdir(path):
        return False, "Not a folder: " + path

    credentials_path = os.path.join(path, "config.json")

    try:
        load_credentials(credentials_path)
    except Exception as e:
        print(str(e))
        return False, "Invalid credentials file: " + str(e)

    posts_folder = os.path.join(path, "posts")
    if not os.path.isdir(posts_folder):
        return False, "No posts folder at: " + posts_folder

    for post_name in os.listdir(posts_folder):
        post_dir = os.path.join(posts_folder, post_name)
        post_valid, reason = nb.post.is_valid_post_folder(post_dir)

        if not post_valid:
            return False, "Post " + post_dir + " seems invalid " + reason

    return True, "Appears valid"


def assert_is_nb_folder(path: str):
    """
    Like is_nb_folder(), but raises an
    AssertionError if "path" is not a
    notebook folder
    """
    valid, reason = is_nb_folder(path)
    assert valid, reason


def load_credentials(path: str) -> str:
    """
    Load the credentials from the notebook folder root
    """
    with open(path) as f:
        obj = json.load(f)
    assert len(obj) == 1 and "api_key" in obj, pprint.pformat(obj)


def save_post_meta(path: str, post_id: str):
    with open(path, "w") as f:
        json.dump(f, {"id": post_id})


class MediumNotebook:
    def __init__(self, nb_root: str, medium_api):
        assert_is_nb_folder(nb_root)
        self._root = nb_root
        self._api

    def init_new_post(self, fs_name: str):
        new_folder = os.path.join(self._root, "posts", fs_name)
        assert not os.path.exists(new_folder)

