import pytest
import json
import os

from src.role.worker_functions import store, PATH_TO_CROSSWALKS
from src.base.node import Node


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


def test_store_in_two_steps_crosswalks():
    crosswalks = [Node(47.0, 8.0), Node(47.1, 8.1)]
    store(crosswalks)
    store(crosswalks)
    with open(PATH_TO_CROSSWALKS, 'r') as f:
        data = json.load(f)
    assert len(data['crosswalks']) == 4


def test_store_two_crosswalks():
    crosswalks = [Node(47.0, 8.0), Node(47.1, 8.1)]
    store(crosswalks)
    with open(PATH_TO_CROSSWALKS, 'r') as f:
        data = json.load(f)
    assert len(data['crosswalks']) == 2
