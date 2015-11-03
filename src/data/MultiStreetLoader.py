import unittest
import overpy
from multiprocessing.dummy import Pool as ThreadPool
from src.base.Constants import Constants

class TestOverpy(unittest.TestCase):
    def __init__(self):
        self.querys = []
        self.ways = []
        self.api = overpy.Overpass()

    @classmethod
    def from_query_list(cls, querys):
        loader = cls()
        loader.querys = querys
        return loader

    def download(self):
        pool = ThreadPool(Constants.NUMBER_OF_THREADS)
        results = pool.map(self.query, self.querys)
        pool.close()
        pool.join()
        for result in results:
            for way in result.ways:
                self.ways.append(way)
        return self.ways

    def query(self,query):
        return self.api.query(query)


