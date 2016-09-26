import os
import environ
import logging
from io import BytesIO
from PIL import Image

from src.base import geo_helper
from src.data.orthofoto.wms.auth_monkey_patch import AuthMonkeyPatch
from requests_ntlm import HttpNtlmAuth


class WmsApi:
    def __init__(self, zoom_level=19):
        self.logger = logging.getLogger(__name__)
        self.current_directory = os.path.dirname(os.path.realpath(__file__))
        self.env = self._read_env()
        self.auth = self.set_auth()
        self.zoom_level = zoom_level

        self._auth_monkey_patch(self.auth)

        from owslib.wms import WebMapService
        self.wms = WebMapService(url=self.env('URL'), version=self.env('VERSION'))

    def set_auth(self):
        user = self.env('NTLM_USER')
        password = self.env('NTLM_PASSWORD')
        return HttpNtlmAuth(user, password) if user is not None and password is not None else None

    def _read_env(self):
        env = environ.Env(
            NTLM_USER=(str, None),
            NTLM_PASSWORD=(str, None),
            URL=(str, None),
            SRS=(str, None),
            VERSION=(str, None),
            LAYER=(str, None)
        )
        current = environ.Path(self.current_directory)
        environ.Env.read_env(current('.env'))
        self._settings_check(env)
        return env

    def _settings_check(self, env):
        if env('URL') is None or env('SRS') is None or env('VERSION') is None or env('LAYER') is None:
            error_message = "You have to set all URL, SRS, LAYER and VERSION in your .env config file."
            self.logger.error(error_message)
            raise Exception(error_message)

    @staticmethod
    def _auth_monkey_patch(auth):
        AuthMonkeyPatch(auth)

    def get_image(self, bbox):
        size = self._calculate_image_size(bbox, self.zoom_level)
        image = self._get(layers=[self.env('LAYER')],
                          srs=self.env('SRS'),
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
