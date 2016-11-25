import time
import logging
import overpass


class OverpassApi:
    def __init__(self):
        self.overpass = overpass.API(timeout=60)
        self.logger = logging.getLogger(__name__)

    def get(self, bbox, tags):
        query = self._get_query(bbox, tags)
        return self._try_overpass_download(query)

    @staticmethod
    def _get_query(bbox, tags):
        bbox_string = '(' + str(bbox) + ');'
        query = '('
        for tag in tags:
            node = 'node["' + tag.key + '"="' + tag.value + '"]' + bbox_string
            way = 'way["' + tag.key + '"="' + tag.value + '"]' + bbox_string
            relation = 'relation["' + tag.key + '"="' + tag.value + '"]' + bbox_string
            query += node + way + relation
        query += ');'
        return query

    def _try_overpass_download(self, query):
        for i in range(4):
            try:
                json_data = self.overpass.Get(query)
                return json_data
            except Exception as e:
                self.logger.warning("Download from overpass failed " + str(i) + " wait " + str(i * 10) + ".  " + str(e))
                time.sleep(i * 10)
        error_message = "Download from overpass failed 4 times."
        self.logger.error(error_message)
        raise Exception(error_message)
