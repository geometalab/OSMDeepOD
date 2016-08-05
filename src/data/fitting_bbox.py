from src.base.bbox import Bbox
from src.data.globalmaptiles import GlobalMercator


class FittingBbox:
    def __init__(self, bbox, zoom_level=19):
        self.bbox = bbox
        self._mercator = GlobalMercator()
        self._ZOOMLEVEL = zoom_level

    def get(self):
        t_minx, t_miny, t_maxx, t_maxy = self.bbox_to_tiles()
        bottom, left, top, right = self._mercator.TileLatLonBounds(t_minx, t_maxy, self._ZOOMLEVEL)
        return Bbox.from_lbrt(left, bottom, right, top)

    def bbox_to_tiles(self):
        m_minx, m_miny = self._mercator.LatLonToMeters(self.bbox.bottom, self.bbox.left)
        m_maxx, m_maxy = self._mercator.LatLonToMeters(self.bbox.top, self.bbox.right)
        t_maxx, t_maxy = self._mercator.MetersToTile(m_maxx, m_maxy, self._ZOOMLEVEL)
        t_minx, t_miny = self._mercator.MetersToTile(m_minx, m_miny, self._ZOOMLEVEL)
        return t_minx, t_miny, t_maxx, t_maxy
