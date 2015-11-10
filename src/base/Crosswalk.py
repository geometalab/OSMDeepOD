from geopy import Point

class Crosswalk(Point):
    def __init__(self, lat = 0.0, lon = 0.0, osm_street_id = 0):
        super(self.__class__, self).__init__(lat, lon)
        self.osm_street_id = osm_street_id

