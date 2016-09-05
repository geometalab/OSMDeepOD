import pytest
from src.data.multi_loader import MultiLoader


@pytest.fixture(scope='module')
def urls():
    return ['https://t5.ssl.ak.tiles.virtualearth.net/tiles/a1202211220212011302.jpeg?g=4401&n=z',
            'https://t2.ssl.ak.tiles.virtualearth.net/tiles/a1202211220212011303.jpeg?g=4401&n=z']


def test_multi_loader(urls):
    multi_loader = MultiLoader(urls=urls)
    multi_loader.download()
    assert 2 == len(multi_loader.results)
