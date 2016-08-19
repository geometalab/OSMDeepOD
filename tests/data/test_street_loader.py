from src.data.street_crosswalk_loader import StreetCrosswalkLoader


def test_load_streets(zurich_bellevue):
    bbox = zurich_bellevue
    loader = StreetCrosswalkLoader()
    streets = loader.load_data(bbox)

    assert len(streets) > 50
    assert len(loader.crosswalks) > 16
    for street in streets:
        assert len(street.nodes) == 2
