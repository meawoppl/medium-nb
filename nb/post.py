import os
import json

METADATA_FILENAME = "meta.json"
CONTENT_FILENAME = "content.md"


def is_valid_post_folder(path: str) -> tuple:
    if not os.path.exists(path):
        return False, "Does not exist:" + path
    if not os.path.isdir(path):
        return False, "Is not a directory: " + path

    meta_path = os.path.join(path, METADATA_FILENAME)
    if not os.path.isfile(meta_path):
        return False, "Missing metadata: " + meta_path

    content_path = os.path.join(path, CONTENT_FILENAME)
    if not os.path.isfile(content_path):
        return False, "Missing content: " + content_path

    return True, "OK"


def assert_is_valid_post_folder(path: str):
    valid, reason = is_valid_post_folder(path)
    assert valid, reason


class Post:
    VALID_PUBLISH_STATUS = ("public","draft","unlisted")
    VALID_CONTENT_FORMAT = ("markdown", "html")

    def __init__(          # NOQA
            self,
            title=None,
            content=None,
            canonicalUrl=None,
            tags=None,
            publishStatus=None,
            contentFormat="markdown"):

        # We only support markdown for now
        assert contentFormat == "markdown", contentFormat
        # NB: non-PEP8 names consistant with JSON request fmt for sanity
        self.title = title
        self.contentFormat = contentFormat
        self.content = content
        self.canonicalUrl = canonicalUrl
        self.tags = tags
        self.publishStatus = publishStatus

    @staticmethod
    def _get_folder_paths(path: str):
        assert os.path.isdir(path), path
        meta_path = os.path.join(path, METADATA_FILENAME)
        cont_path = os.path.join(path, CONTENT_FILENAME)
        return meta_path, cont_path

    def to_folder(self, path: str):
        self.validate_post()
        meta_json = self.to_post_json()
        content = meta_json.pop("content")

        meta_path, cont_path = self._get_folder_paths(path)

        with open(meta_path, "w") as f:
            json.dump(meta_json, f)

        with open(cont_path, "w") as f:
            f.write(content)

    @classmethod
    def from_folder(cls, path: str):
        assert_is_valid_post_folder(path)

        meta_path, cont_path = cls._get_folder_paths(path)
        with open(meta_path) as f:
            meta = json.load(f)

        with open(cont_path) as f:
            meta["content"] = f.read()
        return cls(**meta)

    @classmethod
    def from_post_json(cls, json: dict):
        return cls(
            json["title"],
            json["contentFormat"],
            json["content"],
            json["canonicalUrl"],
            json["tags"],
            json["publishStatus"],
        )

    def to_post_json(self):
        ret = dict(
            title=self.title,
            contentFormat=self.contentFormat,
            content=self.content,
            publishStatus=self.publishStatus,
        )
        # Optinal fields
        if self.canonicalUrl is not None:
            ret["canonicalUrl"] = self.canonicalUrl
        if self.tags is not None:
            ret["tags"] = self.tags
        return ret

    def validate_post(self):
        assert self.title is not None
        assert self.contentFormat in self.VALID_CONTENT_FORMAT, self.contentFormat
        assert self.content is not None
        assert self.tags is not None
        for tag in self.tags:
            assert isinstance(tag, str)
        assert len(self.tags) < 3
        assert self.publishStatus in self.VALID_PUBLISH_STATUS, self.publishStatus
