import requests

import nb.post


class MediumUser:
    def __init__(self, api_key: str):
        self._key = api_key
        user_info = self._get_user_info()
        self.__dict__.update(user_info)

    def _do_authed_get(self, resource: str) -> dict:
        response = requests.get(
            resource,
            headers={"Authorization": "Bearer " + self._key}
        )
        assert response.status_code == 200, "Request failed: " + str(response.status_code)
        return response.json()["data"]

    def _get_user_info(self):
        return self._do_authed_get("https://api.medium.com/v1/me")

    def get_my_posts(self):
        return self._do_authed_get(
            "https://api.medium.com/v1/users/" + self.id + "/publications")

    def push_post(self, post: nb.post.Post):
        post.validate_post()
