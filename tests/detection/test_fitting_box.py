from src.data.fitting_bbox import FittingBbox


def test_fitting_bbox(small_bbox):
    fitting_bbox = FittingBbox(small_bbox)
    new_bbox = fitting_bbox.get()

    assert new_bbox.left != small_bbox.left
