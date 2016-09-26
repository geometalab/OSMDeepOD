from src.base import geo_helper


def test_meter_to_pixel(node1):
    meter_per_pixel = geo_helper.meters_per_pixel(19, node1.latitude)
    assert meter_per_pixel > 0
