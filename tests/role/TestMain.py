import unittest
import src.role.main

class TestMain(unittest.TestCase):

    def test(self):
        bbox = self.Rappi()
        manager = Manager(bbox)


    def ZurichBellvue(self):
        return Bbox(8.54279671719532, 47.366177501999516, 8.547088251618977, 47.36781249586627)

    def Luzern(self):
        return Bbox(8.301307, 47.046349, 8.305528, 47.051053)

    def Rappi(self):
        return Bbox(8.81372, 47.218788, 8.852430, 47.239654)