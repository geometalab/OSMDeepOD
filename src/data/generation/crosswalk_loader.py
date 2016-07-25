import time
import overpass

from src.base.node import Node


class CrosswalkLoader:
    def __init__(self):
        self.overpass = overpass.API(timeout=60)

    def get_crosswalk_nodes(self, bbox):
        overpass_bbox = self._bbox_to_overpass(bbox)
        json_crosswalks = self._try_overpass_download(overpass_bbox)
        nodes = self._json_to_nodes(json_crosswalks)
        return nodes

    def _bbox_to_overpass(self, bbox):
        return str(bbox.bottom) + ',' + str(bbox.left) + ',' + str(bbox.top) + ',' + str(bbox.right)

    def _try_overpass_download(self, overpass_bbox):
        for i in range(4):
            try:
                query = 'node[highway=crossing](' + overpass_bbox + ')'
                json_crosswalks = self.overpass.Get(query)
                return json_crosswalks
            except Exception as e:
                print("Download of crosswalks from overpass failed " + str(i) + " wait " + str(i * 10) + str(e))
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
