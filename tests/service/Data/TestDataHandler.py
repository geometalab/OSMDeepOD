import unittest

from src.service.Data.DataHandler import DataHandler
from geopy import Point

class TestDataHandler(unittest.TestCase):

    def testInsert(self):
        point = Point(47.2, 8.81, 0)
        dataHandler = DataHandler()

        dataHandler.connect()
        dataHandler.insert(point, 1001)
        dataHandler.select()

