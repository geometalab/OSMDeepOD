from src.data.street_crosswalk_loader import StreetCrosswalkLoader
from src.base.bbox import Bbox
from src import cwenv


def zurich_bellevue():
    return Bbox.from_lbrt(8.54279671719532, 47.366177501999516, 8.547088251618977, 47.36781249586627)


def test_load_streets():
    bbox = zurich_bellevue()
    loader = StreetCrosswalkLoader(api_key=cwenv('MAPQUEST_API_KEY'))
    streets = loader.load_data(bbox)

    assert len(streets) > 50
    assert len(loader.crosswalks) > 16
    for street in streets:
        assert len(street.nodes) == 2
