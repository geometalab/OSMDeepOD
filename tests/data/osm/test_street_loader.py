from src.data.osm.street_loader import StreetLoader


def test_load_streets(zurich_bellevue):
    bbox = zurich_bellevue
    loader = StreetLoader()
    streets = loader.load_data(bbox)

    assert len(streets) > 0
