import os

import nb.api


def get_test_api():
    assert "MEDIUM_API_KEY" in os.environ
    api_key = os.environ["MEDIUM_API_KEY"]
    return nb.api.MediumUser(api_key)
