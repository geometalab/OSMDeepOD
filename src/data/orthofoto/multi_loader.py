import logging
import time
from io import BytesIO
from multiprocessing.dummy import Pool as ThreadPool

import requests
from PIL import Image

from src.data.orthofoto.user_agent import UserAgent


class MultiLoader:
    def __init__(self, urls, auth=None):
        self.urls = urls
        self.results = []
        self.nb_threads = 10
        self.nb_tile_per_trial = 40
        self.auth = tuple() if auth is None else auth
        self.user_agent = UserAgent()
        self.logger = logging.getLogger(__name__)

    def download(self):
        results = []
        nb_urls = len(self.urls)
        for i in range(int(nb_urls / self.nb_tile_per_trial) + 1):
            start = i * self.nb_tile_per_trial
            end = start + self.nb_tile_per_trial
            if end >= nb_urls:
                end = nb_urls
            url_part = self.urls[start:end]

            result = self._try_download(url_part)
            results += result

        self.results = results

    def _try_download(self, urls):
        for i in range(4):
            try:
                results = self._download_async(urls)
                return results
            except Exception as e:
                print("Tile download failed " + str(i) + " wait " + str(i * 10) + "  " + str(e))
                time.sleep(i * 10)
        error_message = "Download of tiles have failed 4 times"
        self.logger.error(error_message)
        raise Exception(error_message)

    def _download_async(self, urls):
        pool = ThreadPool(self.nb_threads)
        results = pool.map(self._download_image, urls)
        pool.close()
        pool.join()
        return results

    def _download_image(self, url):
        response = requests.get(url, headers={'User-Agent': self.user_agent.random}, auth=self.auth)
        img = Image.open(BytesIO(response.content))
        img.filename = url
        return img
