import pytest

from src.base.node import Node
from src.base.configuration import Configuration
from src.base.tag import Tag
from src.base.bbox import Bbox


@pytest.fixture(scope="session", autouse=True)
def small_bbox():
    return Bbox.from_lbrt(8.54279671719532, 47.366177501999516, 8.543088251618977, 47.36781249586627)


@pytest.fixture(scope="session", autouse=True)
def big_bbox():
    return Bbox.from_lbrt(8.8, 47.0, 8.9, 47.9)


@pytest.fixture(scope="session", autouse=True)
def zurich_bellevue():
    return Bbox.from_lbrt(8.5448316112, 47.3661604928, 8.5453673825, 47.366466604)


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
def configuration_no_compare():
    parameters = dict(compare=False)
    return Configuration(parameters=parameters)
