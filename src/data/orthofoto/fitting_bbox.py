from src.base.bbox import Bbox
from src.base.globalmaptiles import GlobalMercator


class FittingBbox:
    def __init__(self, zoom_level=19):
        self._mercator = GlobalMercator()
        self._zoom_level = zoom_level

    def get(self, bbox):
        t_minx, t_miny, t_maxx, t_maxy = self.bbox_to_tiles(bbox)
        bbox = self._bbox_from(t_minx, t_miny, t_maxx, t_maxy)
        return bbox

    def bbox_to_tiles(self, bbox):
        m_minx, m_miny = self._mercator.LatLonToMeters(bbox.bottom, bbox.left)
        m_maxx, m_maxy = self._mercator.LatLonToMeters(bbox.top, bbox.right)
        t_maxx, t_maxy = self._mercator.MetersToTile(m_maxx, m_maxy, self._zoom_level)
        t_minx, t_miny = self._mercator.MetersToTile(m_minx, m_miny, self._zoom_level)
        return t_minx, t_miny, t_maxx, t_maxy

    def generate_bbox(self, tx, ty):
        bottom, left, top, right = self._mercator.TileLatLonBounds(tx, ty, self._zoom_level)
        bbox = Bbox.from_lbrt(left, bottom, right, top)
        return bbox

    def _bbox_from(self, t_minx, t_miny, t_maxx, t_maxy):
        bottom, left, _, _ = self._mercator.TileLatLonBounds(t_minx, t_miny, self._zoom_level)
        _, _, top, right = self._mercator.TileLatLonBounds(t_maxx, t_maxy, self._zoom_level)
        return Bbox.from_lbrt(left, bottom, right, top)
