from src.base.node import Node
from src.data.generation.crosswalk_image import CrosswalkImage
from src.data.multi_loader import MultiLoader


def test_get_crosswalk_image_crop():
    node = Node(46.754588, 7.63048, 0)
    url = 'https://t1.ssl.ak.tiles.virtualearth.net/tiles/a1202212103103301000.jpeg?g=4401&n=z'
    urls = list()
    urls.append(url)

    loader = MultiLoader.from_url_list(urls)
    loader.download()
    images = loader.results

    crosswalk_image = CrosswalkImage(node=node, url=url)
    crosswalk_image.tile_image = images[0]
    image = crosswalk_image.crop_tile_image()
    width, height = image.size

    assert width == crosswalk_image._CROPPED_IMAGE_WIDTH
    assert height == crosswalk_image._CROPPED_IMAGE_HEIGHT


def test_build_box():
    node = Node(46.754588, 7.63048, 0)
    url = 'https://t1.ssl.ak.tiles.virtualearth.net/tiles/a1202212103103301000.jpeg?g=4401&n=z'
    px = 12
    py = 102

    crosswalk_image = CrosswalkImage(node=node, url=url)
    left, top, right, bottom = crosswalk_image._build_box(px, py)

    assert (right - left) == crosswalk_image._CROPPED_IMAGE_WIDTH
    assert (bottom - top) == crosswalk_image._CROPPED_IMAGE_HEIGHT


def test_build_filename():
    node = Node(46.754588, 7.63048, 0)
    url = 'https://t1.ssl.ak.tiles.virtualearth.net/tiles/a1202212103103301000.jpeg?g=4401&n=z'
    crosswalk_image = CrosswalkImage(node=node, url=url)

    filename = crosswalk_image._build_filename(url)

    assert filename == '1202212103103301000.png'
