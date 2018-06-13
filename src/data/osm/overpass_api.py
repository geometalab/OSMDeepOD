import time
import logging
import overpass


class OverpassApi:
    def __init__(self):
        self.overpass = overpass.API(timeout=60)
        self.logger = logging.getLogger(__name__)

    def get(self, bbox, tags, nodes=True, ways=True, relations=True, responseformat='geojson'):
        query = self._get_query(bbox, tags, nodes, ways, relations)
        return self._try_overpass_download(query, responseformat)

    @staticmethod
    def _get_query(bbox, tags, nodes=True, ways=True, relations=True):
        bbox_string = '(' + str(bbox) + ');'
        query = '('
        for tag in tags:
            if nodes:
                query += 'node["' + tag.key + '"="' + tag.value + '"]' + bbox_string
            if ways:
                query += 'way["' + tag.key + '"="' + tag.value + '"]' + bbox_string
            if relations:
                query += 'relation["' + tag.key + '"="' + tag.value + '"]' + bbox_string
        query += ');'
        return query

    def _try_overpass_download(self, query, responseformat='geojson'):
        for i in range(4):
            try:
                json_data = self.overpass.get(query, responseformat=responseformat)
                return json_data
            except Exception as e:
                self.logger.warning(e)
                self.logger.warning("Download from overpass failed " + str(i) + " wait " + str(i * 10) + ".  " + str(e))
                time.sleep(i * 10)
        error_message = "Download from overpass failed 4 times."
        self.logger.error(error_message)
        raise Exception(error_message)
