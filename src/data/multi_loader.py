import time
import urllib.request

from multiprocessing.dummy import Pool as ThreadPool
from PIL import Image
from io import BytesIO
from random import choice

user_agents = [
    'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11',
    'Opera/9.25 (Windows NT 5.1; U; en)',
    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
    'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu)',
    'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.0.12) Gecko/20070731 Ubuntu/dapper-security Firefox/1.5.0.12',
    'Lynx/2.8.5rel.1 libwww-FM/2.14 SSL-MM/1.4.1 GNUTLS/1.2.9'
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
    'Opera/9.80 (X11; Linux i686; U; ru) Presto/2.8.131 Version/11.11'
    'Dalvik/2.1.0 (Linux; U; Android 6.0.1; Nexus Player Build/MMB29T)'
]


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
                print("-- " + str(int(new_percentage)) + "%")

    def _try_download(self, urls):
        for i in range(4):
            try:
                results = self._download_async(urls)
                return results
            except Exception as e:
                print("Tile download failed " + str(i) + " wait " + str(i * 10) + str(e))
                time.sleep(i * 10)
        raise Exception("Download of tiles have failed 4 times")

    def _download_async(self, urls):
        pool = ThreadPool(self.nb_threads)
        results = pool.map(_download_image, urls)
        pool.close()
        pool.join()
        return results


def _generate_request(url):
    header = {'User-Agent': choice(user_agents)}
    req = urllib.request.Request(url, headers=header)
    return req


def _download_image(url):
    req = _generate_request(url)
    response = urllib.request.urlopen(req)
    content = response.read()
    img = Image.open(BytesIO(content))
    img.filename = url
    return img
