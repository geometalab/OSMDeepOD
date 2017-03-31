import os
import pytest

from src.base.node import Node
from src.base.configuration import Configuration
from src.base.tag import Tag
from src.base.bbox import Bbox


@pytest.fixture(scope="session", autouse=True)
def small_bbox():
    return Bbox(left=8.54279671719532, bottom=47.366177501999516, right=8.543088251618977, top=47.36781249586627)


@pytest.fixture(scope="session", autouse=True)
def big_bbox():
    return Bbox(left=8.8, bottom=47.0, right=8.9, top=47.9)


@pytest.fixture(scope="session", autouse=True)
def zurich_bellevue():
    return Bbox(left=8.5448316112, bottom=47.3661604928, right=8.5453673825, top=47.366466604)


@pytest.fixture(scope="session", autouse=True)
def node1():
    return Node('47.0', '8.0', 10)


@pytest.fixture(scope="session", autouse=True)
def node2():
    return Node('47.1', '8.1', 10)


@pytest.fixture(scope="session", autouse=True)
def square_image_length():
    return 50


@pytest.fixture(scope="session", autouse=True)
def crosswalk_tag():
    return Tag(key='highway', value='crossing')


@pytest.fixture(scope="session", autouse=True)
def roundabout_tag():
    return Tag(key='junction', value='roundabout')


@pytest.fixture(scope="session", autouse=True)
def default_config():
    return Configuration(os.path.dirname(os.path.realpath(__file__)) + '/test_config.ini')


@pytest.fixture(scope="session", autouse=True)
def configuration_no_compare():
    configuration = Configuration(os.path.dirname(os.path.realpath(__file__)) + '/test_config.ini')
    configuration.DETECTION.compare = 'false'
    return configuration


@pytest.fixture(scope="session", autouse=True)
def store_path():
    file_path = os.path.join(os.getcwd(), 'detected_nodes.json')
    try:
        os.remove(file_path)
    except OSError:
        pass
    return file_path
