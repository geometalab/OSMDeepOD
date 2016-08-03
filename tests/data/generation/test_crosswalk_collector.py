from src.data.generation.crosswalk_collector import CrosswalkCollector


def test_get_crosswalks(zurich_bellevue):
    crosswalk_collector = CrosswalkCollector(bbox=zurich_bellevue)
    crosswalks = crosswalk_collector._get_crosswalk_nodes()
    assert len(crosswalks) != 0


def test_get_images(zurich_bellevue):
    crosswalk_collector = CrosswalkCollector(bbox=zurich_bellevue)
    crosswalks = crosswalk_collector._get_crosswalk_nodes()
    images = crosswalk_collector._get_cropped_images(crosswalks)
    assert len(images) != 0
