import time
import urllib.request
import logging

from multiprocessing.dummy import Pool as ThreadPool
from PIL import Image
from io import BytesIO

from src.data.user_agent import UserAgent

class MultiLoader(object):
    def __init__(self):
        self.urls = []
        self.results = []
        self.nb_threads = 10
        self.nb_tile_per_trial = 40
        self.verbose = True
        self._progress = 0
        self.logger = logging.getLogger(__name__)

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

            new_percentage = 0.0
            if nb_urls > 0:
                new_percentage = (float(end) / nb_urls) * 100

            self._set_progress(new_percentage)

        self.results = results

    def _set_progress(self, new_percentage):
        if self._progress + 5 < new_percentage:
            self._progress = new_percentage
            if self.verbose:
                print("-- " + str(int(new_percentage)) + "%")

    def _try_download(self, urls):
        for i in range(4):
            try:
                results = self._download_async(urls)
                return results
            except Exception as e:
                print("Tile download failed " + str(i) + " wait " + str(i * 10) + str(e))
                time.sleep(i * 10)
        error_message = "Download of tiles have failed 4 times"
        self.logger.error(error_message)
        raise Exception(error_message)

    def _download_async(self, urls):
        pool = ThreadPool(self.nb_threads)
        results = pool.map(_download_image, urls)
        pool.close()
        pool.join()
        return results


def _generate_request(url):
    user_agent = UserAgent()
    header = {'User-Agent': user_agent.random}
    req = urllib.request.Request(url, headers=header)
    return req


def _download_image(url):
    req = _generate_request(url)
    response = urllib.request.urlopen(req)
    content = response.read()
    img = Image.open(BytesIO(content))
    img.filename = url
    return img
