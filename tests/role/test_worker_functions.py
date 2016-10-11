from redis import Redis
import pytest
import json
import os

from src.role.worker_functions import store, enqueue_results, PATH_TO_CROSSWALKS


def remove_file():
    if os.path.exists(PATH_TO_CROSSWALKS):
        os.remove(PATH_TO_CROSSWALKS)


@pytest.yield_fixture(autouse=True)
def setup():
    remove_file()
    try:
        yield
    finally:
        remove_file()


def test_store_zero_crosswalks():
    store([])
    with open(PATH_TO_CROSSWALKS, 'r') as f:
        data = json.load(f)
    assert len(data['crosswalks']) == 0


def test_store_in_two_steps_crosswalks(node1, node2):
    crosswalks = [node1, node2]
    store(crosswalks)
    store(crosswalks)
    with open(PATH_TO_CROSSWALKS, 'r') as f:
        data = json.load(f)
    assert len(data['crosswalks']) == 4


def test_store_two_crosswalks(node1, node2):
    crosswalks = [node1, node2]
    store(crosswalks)
    with open(PATH_TO_CROSSWALKS, 'r') as f:
        data = json.load(f)
    assert len(data['crosswalks']) == 2


def test_enqueue_result(node1, node2):
        crosswalks = [node1, node2]
        redis_connection = Redis('localhost', '40001', password='crosswalks')
        enqueue_results(crosswalks, redis_connection)
