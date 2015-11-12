from setuptools import setup

setup(
    name = "OSM-Crosswalk-Detection",
    version = "0.0.1",
    author = "Buehler Severin and Kurath Samuel",
    description = "Crosswalk detection on orthofotos.",
    license = "MIT",
    keywords = "crosswalk detection",
    url = "https://github.com/geometalab/OSM-Crosswalk-Detection",
    packages=['src', 'src.base', 'src.data', 'src.detection', 'src.detection.deep', 'src.role'],
    install_requires = ['rq', 'geopy', 'pillow', 'fake_useragent', 'httplib2'],
    classifiers = [],
)
