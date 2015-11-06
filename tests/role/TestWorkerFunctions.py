import unittest
import json
from src.role.WorkerFunctions import store
from src.base.Crosswalk import Crosswalk
from src.base.Constants import Constants

class TestWorkerFunctions(unittest.TestCase):

    def test_store(self):
        crosswalks = []
        crosswalks.append(Crosswalk(47.0, 8.0))
        crosswalks.append(Crosswalk(47.1, 8.1))
        store(crosswalks)
        with open(Constants.PATH_TO_CROSSWALKS, 'r') as f:
            data = json.load(f)
        print data