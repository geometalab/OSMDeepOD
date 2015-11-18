import unittest
import json
import os
from src.role.WorkerFunctions import store
from src.base.Node import Node
from src.base.Constants import Constants

class TestWorkerFunctions(unittest.TestCase):

    def setUp(self):
        self.remove_file()

    def tearDown(self):
        self.remove_file()

    def test_store_zero_crosswalks(self):
        store([])
        with open(Constants.PATH_TO_CROSSWALKS, 'r') as f:
            data = json.load(f)
        self.assertTrue(len(data['crosswalks']) == 0);

    def test_store_in_two_steps_crosswalks(self):
        crosswalks = [Node(47.0, 8.0), Node(47.1, 8.1)]
        store(crosswalks)
        store(crosswalks)
        with open(Constants.PATH_TO_CROSSWALKS, 'r') as f:
            data = json.load(f)
        self.assertTrue(len(data['crosswalks']) == 4);


    def test_store_two_crosswalks(self):
        crosswalks = [Node(47.0, 8.0), Node(47.1, 8.1)]
        store(crosswalks)
        with open(Constants.PATH_TO_CROSSWALKS, 'r') as f:
            data = json.load(f)
        self.assertTrue(len(data['crosswalks']) == 2);

    def remove_file(self):
        if os.path.exists(Constants.PATH_TO_CROSSWALKS):
            os.remove(Constants.PATH_TO_CROSSWALKS)
