from src.role.manager import Manager
from src.base.bbox import Bbox
from src.base.node import Node


def big_bbox():
    return Bbox.from_lbrt(8.8, 47.0, 8.9, 47.9)


def test():
    manager = Manager(bbox=big_bbox(), job_queue_name='dummy')
    columns = manager._calc_columns()
    rows = manager._calc_rows()
    assert rows > 40
    assert columns > 2


def test_with_two_columns():
    node1 = Node('47.0', '8.0', 10)
    node2 = node1.add_meter(200, Manager.SMALL_BBOX_SIDE_LENGHT + 50)
    manager = Manager(
            bbox=Bbox.from_leftdown_rightup(
                    node1,
                    node2),
            job_queue_name='dummy')
    columns = manager._calc_columns()
    rows = manager._calc_rows()
    assert rows == 1
    assert columns == 2


def test_first():
    node1 = Node('47.0', '8.0', 10)
    node2 = Node('47.1', '8.1', 10)
    manager = Manager(
            bbox=Bbox.from_leftdown_rightup(
                    node1,
                    node2),
            job_queue_name='dummy')
    manager._generate_small_bboxes()
    assert manager.small_bboxes[0].left == node1.longitude
    assert manager.small_bboxes[0].bottom == node1.latitude


def test_big_bbox():
    node1 = Node('47.0', '8.0', 10)
    node2 = Node('47.5', '8.5', 10)
    manager = Manager(
            bbox=Bbox.from_leftdown_rightup(
                    node1,
                    node2),
            job_queue_name='dummy')
    length = len(manager.small_bboxes)
    manager._generate_small_bboxes()
    assert manager.small_bboxes[0].left == node1.longitude
    assert manager.small_bboxes[0].bottom == node1.latitude
    assert (manager.small_bboxes[length - 1].right >= node2.longitude
            and manager.small_bboxes[length - 1].right <= node2.longitude + 0.05)
    assert (manager.small_bboxes[length -1].top >= node2.latitude
            and manager.small_bboxes[length - 1].top <= node2.latitude + 0.05)


def test_with_two():
    node1 = Node('47.0', '8.0', 10)
    node2 = node1.add_meter(Manager.SMALL_BBOX_SIDE_LENGHT + 50, Manager.SMALL_BBOX_SIDE_LENGHT + 50)
    manager = Manager(
            bbox=Bbox.from_leftdown_rightup(
                    node1,
                    node2),
            job_queue_name='dummy')
    columns = manager._calc_columns()
    rows = manager._calc_rows()
    assert rows == 2
    assert columns == 2


def test_with_three():
    node1 = Node('47.0', '8.0', 10)
    node2 = node1.add_meter(
            2 *
            Manager.SMALL_BBOX_SIDE_LENGHT +
            50,
            2 *
            Manager.SMALL_BBOX_SIDE_LENGHT +
            50)
    manager = Manager(
            bbox=Bbox.from_leftdown_rightup(
                    node1,
                    node2),
            job_queue_name='dummy')
    columns = manager._calc_columns()
    rows = manager._calc_rows()
    assert rows == 3
    assert columns == 3
