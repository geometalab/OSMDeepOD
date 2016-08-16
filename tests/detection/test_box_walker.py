from src.detection.box_walker import BoxWalker
from src.base.node import Node


def test_load_tile(small_bbox):
    walker = BoxWalker(small_bbox)
    walker.load_tiles()
    assert walker.tile is not None


def test_load_streets(small_bbox):
    walker = BoxWalker(small_bbox)
    walker.load_streets()
    assert walker.streets is not None


def test_walk(zurich_bellevue):
    walker = BoxWalker(zurich_bellevue)
    walker.load_convnet()
    walker.load_tiles()
    walker.load_streets()
    walker.walk()
    crosswalk_nodes = walker.plain_result
    assert crosswalk_nodes is not None
    assert len(crosswalk_nodes) > 0


def test_compare_detected_with_osm_same_points(small_bbox, node1, node2):
    walker = BoxWalker(small_bbox)
    detected_crosswalks = [node1, node2]
    walker.osm_crosswalks = detected_crosswalks
    result = walker._compare_osm_with_detected_crosswalks(detected_crosswalks)
    assert len(result) == 0


def test_compare_detected_with_osm_near_points(small_bbox):
    walker = BoxWalker(small_bbox)
    detected_crosswalks = [Node(47.0, 8.0), Node(47.1, 8.1), Node(47.2, 8.2)]
    walker.osm_crosswalks = [Node(47.000001, 8.0), Node(47.100001, 8.1), Node(48.2, 8.2)]
    result = walker._compare_osm_with_detected_crosswalks(detected_crosswalks)
    assert len(result) == 1


def test_compare_detected_with_osm_different_points(small_bbox):
    walker = BoxWalker(small_bbox)
    detected_crosswalks = [Node(47.0, 8.0), Node(47.1, 8.1)]
    walker.osm_crosswalks = [Node(48.0, 8.0), Node(48.1, 8.1)]
    result = walker._compare_osm_with_detected_crosswalks(detected_crosswalks)
    assert len(result) == 2
