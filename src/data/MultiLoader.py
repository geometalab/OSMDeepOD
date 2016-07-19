from multiprocessing.dummy import Pool as ThreadPool
import urllib2
import StringIO
from PIL import Image
from fake_useragent import UserAgent
import time


class MultiLoader(object):

    def __init__(self):
        self.urls = []
        self.results = []
        self.nb_threads = 10
        self.nb_tile_per_trial = 40
        self.verbose = True
        self._progress = 0

    @classmethod
    def from_url_list(cls, urls, verbose=True):
        loader = cls()
        loader.urls = urls
        loader.verbose = verbose
        return loader

    def download(self):
        results = []
        nb_urls = len(self.urls)
        for i in range(int(nb_urls / self.nb_tile_per_trial) + 1):
            start = i * self.nb_tile_per_trial
            end = start + self.nb_tile_per_trial
            if end >= nb_urls:
                end = nb_urls
            urlpart = self.urls[start:end]

            result = self._try_download(urlpart)
            results += result

            new_percentage = (float(end) / nb_urls) * 100
            self._set_progress(new_percentage)

        self.results = results

    def _set_progress(self, new_percentage):
        if self._progress + 5 < new_percentage:
            self._progress = new_percentage
            if self.verbose:
                print "-- " + str(int(new_percentage)) + "%"

    def _try_download(self, urls):
        for i in range(4):
            try:
                results = self._download_async(urls)
                return results
            except Exception as e:
                print "Tile download failed", i, "wait", i * 10, e
                time.sleep(i * 10)
        raise Exception("Download of tiles have failed 4 times " + str(e))

    def _download_async(self, urls):
        pool = ThreadPool(self.nb_threads)
        results = pool.map(_download_image, urls)
        pool.close()
        pool.join()
        return results


def _generate_request(url):
    header = {'User-Agent': UserAgent().random}
    req = urllib2.Request(url, headers=header)
    return req


def _download_image(url):
    request = _generate_request(url)
    response = urllib2.urlopen(request)
    content = response.read()
    img = Image.open(StringIO.StringIO(content))
    img.filename = url
    return img

