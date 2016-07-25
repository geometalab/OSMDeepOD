from src.base.bbox import Bbox
from src.base.node import Node


def rappi():
    return Bbox.from_lbrt(8.81372, 47.218788, 8.852430, 47.239654)


def test_instantiate_from_bltr():
    bottom = 47.0
    left = 8.0
    top = 48.0
    right = 9.0
    bbox = Bbox.from_bltr(bottom, left, top, right)

    assert bbox.bottom == bottom
    assert bbox.left == left
    assert bbox.top == top
    assert bbox.right == right


def test_instantiate_from_bltr_string():
    bottom = '47.0'
    left = '8.0'
    top = '48.0'
    right = '9.0'
    bbox = Bbox.from_bltr(bottom, left, top, right)

    assert bbox.bottom == bottom
    assert bbox.left == left
    assert bbox.top == top
    assert bbox.right == right


def test_in_bbox():
    bbox = rappi()
    node = Node(47.22, 8.82)

    assert bbox.in_bbox(node)


def test_not_in_bbox():
    bbox = rappi()
    node = Node(48.0, 8.8)
    assert bbox.in_bbox(node)
