from src.data.StreetDrawer import StreetDrawer
from src.base.Bbox import Bbox
from src import cwenv

'''
Tool to visualize the streets which are loaded within a specific Bbox
'''

zurich_bellevue = Bbox.from_lbrt(
    8.54279671719532,
    47.366177501999516,
    8.547088251618977,
    47.36781249586627)
drawer = StreetDrawer.from_bbox(
    zurich_bellevue,
    apiKey=cwenv('MAPQUEST_API_KEY'))
drawer.show()
