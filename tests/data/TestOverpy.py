import unittest
import overpy
from multiprocessing.dummy import Pool as ThreadPool
from src.base.Constants import Constants

class TestOverpy(unittest.TestCase):

    def test(self):
        api = overpy.Overpass()
        querys = []
        querys.append("""
            [out:json];
            (
              node["highway"="primary"](47.366177501999516,8.54279671719532,47.36781249586627,8.547088251618977);
              way["highway"="primary"](47.366177501999516,8.54279671719532,47.36781249586627,8.547088251618977);
              relation["highway"="primary"](47.366177501999516,8.54279671719532,47.36781249586627,8.547088251618977);
            );
            out body;
            >;
            out skel qt;
            """)

        querys.append("""
            [out:json];
            (
              node["highway"="pedestrian"](47.366177501999516,8.54279671719532,47.36781249586627,8.547088251618977);
              way["highway"="pedestrian"](47.366177501999516,8.54279671719532,47.36781249586627,8.547088251618977);
              relation["highway"="pedestrian"](47.366177501999516,8.54279671719532,47.36781249586627,8.547088251618977);
            );
            out body;
            >;
            out skel qt;
            """)

        results = self.download(querys)
        for result in results:
            for way in result.ways:
                print("Name: %s" % way.tags.get("name", "n/a"))
                print("  Highway: %s" % way.tags.get("highway", "n/a"))
                print("  Nodes:")
                for node in way.nodes:
                    print("    Lat: %f, Lon: %f" % (node.lat, node.lon))



    def download(self, querys):
        pool = ThreadPool(Constants.NUMBER_OF_THREADS)
        results = pool.map(self.query, querys)
        pool.close()
        pool.join()
        return results

    def query(self,query):
        api = overpy.Overpass()
        return api.query(query)


