import hashlib
import os


EXTENSION_TO_MIME = {
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".png": "image/png",
    ".gif": "image/gif",
    ".tif": "image/tiff",
    ".tiff": "image/tiff",
}


class MediumImage:
    def __init__(self, path: str):
        assert os.path.isfile(path), path
        _, ext = os.path.splitext(path)
        assert ext.lower() in EXTENSION_TO_MIME, path

        self.mime = EXTENSION_TO_MIME[ext.lower()]
        with open(path, "rb") as f:
            self.content = f.read()
        self.md5 = hashlib.md5(self.content).hexdigest()

        self.url = None
