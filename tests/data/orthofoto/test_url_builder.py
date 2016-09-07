import requests
import pytest

from src.data.orthofoto.fitting_bbox import FittingBbox
from src.data.orthofoto.url_builder import UrlBuilder


@pytest.fixture(scope='module')
def urls(small_bbox):
    url_builder = UrlBuilder()
    fitting_box = FittingBbox()
    t_minx, t_miny, t_maxx, t_maxy = fitting_box.bbox_to_tiles(small_bbox)
    return url_builder.get_urls_by_tiles(t_minx, t_miny, t_maxx, t_maxy)


def test_url_from_node(urls):
    assert 'ssl.ak.tiles.virtualearth.net/tiles/a' in urls[0]


def test_url_reachable(urls):
    try:
        response = requests.get(urls[0])
    except Exception:
        assert False
    assert response.content is not None
