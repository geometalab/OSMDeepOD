import os
from PIL import Image
from src.detection.tensor.detector import Detector


def test_detector():
    current_dir = os.path.dirname(__file__)
    crosswalk_image = Image.open(current_dir + '/img/crosswalk.jpg')
    non_crosswalk_image = Image.open(current_dir + '/img/non_crosswalk.jpg')

    detector = Detector()
    is_crosswalk = detector.detect(crosswalk_image)
    is_not_crosswalk = detector.detect(non_crosswalk_image)

    assert is_crosswalk['crosswalk'] > 0.9
    assert is_not_crosswalk['noncrosswalk'] > 0.9
