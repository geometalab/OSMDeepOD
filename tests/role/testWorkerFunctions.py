import unittest
import json
import os
from src.role.WorkerFunctions import store, PATH_TO_CROSSWALKS
from src.base.Node import Node


class TestWorkerFunctions(unittest.TestCase):

    def setUp(self):
        self.remove_file()

    def tearDown(self):
        self.remove_file()

    def test_store_zero_crosswalks(self):
        store([])
        with open(PATH_TO_CROSSWALKS, 'r') as f:
            data = json.load(f)
        self.assertTrue(len(data['crosswalks']) == 0)

    def test_store_in_two_steps_crosswalks(self):
        crosswalks = [Node(47.0, 8.0), Node(47.1, 8.1)]
        store(crosswalks)
        store(crosswalks)
        with open(PATH_TO_CROSSWALKS, 'r') as f:
            data = json.load(f)
        self.assertTrue(len(data['crosswalks']) == 4)

    def test_store_two_crosswalks(self):
        crosswalks = [Node(47.0, 8.0), Node(47.1, 8.1)]
        store(crosswalks)
        with open(PATH_TO_CROSSWALKS, 'r') as f:
            data = json.load(f)
        self.assertTrue(len(data['crosswalks']) == 2)

    @staticmethod
    def remove_file():
        if os.path.exists(PATH_TO_CROSSWALKS):
            os.remove(PATH_TO_CROSSWALKS)
