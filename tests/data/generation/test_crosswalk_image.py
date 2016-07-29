import pytest

from src.base.node import Node
from src.data.generation.crosswalk_image import CrosswalkImage
from src.data.multi_loader import MultiLoader


@pytest.fixture(scope="module")
def crosswalk_node():
    return Node(46.754588, 7.63048, 0)


@pytest.fixture(scope="module")
def crosswalk_url():
    return 'https://t1.ssl.ak.tiles.virtualearth.net/tiles/a1202212103103301000.jpeg?g=4401&n=z'


def test_get_crosswalk_image_crop(crosswalk_node, crosswalk_url):
    node = crosswalk_node
    url = crosswalk_url
    urls = list()
    urls.append(crosswalk_url)

    loader = MultiLoader.from_url_list(urls)
    loader.download()
    images = loader.results

    crosswalk_image = CrosswalkImage(node=node, url=url)
    crosswalk_image.tile_image = images[0]
    image = crosswalk_image.crop_tile_image()
    width, height = image.size

    assert width == crosswalk_image._CROPPED_IMAGE_WIDTH
    assert height == crosswalk_image._CROPPED_IMAGE_HEIGHT


def test_build_box(crosswalk_node, crosswalk_url):
    node = crosswalk_node
    url = crosswalk_url

    px = 12
    py = 102

    crosswalk_image = CrosswalkImage(node=node, url=url)
    left, top, right, bottom = crosswalk_image._build_box(px, py)

    assert (right - left) == crosswalk_image._CROPPED_IMAGE_WIDTH
    assert (bottom - top) == crosswalk_image._CROPPED_IMAGE_HEIGHT


def test_build_filename(crosswalk_node, crosswalk_url):
    node = crosswalk_node
    url = crosswalk_url

    crosswalk_image = CrosswalkImage(node=node, url=url)

    filename = crosswalk_image._build_filename(url)

    assert filename == '1202212103103301000.png'
