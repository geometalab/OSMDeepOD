import json
from src.role.manager import Manager
from src.base.bbox import Bbox
from src.base.configuration import Configuration


def test(big_bbox, default_config):
    manager = Manager(bbox=big_bbox, configuration=default_config)
    columns = manager._calc_columns()
    rows = manager._calc_rows()
    assert rows > 40
    assert columns > 2


def test_with_two_columns(node1, configuration_no_compare):
    node2 = node1.add_meter(200, int(configuration_no_compare.JOB.bboxsize) + 50)
    manager = Manager(bbox=Bbox.from_nodes(node_left_down=node1, node_right_up=node2),
                      configuration=configuration_no_compare)
    columns = manager._calc_columns()
    rows = manager._calc_rows()
    assert rows == 1
    assert columns == 2


def test_first(node1, node2, default_config):
    manager = Manager(bbox=Bbox.from_nodes(node_left_down=node1, node_right_up=node2), configuration=default_config)
    manager._generate_small_bboxes()
    assert manager.small_bboxes[0].left == node1.longitude
    assert manager.small_bboxes[0].bottom == node1.latitude


def test_big_bbox(node1, node2, default_config):
    manager = Manager(bbox=Bbox.from_nodes(node_left_down=node1, node_right_up=node2), configuration=default_config)
    length = len(manager.small_bboxes)
    manager._generate_small_bboxes()
    assert manager.small_bboxes[0].left == node1.longitude
    assert manager.small_bboxes[0].bottom == node1.latitude
    assert (manager.small_bboxes[length - 1].right >= node2.longitude
            and manager.small_bboxes[length - 1].right <= node2.longitude + 0.05)
    assert (manager.small_bboxes[length - 1].top >= node2.latitude
            and manager.small_bboxes[length - 1].top <= node2.latitude + 0.05)


def test_with_two(node1, configuration_no_compare):
    bbox_size = int(configuration_no_compare.JOB.bboxsize)
    node2 = node1.add_meter(bbox_size + 50, bbox_size + 50)
    manager = Manager(bbox=Bbox.from_nodes(node_left_down=node1, node_right_up=node2),
                      configuration=configuration_no_compare)
    columns = manager._calc_columns()
    rows = manager._calc_rows()
    assert rows == 2
    assert columns == 2


def test_with_three(node1, configuration_no_compare):
    bbox_size = int(configuration_no_compare.JOB.bboxsize)
    node2 = node1.add_meter(2 * bbox_size + 50, 2 * bbox_size + 50)
    manager = Manager(bbox=Bbox.from_nodes(node_left_down=node1, node_right_up=node2),
                      configuration=configuration_no_compare)
    columns = manager._calc_columns()
    rows = manager._calc_rows()
    assert rows == 3
    assert columns == 3


def test_manager_standalone(store_path, configuration_no_compare):
    small_bbox = Bbox(left=9.351172, bottom=47.098195, right=9.351301, top=47.098480)
    configuration_no_compare.DETECTION.bboxsize = 50
    manager = Manager(bbox=small_bbox, standalone=True, configuration=configuration_no_compare)

    manager.run()
    with open(store_path, 'r') as f:
        data = json.load(f)
    assert len(data['nodes']) == 1
