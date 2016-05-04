import os
import codecs
import re
from setuptools import setup
from pip.req import parse_requirements

package = 'src'


here = os.path.abspath(os.path.dirname(__file__))
with codecs.open(os.path.join(here, package, '__init__.py'),
                 encoding='utf8') as version_file:
    metadata = dict(
        re.findall(
            r"""__([a-z]+)__ = "([^"]+)""",
            version_file.read()))


def get_packages(package):
    """
    Return root package and all sub-packages.
    """
    return [dirpath
            for dirpath, _, _ in os.walk(package)
            if os.path.exists(os.path.join(dirpath, '__init__.py'))]


def get_requirements():
    requirements_file_path = os.path.join(
        os.path.dirname(__file__),
        'requires.dev.txt')
    if os.path.exists(requirements_file_path):
        parsed_requirements = parse_requirements(
            requirements_file_path,
            session=False)
        requirements = [str(ir.req) for ir in parsed_requirements]
    else:
        requirements = []
    return requirements


setup(
    name="OSM-Crosswalk-Detection",
    version=metadata['version'],
    author="Buehler Severin and Kurath Samuel",
    maintainer="Marcel Huber",
    maintainer_email="marcel.huber@hsr.ch",
    description="Crosswalk detection on orthofotos.",
    license="MIT",
    keywords=['crosswalk detection'],
    url="https://github.com/geometalab/OSM-Crosswalk-Detection",
    packages=get_packages(package),
    install_requires=get_requirements(),
    setup_requires=[],
    test_suite='tests',
    tests_require=[],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Topic :: Scientific/Engineering :: GIS",
        "Topic :: Scientific/Engineering :: Image Recognition",
        "Topic :: Scientific/Engineering :: Visualization"],
)
