from src.detection.box_walker import BoxWalker
from src.base.bbox import Bbox
from src.base.node import Node
from src import cwenv


def small_bbox():
    return Bbox.from_lbrt(8.54279671719532, 47.366177501999516, 8.543088251618977, 47.36781249586627)


def zurich_bellevue():
    return Bbox.from_lbrt(8.54279671719532, 47.366177501999516, 8.547088251618977, 47.36781249586627)


def test_load_tile():
    walker = BoxWalker(
            small_bbox(),
            api_key=cwenv('MAPQUEST_API_KEY'),
            verbose=False)
    walker.load_tiles()
    assert walker.tile is not None


def test_load_streets():
    walker = BoxWalker(
            small_bbox(),
            api_key=cwenv('MAPQUEST_API_KEY'),
            verbose=False)
    walker.load_streets()
    assert walker.streets is not None


def test_walk():
    walker = BoxWalker(
            zurich_bellevue(),
            api_key=cwenv('MAPQUEST_API_KEY'),
            verbose=True)
    walker.load_convnet()
    walker.load_tiles()
    walker.load_streets()
    walker.walk()
    crosswalk_nodes = walker.plain_result
    assert crosswalk_nodes is not None
    assert len(crosswalk_nodes) > 0


def test_compare_detected_with_osm_same_points():
    walker = BoxWalker(
            small_bbox(),
            api_key=cwenv('MAPQUEST_API_KEY'),
            verbose=False)
    detected_crosswalks = [Node(47.0, 8.0), Node(47.1, 8.1)]
    walker.osm_crosswalks = detected_crosswalks
    result = walker._compare_osm_with_detected_crosswalks(detected_crosswalks)
    assert len(result) == 0


def test_compare_detected_with_osm_near_points():
    walker = BoxWalker(
            small_bbox(),
            api_key=cwenv('MAPQUEST_API_KEY'),
            verbose=False)
    detected_crosswalks = [
        Node(
                47.0, 8.0), Node(
                47.1, 8.1), Node(
                47.2, 8.2)]
    walker.osm_crosswalks = [
        Node(
                47.000001, 8.0), Node(
                47.100001, 8.1), Node(
                48.2, 8.2)]
    result = walker._compare_osm_with_detected_crosswalks(detected_crosswalks)
    assert len(result) == 1


def test_compare_detected_with_osm_different_points():
    walker = BoxWalker(
            small_bbox(),
            api_key=cwenv('MAPQUEST_API_KEY'),
            verbose=False)
    detected_crosswalks = [Node(47.0, 8.0), Node(47.1, 8.1)]
    walker.osm_crosswalks = [Node(48.0, 8.0), Node(48.1, 8.1)]
    result = walker._compare_osm_with_detected_crosswalks(detected_crosswalks)
    assert len(result) == 2
