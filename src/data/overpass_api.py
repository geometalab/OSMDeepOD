import time
import logging
import overpass

from src.base.street import Street
from src.base.node import Node

logger = logging.getLogger(__name__)

class OverpassApi:
    def __init__(self, street_categories):
        self.overpass = overpass.API(timeout=60)
        self.crosswalks = []
        self.streets = []
        self.street_categories = street_categories

    def load_data(self, bbox):
        self._load_data(bbox)
        return self.streets

    def _load_data(self, bbox):
        query = self._get_query(bbox)
        json_data = self._try_overpass_download(query)
        self._set_data(json_data)

    def _get_query(self, bbox):
        bbox = '(' + self._bbox_to_overpass(bbox) + ');'
        query = '('
        for category in self.street_categories:
            node = 'node["highway"="' + category + '"]' + bbox
            way = 'way["highway"="' + category + '"]' + bbox
            relation = 'relation["highway"="' + category + '"]' + bbox
            query += node + way + relation
        crosswalks = 'node["highway"="crossing"]' + bbox
        query += crosswalks + ');'
        return query

    def _bbox_to_overpass(self, bbox):
        return str(bbox.bottom) + ',' + str(bbox.left) + ',' + str(bbox.top) + ',' + str(bbox.right)

    def _try_overpass_download(self, query):
        for i in range(4):
            try:
                json_data = self.overpass.Get(query)
                return json_data
            except Exception as e:
                logger.warning("Download of streets from overpass failed " + str(i) + " wait " + str(i * 10) + str(e))
                time.sleep(i * 10)
        error_message = "Download of streets from overpass failed 4 times."
        logger.error(error_message)
        raise Exception(error_message)

    def _set_data(self, json_data):
        for feature in json_data['features']:
            if feature['properties']['highway'] == 'crossing':
                self._set_crosswalk(feature)
            else:
                self._set_street(feature)

    def _set_crosswalk(self, feature):
        osm_id = feature['id']
        coordinates = feature['geometry']['coordinates']
        crosswalk = Node(coordinates[1], coordinates[0], osm_id)
        self.crosswalks.append(crosswalk)

    def _set_street(self, feature):
        highway = feature['properties']['highway']
        osm_id = feature['id']
        if self._has_name(feature):
            name = feature['properties']['name']
        else:
            name = 'unknown'
        coordinates = feature['geometry']['coordinates']
        for i in range(len(coordinates)-1):
            street = Street.from_info(name, osm_id, highway)
            start_node = Node(coordinates[i][1], coordinates[i][0])
            end_node = Node(coordinates[i + 1][1], coordinates[i + 1][0])
            street.nodes.append(start_node)
            street.nodes.append(end_node)
            self.streets.append(street)

    def _has_name(self, feature):
        return 'name' in feature['properties']
