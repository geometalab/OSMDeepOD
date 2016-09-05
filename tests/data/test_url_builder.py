import pytest
import urllib.request

from src.data.url_builder import UrlBuilder


@pytest.fixture(scope="module")
def url_builder():
    return UrlBuilder()


def test_url_from_node(node1, url_builder):
    url = url_builder.get_urls_by_tiles()
    assert url.endswith('ssl.ak.tiles.virtualearth.net/tiles/a1202212110112020212.jpeg?g=4401&n=z')


def test_url_reachable(node1, url_builder):
    url = url_builder.get_url_by_node(node1)
    req = urllib.request.Request(url)
    try:
        response = urllib.request.urlopen(req)
        content = response.read()
    except Exception:
        assert False
    assert content is not None
