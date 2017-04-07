import argparse
import logging
import logging.handlers
from redis.exceptions import ConnectionError

from src.base.configuration import Configuration
from src.base.bbox import Bbox
from src.role.worker import Worker
from src.role.manager import Manager


def redis_args(configuration):
    return [configuration.REDIS.server, configuration.REDIS.port, configuration.REDIS.password]


def manager(args, configuration):
    big_bbox = Bbox(left=args.bb_left, bottom=args.bb_bottom, right=args.bb_right, top=args.bb_top)
    try:
        print('Manager has started...')
        manage = Manager(bbox=big_bbox, configuration=configuration, standalone=args.standalone)
        manage.run()
    except ConnectionError:
        print(
            'Failed to connect to redis instance [{ip}:{port}], is it running? Check connection arguments and retry.'.format(
                ip=configuration.REDIS.server,
                port=configuration.REDIS.port))
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
                ip=configuration.REDIS.server,
                port=configuration.REDIS.port))
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
                ip=configuration.REDIS.server,
                port=configuration.REDIS.port))
    finally:
        print('ResultWorker has finished!')


def set_logger():
    root_logger = logging.getLogger()
    syslog_handler = logging.handlers.SysLogHandler(address=('localhost', 514))
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s %(name)s')
    syslog_handler.setFormatter(formatter)
    root_logger.addHandler(syslog_handler)
    root_logger.setLevel(logging.WARNING)


def main_func():
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

    parser.add_argument(
        '-s',
        '--standalone',
        dest='standalone',
        action='store_true',
        help='If chosen the detection will run standalone and save the results in "crosswalks.json".')
    parser.set_defaults(standalone=False)

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
    configuration = Configuration(args.config)
    args.func(args, configuration)


if __name__ == "__main__":
    main_func()
