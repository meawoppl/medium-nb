import pprint
import tempfile
import time
import os

import requests

import nb.post
import nb.munge

EXTENSION_TO_MIME = {
    ".png": "image/png",
    ".jpeg": "image/jpeg",
    ".jpg": "image/jpeg",
    ".tiff": "image/tiff",
    ".tif": "image/tiff",
}


def filename_to_mime(filename: str) -> str:
    _, extension = os.path.splitext(filename)
    assert extension.lower() in EXTENSION_TO_MIME, extension
    return EXTENSION_TO_MIME[extension.lower()]


class MediumUser:
    def __init__(self, api_key: str):
        self._key = api_key
        user_info = self._get_user_info()
        self.__dict__.update(user_info)

    def assert_response(self, response, expected_code: int=200):
        if response.status_code != expected_code:
            formatted_message = \
                "Response Failed! Code: {} Expected: {}\n" \
                "Response-Headers:\n{}\n Repsonse-Body:\n{}\n".format(
                    response.status_code, expected_code,
                    pprint.pformat(dict(response.headers.items())),
                    response.raw.read()
                )
            raise AssertionError(formatted_message)

        return response.json()["data"]

    def _do_authed_get(self, resource: str) -> dict:
        response = requests.get(
            resource,
            headers={"Authorization": "Bearer " + self._key}
        )
        return self.assert_response(response)

    def _do_authed_put(self, resource: str, json):
        response = requests.post(
            resource,
            headers={"Authorization": "Bearer " + self._key},
            json=json
        )
        return self.assert_response(response, expected_code=201)

    def _get_user_info(self):
        return self._do_authed_get("https://api.medium.com/v1/me")

    def get_my_posts(self):
        return self._do_authed_get(
            "https://api.medium.com/v1/users/" + self.id + "/publications")

    def new_post(self, post: nb.post.Post):
        """
        This creates a new post on the Medium website
        it ruturns the post's id feild and additionally
        sets it on the post object passed in.

        Posts if a post has an existing .id it will raise
        an AssertionError.  To update a post use update_post()
        """
        post.validate_post()
        posting_response_json = self._do_authed_put(
            "https://api.medium.com/v1/users/" + self.id + "/posts",
            post.to_json()
        )
        post.id = posting_response_json["id"]
        return post.id

    def delete_post(self, postid: str):
        raise NotImplementedError("Medium does not implement?!?!?")

        path = "/p/" + postid
        response = requests.delete(
            "https://medium.com" + path,
            headers={
                "Authorization": "Bearer " + self._key,
                "path": path,
                "referer": "https://medium.com/me/stories/drafts"
            },
        )
        self.assert_response(response, 200)

    def update_post(self, post: nb.post.Post):
        raise NotImplementedError("Medium does not implement?!?!?")

        posting_json = post.to_json()
        posting_json["id"] = post.id
        response = requests.post(
            "https://api.medium.com/v1/users/" + self.id + "/posts",
            headers={"Authorization": "Bearer " + self._key},
            json=posting_json
        )
        self.assert_response(response)

    def upload_image(self, filepath: str) -> tuple:
        """
        Upload the file found at "filepath", return a 2-tuple with:
         - Medium image url
         - Medium image "md5" hash.
        """
        mime = filename_to_mime(filepath)
        with open(filepath, "rb") as f:
            response = requests.post(
                "https://api.medium.com/v1/images",
                headers={
                    "Authorization": "Bearer " + self._key,
                },
                files={
                    "image": (filepath, f, mime)
                }
            )
        resp = self.assert_response(response, 201)
        return resp["url"], resp["md5"]

    def upload_image_bytes(self, image: bytes, filename: str):
        with tempfile.TemporaryDirectory() as td:
            img_temp = os.path.join(td, filename)
            with open(img_temp, "wb") as f:
                f.write(image)

            return self.upload_image(img_temp)

    def convert_upload_md(self, file: str):
        content, equations = nb.munge.load_content_file(file)

        # Convert equations -> png and upload
        medium_links = {}
        for number, eq in equations.items():
            png_data = nb.latex.render_in_tex(eq)
            url, _ = self.upload_image_bytes(png_data, "equation_" + str(number) + ".png")
            medium_links[number] = url

        # Replace document links with medium ones
        replaced_content = nb.munge.replace_content_placeholders(content, medium_links)
        p = nb.post.Post(
            title="MediumMathSync:" + time.ctime(),
            content=replaced_content,
            contentFormat="markdown",
            canonicalUrl="https://github.com/meawoppl/medium-nb",
            tags=[],
            publishStatus="draft",
        )

        self.new_post(p)
