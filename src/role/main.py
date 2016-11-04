import argparse
import configparser
import logging
import logging.handlers
import os
from redis.exceptions import ConnectionError

from src.base.search import Search
from src.base.bbox import Bbox
from src.role.worker import Worker
from src.role.manager import Manager


def redis_args(config):
    return [config['REDIS']['server'], config['REDIS']['port'], config['REDIS']['password']]


def manager(args, config):
    big_bbox = Bbox.from_lbrt(
        args.bb_left,
        args.bb_bottom,
        args.bb_right,
        args.bb_top)
    try:
        print('Manger has started...')
        word = config.get(section='DETECTION', option='word', fallback='crosswalk')
        key = config.get(section='DETECTION', option='key', fallback='highway')
        value = config.get(section='DETECTION', option='value', fallback='crosswalk')
        zoom = config.getint(section='DETECTION', option='zoom', fallback=19)
        compare = config.getboolean(section='DETECTION', option='compare', fallback=True)
        orthofoto = config.get(section='DETECTION', option='orthofoto', fallback='other')
        network = config.get(section='DETECTION', option='network')
        search = Search(word=word, key=key, value=value, zoom_level=zoom, compare=compare, orthofoto=orthofoto,
                        network=network)
        Manager.from_big_bbox(
            big_bbox,
            redis_args(config),
            'jobs',
            search)
    except ConnectionError:
        print(
            'Failed to connect to redis instance [{ip}:{port}], is it running? Check connection arguments and retry.'.format(
                ip=config['REDIS']['server'],
                port=config['REDIS']['port']))
    finally:
        print('Manager has finished!')


def job_worker(_, config):
    worker = Worker.from_worker(['jobs'])
    try:
        print('JobWorker has started...')
        worker.run(redis_args(config))
    except ConnectionError:
        print(
            'Failed to connect to redis instance [{ip}:{port}], is it running? Check connection arguments and retry.'.format(
                ip=config['REDIS']['server'],
                port=config['REDIS']['port']))
    finally:
        print('JobWorker has finished!')


def result_worker(_, config):
    worker = Worker.from_worker(['results'])
    try:
        print('ResultWorker has started...')
        worker.run(redis_args(config))
    except ConnectionError:
        print(
            'Failed to connect to redis instance [{ip}:{port}], is it running? Check connection arguments and retry.'.format(
                ip=config['REDIS']['server'],
                port=config['REDIS']['port']))
    finally:
        print('ResultWorker has finished!')


def set_logger():
    root_logger = logging.getLogger()
    syslog_handler = logging.handlers.SysLogHandler(address=('localhost', 514))
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s %(name)s')
    syslog_handler.setFormatter(formatter)
    root_logger.addHandler(syslog_handler)
    root_logger.setLevel(logging.WARNING)


def read_config(args):
    config_file = args.config
    config = configparser.ConfigParser()
    if not os.path.isfile(config_file): raise Exception("The config file does not exist! " + config_file)

    config.read(config_file)
    if not os.path.isfile(config_file): raise Exception("The config file could not be red! " + config_file)
    if not config.has_section('REDIS'): raise Exception("Section 'REDIS' is not in config file! " + config_file)
    if not config.has_option('REDIS', 'server'): raise Exception("'server' no in 'REDIS' section! " + config_file)
    if not config.has_option('REDIS', 'password'): raise Exception("'password' no in 'REDIS' section! " + config_file)
    if not config.has_option('REDIS', 'port'): raise Exception("'port' no in 'REDIS' section! " + config_file)

    if args.role == 'manager':
        if not config.has_section('DETECTION'): raise Exception(
            "Section 'DETECTION' is not in config file! " + config_file)
        if not config.has_option('DETECTION', 'network'): raise Exception(
            "'network' no in 'DETECTION' section! " + config_file)
        if not os.path.isfile(config_file): raise Exception("The config file does not exist! " + config_file)
    return config


def mainfunc():
    set_logger()
    parser = argparse.ArgumentParser(description='Detect crosswalks.', )
    parser.add_argument(
        '-c',
        '--config',
        action='store',
        dest='config',
        required=True,
        help='The path to the configuration file.'
    )

    subparsers = parser.add_subparsers(
        title='worker roles',
        description='',
        dest='role',
        help='Select the role of this process'
    )

    subparsers.required = True

    p_manager = subparsers.add_parser(
        'manager',
        help='Splits up the given bounding box (WGS84, minlon/minlat/maxlon/maxlat) into small pieces and puts them into the redis queue to be consumed by the jobworkers.')
    p_manager.add_argument(
        'bb_left',
        type=float,
        action='store',
        help='left float value of the bounding box (WGS84, minlon)')
    p_manager.add_argument(
        'bb_bottom',
        type=float,
        action='store',
        help='bottom float value of the bounding box (WGS84, minlat)')
    p_manager.add_argument(
        'bb_right',
        type=float,
        action='store',
        help='right float value of the bounding box (WGS84, maxlon)')
    p_manager.add_argument(
        'bb_top',
        type=float,
        action='store',
        help='top float value of the bounding box (WGS84, maxlat)')
    p_manager.set_defaults(func=manager)

    p_jobworker = subparsers.add_parser(
        'jobworker',
        help='Detect crosswalks on element from the redis queue.')
    p_jobworker.set_defaults(func=job_worker)

    p_resultworker = subparsers.add_parser(
        'resultworker',
        help='Consolidate and write out results.')
    p_resultworker.set_defaults(func=result_worker)

    args = parser.parse_args()
    config = read_config(args)
    args.func(args, config)


if __name__ == "__main__":
    mainfunc()
