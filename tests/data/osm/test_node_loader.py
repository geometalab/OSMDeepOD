from src.data.osm.node_loader import NodeLoader


def test_load_streets(zurich_bellevue, crosswalk_tag):
    bbox = zurich_bellevue
    loader = NodeLoader()
    crosswalks = loader.load_data(bbox,crosswalk_tag)

    assert len(crosswalks) > 0
