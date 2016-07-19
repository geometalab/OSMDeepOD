from src.base.Bbox import Bbox
from src.data.crosswalk_collector import CrosswalkCollector


def zuerich_bellevue():
    return Bbox.from_lbrt(
            8.54279671719532,
            47.366177501999516,
            8.547088251618977,
            47.36781249586627
    )


def small_bbox():
    return Bbox.from_lbrt(
            8.8158524036,
            47.224907338,
            8.818745541,
            47.2256733959
    )


def bern():
    return Bbox.from_lbrt(
            7.4409936706,
            46.9441650631,
            7.4464679917,
            46.9461714321
    )


def thun():
    return Bbox.from_lbrt(
            7.6221979399,
            46.7533919504,
            7.6339494447,
            46.7626445727
    )


def test_get_crosswalks():
    crosswalk_collector = CrosswalkCollector(bbox=small_bbox())
    crosswalks = crosswalk_collector._get_crosswalk_nodes()
    assert len(crosswalks) != 0


def test_get_images():
    crosswalk_collector = CrosswalkCollector(bbox=small_bbox())
    images = crosswalk_collector._get_images()
    assert len(images) != 0


def test_run():
    crosswalk_collector = CrosswalkCollector(bbox=thun())
    crosswalk_collector.run()
    assert 0 == 0
