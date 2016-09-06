from io import BytesIO
from PIL import Image

from src.data.orthofoto.wms.auth_monkey_patch import AuthMonkeyPatch


class WmsApi:
    def __init__(self, url='', version='1.1.0', auth=None):
        self.url = url
        self.auth = auth
        self.version = version
        self._auth_monkey_patch(auth)

        from owslib.wms import WebMapService
        self.wms = WebMapService(url, version=version)

    @staticmethod
    def _auth_monkey_patch(auth):
        AuthMonkeyPatch(auth)

    def get(self, **kwargs):
        img = self.wms.getmap(**kwargs)
        return Image.open(BytesIO(img.read()))
