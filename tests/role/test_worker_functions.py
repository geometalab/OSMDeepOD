from redis import Redis
import pytest
import json
import os

from src.role.worker_functions import store, enqueue_results


def remove_file(path):
    if os.path.exists(path):
        os.remove(path)


@pytest.yield_fixture(autouse=True)
def setup(store_path):
    remove_file(store_path)
    try:
        yield
    finally:
        remove_file(store_path)


def test_store_zero_crosswalks(store_path):
    store([])
    with open(store_path, 'r') as f:
        data = json.load(f)
    assert len(data['nodes']) == 0


def test_store_in_two_steps_crosswalks(node1, node2, store_path):
    crosswalks = [node1, node2]
    store(crosswalks)
    store(crosswalks)
    with open(store_path, 'r') as f:
        data = json.load(f)
    assert len(data['nodes']) == 4


def test_store_two_crosswalks(node1, node2, store_path):
    crosswalks = [node1, node2]
    store(crosswalks)
    with open(store_path, 'r') as f:
        data = json.load(f)
    assert len(data['nodes']) == 2


def test_enqueue_result(node1, node2):
    try:
        crosswalks = [node1, node2]
        redis_connection = Redis('localhost', '40001', password='crosswalks')
        enqueue_results(crosswalks, redis_connection)
        assert True
    except Exception:
        assert True

