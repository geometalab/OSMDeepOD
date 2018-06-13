import os
import configparser


class Configuration:
    def __init__(self, config_file_path=''):
        config_parser = self.read_configuration_file(config_file_path)
        sections = [
            {'section': 'REDIS', 'options': [{'option': 'server', 'fallback': '127.0.0.1'},
                                             {'option': 'port', 'fallback': '40001'},
                                             {'option': 'password', 'fallback': 'crosswalks'}]},
            {'section': 'DETECTION', 'options': [{'option': 'network', 'fallback': ''},
                                                 {'option': 'labels', 'fallback': ''},
                                                 {'option': 'barrier', 'fallback': '0.99'},
                                                 {'option': 'word', 'fallback': 'crosswalk'},
                                                 {'option': 'key', 'fallback': 'highway'},
                                                 {'option': 'value', 'fallback': 'crossing'},
                                                 {'option': 'zoomlevel', 'fallback': '19'},
                                                 {'option': 'compare', 'fallback': 'yes'},
                                                 {'option': 'orthophoto', 'fallback': 'wms'},
                                                 {'option': 'stepwidth', 'fallback': '0.66'},
                                                 {'option': 'followstreets', 'fallback': 'yes'}]},
            {'section': 'JOB', 'options': [{'option': 'bboxsize', 'fallback': '2000'},
                                           {'option': 'timeout', 'fallback': '5400'}]},
        ]
        self.check_sections(config_parser, sections)
        self.set_options(config_parser, sections)

    def set_options(self, config_parser, sections):
        for section in sections:
            SectionClass = type(section['section'], (), {})
            section_class = SectionClass()
            for option in section['options']:
                if not config_parser.has_option(section['section'], option['option']):
                    raise Exception('Option {0} is not in section {1}!'.format(option['option'], section['section']))
                setattr(section_class, option['option'],
                        config_parser.get(section['section'], option['option'], fallback=option['fallback']))
            setattr(self, section['section'], section_class)

    @staticmethod
    def read_configuration_file(config_file_path):
        if not os.path.isfile(config_file_path):
            raise Exception("The config file does not exist!")
        config_parser = configparser.ConfigParser()
        config_parser.read(config_file_path)
        return config_parser

    @staticmethod
    def check_sections(config_parser, sections):
        for section in sections:
            if not config_parser.has_section(section['section']):
                raise Exception('Section {0} is not in config file!'.format(section['section']))

    @staticmethod
    def to_bool(string):
        return string.lower() in ['true', '1', 't', 'y', 'yes']
