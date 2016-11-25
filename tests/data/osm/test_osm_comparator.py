import pytest

from src.base.bbox import Bbox
from src.base.node import Node
from src.data.osm.osm_comparator import OsmComparator


@pytest.fixture(scope="module", autouse=True)
def node():
    return Node(47.0912, 9.3470236659, 0)


@pytest.fixture(scope="module", autouse=True)
def roundabout_bbox():
    return Bbox(left=9.345857, bottom=47.090498, right=9.348325, top=47.092383)


def test_comparator(node, roundabout_bbox, roundabout_tag):
    comparator = OsmComparator(max_distance=29)
    nodes = comparator.compare([node], roundabout_bbox, roundabout_tag)
    assert len(nodes) == 0
