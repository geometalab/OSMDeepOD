from src.data.street_drawer import StreetDrawer
from examples.zuerich_bellevue import zuerich_bellevue

'''
Tool to visualize the streets which are loaded within a specific Bbox
'''

drawer = StreetDrawer.from_bbox(zuerich_bellevue)
drawer.show()
