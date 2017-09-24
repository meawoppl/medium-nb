import json
import os
import pprint


def is_nb_folder(path: str) -> tuple:
    """
    Return True if "path" appears to be medium
    markdown notebook folder
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
    assert len(obj) == 1 and "api_key" in obj, pprint.pfortmat(obj)


class MediumNotebook:
    def __init__(self, nb_root: str):
        assert_is_nb_folder(nb_root)
        self._root = nb_root
