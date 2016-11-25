import json
from src.role.manager import Manager
from src.base.bbox import Bbox
from src.base.configuration import Configuration


def test(big_bbox):
    manager = Manager(bbox=big_bbox)
    columns = manager._calc_columns()
    rows = manager._calc_rows()
    assert rows > 40
    assert columns > 2


def test_with_two_columns(node1, configuration_no_compare):
    node2 = node1.add_meter(200, configuration_no_compare.bbox_size + 50)
    manager = Manager(bbox=Bbox.from_nodes(node_left_down=node1, node_right_up=node2))
    columns = manager._calc_columns()
    rows = manager._calc_rows()
    assert rows == 1
    assert columns == 2


def test_first(node1, node2):
    manager = Manager(bbox=Bbox.from_nodes(node_left_down=node1, node_right_up=node2))
    manager._generate_small_bboxes()
    assert manager.small_bboxes[0].left == node1.longitude
    assert manager.small_bboxes[0].bottom == node1.latitude


def test_big_bbox(node1, node2):
    manager = Manager(bbox=Bbox.from_nodes(node_left_down=node1, node_right_up=node2))
    length = len(manager.small_bboxes)
    manager._generate_small_bboxes()
    assert manager.small_bboxes[0].left == node1.longitude
    assert manager.small_bboxes[0].bottom == node1.latitude
    assert (manager.small_bboxes[length - 1].right >= node2.longitude
            and manager.small_bboxes[length - 1].right <= node2.longitude + 0.05)
    assert (manager.small_bboxes[length - 1].top >= node2.latitude
            and manager.small_bboxes[length - 1].top <= node2.latitude + 0.05)


def test_with_two(node1, configuration_no_compare):
    node2 = node1.add_meter(configuration_no_compare.bbox_size + 50, configuration_no_compare.bbox_size + 50)
    manager = Manager(bbox=Bbox.from_nodes(node_left_down=node1, node_right_up=node2))
    columns = manager._calc_columns()
    rows = manager._calc_rows()
    assert rows == 2
    assert columns == 2


def test_with_three(node1, configuration_no_compare):
    node2 = node1.add_meter(2 * configuration_no_compare.bbox_size + 50, 2 * configuration_no_compare.bbox_size + 50)
    manager = Manager(bbox=Bbox.from_nodes(node_left_down=node1, node_right_up=node2))
    columns = manager._calc_columns()
    rows = manager._calc_rows()
    assert rows == 3
    assert columns == 3


def test_manager_configuration(big_bbox):
    manager = Manager(bbox=big_bbox)
    assert manager.configuration is not None


def test_manager_standalone(store_path):
    small_bbox = Bbox(left=8.83848086, bottom=47.2218996495, right=8.8388215005, top=47.2220713398)
    manager = Manager(bbox=small_bbox, standalone=True, configuration=Configuration(dict(bbox_size=50, compare=False)))
    manager.run()
    with open(store_path, 'r') as f:
        data = json.load(f)
    assert len(data['nodes']) == 1
