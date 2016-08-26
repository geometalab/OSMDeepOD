import pytest

from src.base.node import Node
from src.base.bbox import Bbox


@pytest.fixture(scope="session", autouse=True)
def small_bbox():
    return Bbox.from_lbrt(8.54279671719532, 47.366177501999516, 8.543088251618977, 47.36781249586627)


@pytest.fixture(scope="session", autouse=True)
def big_bbox():
    return Bbox.from_lbrt(8.8, 47.0, 8.9, 47.9)


@pytest.fixture(scope="session", autouse=True)
def zurich_bellevue():
    return Bbox.from_lbrt(8.54279671719532, 47.366177501999516, 8.547088251618977, 47.36781249586627)


@pytest.fixture(scope="session", autouse=True)
def node1():
    return Node('47.0', '8.0', 10)


@pytest.fixture(scope="session", autouse=True)
def node2():
    return Node('47.1', '8.1', 10)


@pytest.fixture(scope="session", autouse=True)
def step_distance():
    return 18


@pytest.fixture(scope="session", autouse=True)
def square_image_length():
    return 50

