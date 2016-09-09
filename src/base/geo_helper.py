import math

from osgeo import osr
from osgeo import ogr


def meters_per_pixel(zoom, lat):
    return (math.cos(lat * math.pi / 180.0) * 2 * math.pi * 6378137) / (256 * 2 ** zoom)


def epsg4326_to_epsg21781(epsg4326_node):
    source = osr.SpatialReference()
    source.ImportFromEPSG(4326)

    target = osr.SpatialReference()
    target.ImportFromEPSG(21781)
    transform = osr.CoordinateTransformation(source, target)

    point = ogr.CreateGeometryFromWkt(
        "POINT( " + str(epsg4326_node.longitude) + " " + str(epsg4326_node.latitude) + " )")
    point.Transform(transform)

    print(point.ExportToWkt())
