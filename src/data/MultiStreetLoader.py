import unittest
import overpy
from multiprocessing.dummy import Pool as ThreadPool

class MultiStreetLoader(unittest.TestCase):
    def __init__(self):
        self.queries = []
        self.ways = []
        self.api = overpy.Overpass()

    @classmethod
    def from_query_list(cls, queries):
        loader = cls()
        loader.queries = queries
        return loader

    def download(self):
        pool = ThreadPool(len(self.queries))
        results = pool.map(self._get_ways, self.queries)
        pool.close()
        pool.join()
        for result in results:
            for way in result.ways:
                self.ways.append(way)
        return self.ways

    def _get_ways(self,query):
        return self.api.query(query)


