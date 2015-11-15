from multiprocessing.dummy import Pool as ThreadPool
import urllib2
import StringIO
from PIL import Image
from fake_useragent import UserAgent
import time

class MultiLoader:
    def __init__(self):
        self.urls = []
        self.results = []
        self.nb_threads = 5
        self.nb_tile_per_trial = 20
        self.useragent = UserAgent()


    @classmethod
    def from_url_list(cls, urls):
        loader = cls()
        loader.urls = urls
        return loader

    def generate_request(self, url):
        header ={'User-Agent': self.useragent.random}
        req = urllib2.Request(url, headers=header)
        return req

    def download(self):
        results = []
        nb_urls = len(self.urls)
        percentage = 0
        for i in range(int(nb_urls/self.nb_tile_per_trial)+1):
            start = i * self.nb_tile_per_trial
            end = start + self.nb_tile_per_trial
            if(end >= nb_urls): end = nb_urls
            urlpart = self.urls[start:end]

            result = self._try_download(urlpart)
            results += result
            newpercentage = (float(end)/nb_urls) * 100
            if(percentage + 5 < newpercentage):
                #time.sleep(7)
                percentage = newpercentage
                print "-- " + str(int(percentage)) + "%"

        self.results = self._convert_to_image(results)

    def _try_download(self, requests):
        for i in range(3):
            try:
                results = self._download(requests)
                return results
            except:
                pass
        raise Exception("Download of tiles have failed 4 times...")

    def _download(self, urls):
        pool = ThreadPool(self.nb_threads)
        results = pool.map(urllib2.urlopen, urls)
        pool.close()
        pool.join()
        return results

    def _convert_to_image(self, results):
        ret = []
        for loads in results:
            img = loads.read()
            img = Image.open(StringIO.StringIO(img))
            ret.append(img)

        return ret