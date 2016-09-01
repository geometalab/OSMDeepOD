from src.data.fitting_bbox import FittingBbox


def test_fitting_bbox(small_bbox):
    fitting_bbox = FittingBbox()
    new_bbox = fitting_bbox.get(bbox=small_bbox)

    assert new_bbox.left != small_bbox.left
