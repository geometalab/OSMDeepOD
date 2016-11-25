import argparse
import configparser
import logging
import logging.handlers
import os
from redis.exceptions import ConnectionError

from src.base.configuration import Configuration
from src.base.bbox import Bbox
from src.role.worker import Worker
from src.role.manager import Manager


def redis_args(configuration):
    return [configuration.server, configuration.port, configuration.password]


def manager(args, configuration):
    big_bbox = Bbox(left=args.bb_left, bottom=args.bb_bottom, right=args.bb_right, top=args.bb_top)
    try:
        print('Manager has started...')
        manage = Manager(big_bbox, 'jobs', configuration, args.standalone)
        manage.run()
    except ConnectionError:
        print(
            'Failed to connect to redis instance [{ip}:{port}], is it running? Check connection arguments and retry.'.format(
                ip=configuration.server,
                port=configuration.port))
    finally:
        print('Manager has finished!')


def job_worker(_, configuration):
    worker = Worker.from_worker(['jobs'])
    try:
        print('JobWorker has started...')
        worker.run(redis_args(configuration))
    except ConnectionError:
        print(
            'Failed to connect to redis instance [{ip}:{port}], is it running? Check connection arguments and retry.'.format(
                ip=configuration.server,
                port=configuration.port))
    finally:
        print('JobWorker has finished!')


def result_worker(_, configuration):
    worker = Worker.from_worker(['results'])
    try:
        print('ResultWorker has started...')
        worker.run(redis_args(configuration))
    except ConnectionError:
        print(
            'Failed to connect to redis instance [{ip}:{port}], is it running? Check connection arguments and retry.'.format(
                ip=configuration,
                port=configuration))
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
    if not os.path.isfile(config_file):
        raise Exception("The config file does not exist! " + config_file)
    config.read(config_file)
    configuration = Configuration()
    if not args.standalone:
        configuration.check_redis_fields(config)
    configuration.set_from_config_parser(config)

    if args.role is 'manager':
        configuration.check_manager_config(config)
    return configuration


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
    p_manager.add_argument(
        '-s'
        '--standalone',
        dest='standalone',
        action='store_true',
        help='If chosen the detection will run standalone and save the results in "crosswalks.json".')
    p_manager.set_defaults(standalone=False)

    p_jobworker = subparsers.add_parser(
        'jobworker',
        help='Detect crosswalks on element from the redis queue.')
    p_jobworker.set_defaults(func=job_worker)

    p_resultworker = subparsers.add_parser(
        'resultworker',
        help='Consolidate and write out results.')
    p_resultworker.set_defaults(func=result_worker)

    args = parser.parse_args()
    configuration = read_config(args)
    args.func(args, configuration)


if __name__ == "__main__":
    mainfunc()
