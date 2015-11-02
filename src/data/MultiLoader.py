from multiprocessing.dummy import Pool as ThreadPool
import urllib2
import StringIO
from PIL import Image
from src.base.Constants import Constants

class MultiLoader:
    def __init__(self):
        self.urls = []
        self.results = []

    @classmethod
    def from_url_list(cls, urls):
        loader = cls()
        loader.urls = urls
        return loader

    def download(self):
        pool = ThreadPool(Constants.NUMBER_OF_THREADS)
        results = pool.map(urllib2.urlopen, self.urls)
        pool.close()
        pool.join()

        self.results = self._convert_to_image(results)

    def _convert_to_image(self, results):
        ret = []
        for loads in results:
            img = loads.read()
            img = Image.open(StringIO.StringIO(img))
            ret.append(img)

        return ret