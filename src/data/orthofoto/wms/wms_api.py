import os
import logging
import configparser
from io import BytesIO
from PIL import Image

from src.base import geo_helper
from src.base.globalmaptiles import GlobalMercator
from src.data.orthofoto.wms.auth_monkey_patch import AuthMonkeyPatch
from requests_ntlm import HttpNtlmAuth

logger = logging.getLogger(__name__)


class WmsApi:
    def __init__(self, zoom_level=19):
        self.config = self._read_wms_config()
        self.auth = self.set_auth()
        self.zoom_level = zoom_level
        self._auth_monkey_patch(self.auth)
        self.mercator = GlobalMercator()

        from owslib.wms import WebMapService
        self.wms = WebMapService(url=self.config.get(section='WMS', option='Url'),
                                 version=self.config.get(section='WMS', option='Version'))

    def set_auth(self):
        user = self.config.get(section='CREDENTIALS', option='NtlmUser', fallback=None)
        password = self.config.get(section='CREDENTIALS', option='NtlmPassword', fallback=None)
        return HttpNtlmAuth(user, password) if user is not None and password is not None else None

    def _read_wms_config(self):
        current_directory = os.path.dirname(os.path.abspath(__file__))
        config_file = os.path.join(current_directory, 'wms.ini')
        config = configparser.ConfigParser()
        if not os.path.isfile(config_file):
            raise Exception("The WMS config file does not exist! " + config_file)
        config.read(config_file)
        self.check_wms_config_fields(config)
        return config

    @staticmethod
    def _auth_monkey_patch(auth):
        AuthMonkeyPatch(auth)

    def get_image(self, bbox):
        bbox_ = self._box(bbox)
        bbox_ = self.mercator.LatLonToMeters(bbox_[3], bbox_[0]) + self.mercator.LatLonToMeters(bbox_[1], bbox_[2])
        size = self._calculate_image_size(bbox, self.zoom_level)
        image = self._get(layers=[self.config.get(section='WMS', option='Layer')],
                          srs=self.config.get(section='WMS', option='Srs'),
                          bbox=bbox_,
                          size=size,
                          format='image/jpeg',
                          )
        return image

    def get_image_size(self, bbox):
        return self._calculate_image_size(bbox, self.zoom_level)

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

    @staticmethod
    def check_wms_config_fields(config):
        if not config.has_section('WMS'):
            raise Exception("Section 'WMS' is not in WMS config file!")
        if not config.has_option('WMS', 'Url'):
            raise Exception("'Url' is not in 'WMS' section!")
        if not config.has_option('WMS', 'Srs'):
            raise Exception("'Srs' is not in 'WMS' section!")
        if not config.has_option('WMS', 'Version'):
            raise Exception("'Version' is not in 'WMS' section!")
        if not config.has_option('WMS', 'Layer'):
            raise Exception("'Layer' is not in 'WMS' section!")
