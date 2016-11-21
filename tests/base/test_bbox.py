import pytest
import copy
from src.base.bbox import Bbox
from src.base.node import Node


@pytest.fixture(scope="module")
def rappi():
    return Bbox(left=8.81372, bottom=47.218788, right=8.852430, top=47.239654)


def test_instantiate():
    bottom = 47.0
    left = 8.0
    top = 48.0
    right = 9.0
    bbox = Bbox(bottom=bottom, left=left, top=top, right=right)

    assert bbox.bottom == bottom
    assert bbox.left == left
    assert bbox.top == top
    assert bbox.right == right


def test_instantiate_from_string():
    bottom = '47.0'
    left = '8.0'
    top = '48.0'
    right = '9.0'
    bbox = Bbox(bottom=bottom, left=left, top=top, right=right)

    assert bbox.bottom == bottom
    assert bbox.left == left
    assert bbox.top == top
    assert bbox.right == right


def test_in_bbox(rappi):
    bbox = rappi
    node = Node(47.22, 8.82)

    assert bbox.in_bbox(node)


def test_not_in_bbox(rappi):
    bbox = rappi
    node = Node(48.0, 8.8)
    assert not bbox.in_bbox(node)


def test_equal(rappi):
    rappi2 = copy.copy(rappi)
    assert rappi2 is not rappi
    assert rappi2 == rappi


def test_not_equal(rappi):
    bbox = Bbox()
    assert bbox is not rappi
    assert bbox != rappi
