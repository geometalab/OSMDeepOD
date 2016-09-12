import math


def meters_per_pixel(zoom, lat):
    return (math.cos(lat * math.pi / 180.0) * 2 * math.pi * 6378137) / (256 * 2 ** zoom)
