from io import BytesIO
from PIL import Image

from src.base import geo_helper
from src.data.orthofoto.wms.auth_monkey_patch import AuthMonkeyPatch


class WmsApi:
    def __init__(self, zoom_level=19, url='', auth=None):
        self.url = url
        self.zoom_level = zoom_level
        self.srs = 'EPSG:4326'
        self.version = '1.1.0'
        self.auth = auth
        self._auth_monkey_patch(auth)

        from owslib.wms import WebMapService
        self.wms = WebMapService(url, version=self.version)

    @staticmethod
    def _auth_monkey_patch(auth):
        AuthMonkeyPatch(auth)

    def get_image(self, bbox):
        size = self._calculate_image_size(bbox, self.zoom_level)
        image = self._get(layers=['0'],
                          srs=self.srs,
                          bbox=self._box(bbox),
                          size=size,
                          format='image/jpeg',
                          )
        return image

    @staticmethod
    def _calculate_image_size(bbox, zoom_level):
        meters_per_pixel = geo_helper.meters_per_pixel(zoom_level, bbox.bottom)
        width_meter = bbox.node_left_down().get_distance_in_meter(bbox.node_right_down())
        height_meter = bbox.node_left_down().get_distance_in_meter(bbox.node_left_up())
        height = int(height_meter / meters_per_pixel)
        width = int(width_meter / meters_per_pixel)
        return width, height

    def _get(self, **kwargs):
        img = self.wms.getmap(**kwargs)
        return Image.open(BytesIO(img.read()))

    @staticmethod
    def _box(bbox):
        node_left_down = bbox.node_left_down()
        node_right_up = bbox.node_right_up()
        return node_left_down.longitude, node_left_down.latitude, node_right_up.longitude, node_right_up.latitude
