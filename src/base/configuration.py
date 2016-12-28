import os
from src.base.tag import Tag


class Configuration:
    def __init__(self, parameters=None):
        if parameters is None: parameters = dict()
        self.word = parameters.get('word', 'crosswalk')
        self.tag = Tag(key=parameters.get('key', 'highway'), value=parameters.get('value', 'crossing'))
        self.zoom_level = parameters.get('zoom_level', 19)
        self.barrier = parameters.get('barrier', 0.99)
        self.compare = parameters.get('compare', True)
        self.orthophoto = parameters.get('orthophoto', 'other')
        self.network = parameters.get('network', '')
        self.labels = parameters.get('labels', '')
        self.step_width = parameters.get('StepWidth', 0.66)
        self.follow_streets = parameters.get('follow_street', True)
        self.bbox_size = float(parameters.get('bbox_size', 2000))
        self.timeout = parameters.get('timeout', 5400)
        self.server = parameters.get('server', '127.0.0.1')
        self.port = parameters.get('port', 40001)
        self.password = parameters.get('password', 'crosswalks')

    def set_from_config_parser(self, config):
        self.word = config.get(section='DETECTION', option='Word', fallback='crosswalk')
        self.tag = Tag(key=config.get(section='DETECTION', option='Key', fallback='highway'),
                       value=config.get(section='DETECTION', option='Value', fallback='crosswalk'))
        self.zoom_level = config.getint(section='DETECTION', option='ZoomLevel', fallback=19)
        self.compare = config.getboolean(section='DETECTION', option='Compare', fallback=True)
        self.orthophoto = config.get(section='DETECTION', option='Orthofoto', fallback='other')
        self.network = config.get(section='DETECTION', option='Network')
        self.labels = config.get(section='DETECTION', option='Labels')
        self.follow_streets = config.getboolean(section='DETECTION', option='FollowStreets', fallback=True)
        self.barrier = config.getfloat(section='DETECTION', option='DetectionBarrier', fallback=0.99)
        self.step_width = config.getfloat(section='DETECTION', option='StepWidth', fallback=0.66)
        self.bbox_size = config.getint(section='REDIS', option='BboxSize', fallback=2000)
        self.timeout = config.getint(section='REDIS', option='Timeout', fallback=5400)
        self.port = config.getint(section='REDIS', option='Port', fallback=40001)
        self.password = config.get(section='REDIS', option='Password', fallback='crosswalks')
        self.server = config.get(section='REDIS', option='Server', fallback='127.0.0.1')

    @staticmethod
    def check_redis_fields(config):
        if not config.has_section('REDIS'):
            raise Exception("Section 'REDIS' is not in config file!")
        if not config.has_option('REDIS', 'Server'):
            raise Exception("'server' not in 'REDIS' section!")
        if not config.has_option('REDIS', 'Password'):
            raise Exception("'password' not in 'REDIS' section!")
        if not config.has_option('REDIS', 'Port'):
            raise Exception("'port' not in 'REDIS' section!")

    @staticmethod
    def check_manager_config(config):
        if not config.has_section('DETECTION'): raise Exception(
            "Section 'DETECTION' is not in config file!")

        if not config.has_option('DETECTION', 'network'): raise Exception(
            "'network' not in 'DETECTION' section! ")
        network = config.get(section='DETECTION', option='network')
        if not os.path.isfile(network): raise Exception("The config file does not exist! " + network)

        labels = config.get(section='DETECTION', option='labels')
        if not config.has_option('DETECTION', 'labels'): raise Exception(
            "'labels' not in 'DETECTION' section! ")
        if not os.path.isfile(labels):
            raise Exception("The config file does not exist! " + labels)
