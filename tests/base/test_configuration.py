import pytest
from src.base.configuration import Configuration


@pytest.fixture(scope="function", autouse=True)
def configuration():
    return Configuration()


def test_default_values(configuration):
    assert configuration.port == 40001
    assert configuration.server == '127.0.0.1'
    assert configuration.password == 'crosswalks'
    assert configuration.word == 'crosswalk'
    assert configuration.compare
    assert configuration.barrier == 0.99
    assert configuration.timeout == 5400
    assert configuration.follow_streets


def test_parameter():
    port = 1991
    configuration = Configuration(dict(port=port))
    assert configuration.port == port


def test_config(configuration):
    port = 1991
    redis_port = dict(Port=port)
    config = {'REDIS': redis_port}

    configuration.set_from_config_parser(config)

    assert configuration.port == port
