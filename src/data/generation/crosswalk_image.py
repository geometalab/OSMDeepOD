import re

from src.data.globalmaptiles import GlobalMercator


class CrosswalkImage(object):
    def __init__(self, node=None, url=None):
        self._ZOOMLEVEL = 19
        self._CROPPED_IMAGE_HEIGHT = 50
        self._CROPPED_IMAGE_WIDTH = 50
        self._node = node
        self._url = url
        self._tile_image = None
        self._crosswalk_image = None
        self._position_px, self._position_py = self._get_pixel_position_of_crosswalks()

    def crop_tile_image(self):
        box = self._build_box(self._position_px, self._position_py)
        if self._is_on_image(box, self._tile_image):
            image = self._tile_image.crop(box)
            image.filename = self._build_filename(self._tile_image.filename)
            if self._image_has_the_right_size(image):
                self._crosswalk_image = image
                return image
        return None

    def _get_pixel_position_of_crosswalks(self):
        mercator = GlobalMercator()
        meter_crosswalk_x, meter_crosswalk_y = mercator.LatLonToMeters(self._node.latitude, self._node.longitude)
        tile_x, tile_y = mercator.MetersToTile(meter_crosswalk_x, meter_crosswalk_y, self._ZOOMLEVEL)
        lat_bottom, lon_left, _, _ = mercator.TileLatLonBounds(tile_x, tile_y, self._ZOOMLEVEL)
        meter_left_x, meter_bottom_y = mercator.LatLonToMeters(lat_bottom, lon_left)
        pixel_x, pixel_y = mercator.MetersToPixels(meter_crosswalk_x, meter_crosswalk_y, self._ZOOMLEVEL)
        pixel_left_x, pixel_bottom_y = mercator.MetersToPixels(meter_left_x, meter_bottom_y, self._ZOOMLEVEL)
        return (pixel_x - pixel_left_x), (255 - (pixel_y - pixel_bottom_y))

    @staticmethod
    def _is_on_image(box, image):
        width, height = image.size
        return box[0] >= 0 and box[1] >= 0 and box[2] <= width and box[3] <= height

    def _image_has_the_right_size(self, image):
        width, height = image.size
        return width == self._CROPPED_IMAGE_WIDTH and height == self._CROPPED_IMAGE_HEIGHT

    def _build_box(self, px, py):
        left = int(px - self._CROPPED_IMAGE_WIDTH / 2)
        top = int(py - self._CROPPED_IMAGE_HEIGHT / 2)
        right = int(px + self._CROPPED_IMAGE_WIDTH / 2)
        bottom = int(py + self._CROPPED_IMAGE_HEIGHT / 2)
        return left, top, right, bottom

    @staticmethod
    def _build_filename(filename):
        filename = re.sub(r"^https://t..ssl.ak.tiles.virtualearth.net/tiles/a*", '', filename)
        filename = re.sub(r".jpeg\?g=4401&n=z", '', filename)
        return filename + '.png'

    @property
    def node(self):
        return self._node

    @property
    def url(self):
        return self._url

    @property
    def tile_image(self):
        return self._tile_image

    @tile_image.setter
    def tile_image(self, value):
        self._tile_image = value

    @property
    def crosswalk_image(self):
        return self._crosswalk_image

    @property
    def position_px(self):
        return self._position_px

    @property
    def position_py(self):
        return self._position_py
