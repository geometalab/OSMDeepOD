import overpass
import time
import re
import os

from src.base.Node import Node
from src.data.MultiLoader import MultiLoader
from src.data.url_builder import UrlBuilder
from src.data.globalmaptiles import GlobalMercator
from src.detection.deep.Convnet import Convnet


class CrosswalkCollector:
    def __init__(self, bbox=None, timeout=30):
        self._ZOOMLEVEL = 19
        self.overpass = overpass.API(timeout=timeout)
        self.bbox = bbox

    def run(self):
        images = self._get_images()
        crosswalk_images = self._detect_crosswalks(images)
        self._store(crosswalk_images)

    def _get_images(self):
        nodes = self._get_crosswalk_nodes()
        url_builder = UrlBuilder()
        urls_and_nodes = url_builder.get_urls_by_nodes(nodes)
        urls = [url[0] for url in urls_and_nodes]
        if not urls:
            return None
        loader = MultiLoader.from_url_list(urls)
        loader.download()
        images = loader.results
        matches = self._match_image_to_node(images, urls_and_nodes)
        cut_images = self._get_cut_images(matches)
        return cut_images

    def _get_crosswalk_nodes(self):
        overpass_bbox = self._bbox_to_overpass()
        json_crosswalks = self._try_overpass_download(overpass_bbox)
        nodes = self._json_to_nodes(json_crosswalks)
        return nodes

    def _try_overpass_download(self, overpass_bbox):
        for i in range(4):
            try:
                json_crosswalks = self.overpass.Get('node[highway=crossing](' + overpass_bbox + ')')
                return json_crosswalks
            except Exception as e:
                print "Download of crosswalks from overpass failed", i, "wait", i * 10, e
                time.sleep(i * 10)
        raise Exception("Download of crosswalks from overpass failed 4 times " + str(e))

    def _json_to_nodes(self, json):
        nodes = []
        for feature in json['features']:
            coordinates = feature['geometry']['coordinates']
            osm_id = feature['id']
            node = Node(coordinates[1], coordinates[0], osm_id)
            nodes.append(node)
        return nodes

    def _bbox_to_overpass(self):
        return str(self.bbox.bottom) + ',' + str(self.bbox.left) + ',' + str(self.bbox.top) + ',' + str(self.bbox.right)

    def _match_image_to_node(self, images, urls_and_nodes):
        matches = []
        for i in range(len(urls_and_nodes)):
            match = dict(url=urls_and_nodes[i][0], node=urls_and_nodes[i][1])
            for image in images:
                if image.filename == urls_and_nodes[i][0]:
                    match['image'] = image
            matches.append(match)
        return matches

    def _get_cut_images(self, matches):
        matches = self._set_pixel_position_of_crosswalks(matches)
        images = []
        for match in matches:
            box = self._build_box(match['pixel_crosswalk_x'], match['pixel_crosswalk_y'])
            if self._is_on_image(box):
                image = match['image'].crop(box)
                image.filename = self._build_filename(match['image'].filename)
                if self._image_has_the_right_size(image):
                    images.append(image)
        return images

    def _set_pixel_position_of_crosswalks(self, matches):
        mercator = GlobalMercator()
        for match in matches:
            meter_crosswalk_x, meter_crosswalk_y = mercator.LatLonToMeters(match['node'].latitude,
                                                                           match['node'].longitude)
            tile_x, tile_y = mercator.MetersToTile(meter_crosswalk_x, meter_crosswalk_y, self._ZOOMLEVEL)
            lat_bottom, lon_left, _, _ = mercator.TileLatLonBounds(tile_x, tile_y, self._ZOOMLEVEL)
            meter_left_x, meter_bottom_y = mercator.LatLonToMeters(lat_bottom, lon_left)
            pixel_crosswalk_x, pixel_crosswalk_y = mercator.MetersToPixels(meter_crosswalk_x, meter_crosswalk_y,
                                                                           self._ZOOMLEVEL)
            pixel_left_x, pixel_bottom_y = mercator.MetersToPixels(meter_left_x, meter_bottom_y, self._ZOOMLEVEL)
            match['pixel_crosswalk_x'] = pixel_crosswalk_x - pixel_left_x
            match['pixel_crosswalk_y'] = 255 - (pixel_crosswalk_y - pixel_bottom_y)
        return matches

    def _is_on_image(self, box):
        return box[0] >= 0 and box[1] >= 0 and box[2] <= 255 and box[3] <= 255

    def _image_has_the_right_size(self, image):
        width, height = image.size
        return width == 50 and height == 50

    def _build_box(self, px, py):
        left = int(px - 25)
        top = int(py - 25)
        right = int(px + 25)
        bottom = int(py + 25)
        return (left, top, right, bottom)

    def _detect_crosswalks(self, images):
        convnet = Convnet.from_verbose(False)
        convnet.initialize()
        convnet.threshold = 0.01  # The current convnet is very bad outside of zuerich, so I changed the threshold
        predictions = convnet.predict_crosswalks(images)
        detected_crosswalks = []
        for i in range(len(predictions)):
            if predictions[i]:
                detected_crosswalks.append(images[i])
        return detected_crosswalks

    def _store(self, images):
        cwd = os.path.dirname(os.path.realpath(__file__))
        for image in images:
            image.save(cwd + '/img/' + image.filename)

    def _build_filename(self, filename):
        filename = re.sub(r"^https://t..ssl.ak.tiles.virtualearth.net/tiles/a*", '', filename)
        filename = re.sub(r".jpeg\?g=4401&n=z", '', filename)
        return filename + '.png'
