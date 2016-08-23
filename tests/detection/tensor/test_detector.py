import os
import pytest
import numpy
from PIL import Image

from src.detection.tensor.detector import Detector


@pytest.fixture(scope="module")
def detector():
    return Detector()


def test_detector(detector):
    current_dir = os.path.dirname(__file__)
    crosswalk_image = Image.open(current_dir + '/img/crosswalk.jpg')
    non_crosswalk_image = Image.open(current_dir + '/img/non_crosswalk.jpg')

    results = detector.detect([crosswalk_image, non_crosswalk_image])

    assert results[0]['crosswalk'] > 0.9
    assert results[1]['noncrosswalk'] > 0.9


def test_detector_multiple_images(detector):
    current_dir = os.path.dirname(__file__)
    crosswalk_image = Image.open(current_dir + '/img/crosswalk.jpg')

    images = []
    image_count = 10
    for _ in range(image_count):
        images.append(crosswalk_image.copy())

    answers = detector.detect(images)

    assert len(answers) == image_count


def test_pil_to_tf(detector):
    image = Image.new("RGB", (512, 512), "white")
    np_arary = detector._pil_to_np(image)

    assert isinstance(np_arary, numpy.ndarray)
