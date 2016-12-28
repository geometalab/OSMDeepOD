import configparser
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
    config = Configuration(dict(port=port))
    assert config.port == port


def test_config(configuration):
    config = configparser.ConfigParser()
    redis = 'REDIS'
    detection = 'DETECTION'
    port = 1991

    config.add_section(redis)
    config.add_section(detection)

    config.set(section=redis, option='Port', value=str(port))
    config.set(section=redis, option='Server', value='')
    config.set(section=redis, option='Password', value='')
    config.set(section=detection, option='Network', value='')
    config.set(section=detection, option='Labels', value='')

    configuration.set_from_config_parser(config)

    assert configuration.port == port


def test_barrier_constraints_high(configuration):
    barrier = 1.1
    assert not configuration.check_barrier_constraints(barrier)


def test_barrier_constraints_low(configuration):
    barrier = -1.0
    assert not configuration.check_barrier_constraints(barrier)


def test_barrier_constraints_correct(configuration):
    barrier = 0.5
    assert configuration.check_barrier_constraints(barrier)
