import argparse
from src.base.Bbox import Bbox
from src.role.Worker import Worker
from src.role.Manager import Manager
from redis.exceptions import ConnectionError
from src import cwenv


def redis_args(args):
    return [args.redis_host, args.redis_port, args.redis_pass]


def manager(args):
    big_bbox = Bbox.from_lbrt(
        args.bb_left,
        args.bb_bottom,
        args.bb_right,
        args.bb_top)
    try:
        print('Manger has started...')
        Manager.from_big_bbox(big_bbox, redis_args(args))
    except ConnectionError:
        print(
            'Failed to connect to redis instance [{ip}:{port}], is it running? Check connection arguments and retry.'.format(
                ip=args.redis_host,
                port=args.redis_port))
    finally:
        print 'Manager has finished!'


def jobworker(args):
    jobWorker = Worker.from_worker(['jobs'])
    try:
        print 'JobWorker has started...'
        jobWorker.run(redis_args(args))
    except ConnectionError:
        print(
            'Failed to connect to redis instance [{ip}:{port}], is it running? Check connection arguments and retry.'.format(
                ip=args.redis_host,
                port=args.redis_port))
    finally:
        print 'JobWorker has finished!'


def resultworker(args):
    resultWorker = Worker.from_worker(['results'])
    try:
        print 'ResultWorker has started...'
        resultWorker.run(redis_args(args))
    except ConnectionError:
        print(
            'Failed to connect to redis instance [{ip}:{port}], is it running? Check connection arguments and retry.'.format(
                ip=args.redis_host,
                port=args.redis_port))
    finally:
        print 'ResultWorker has finished!'


def mainfunc():
    parser = argparse.ArgumentParser(description='Detect crosswalks.', )
    redis_host = cwenv('REDIS_HOST')
    redis_port = cwenv('REDIS_PORT')
    redis_pass = cwenv('REDIS_PASS')
    parser.add_argument(
        '--redis',
        action='store',
        dest='redis_host',
        default=redis_host,
        help='hostname or ip of redis database, default is ' +
        redis_host)
    parser.add_argument(
        '--port',
        action='store',
        dest='redis_port',
        default=redis_port,
        help='port of redis database, default is ' +
        redis_port)
    parser.add_argument(
        '--pass',
        action='store',
        dest='redis_pass',
        default=redis_pass,
        help='password of redis database, default is ' +
        redis_pass)

    subparsers = parser.add_subparsers(
        title='worker roles',
        description='',
        help='Select the role of this process')

    p_manager = subparsers.add_parser(
        'manager',
        help='Splits up the given bounding box (WGS84, minlon/minlat/maxlon/maxlat) into small pieces and puts them into the redis queue to be consumed by the jobworkers.')

    bb_left, bb_bottom, bb_right, bb_top = None, None, None, None
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
    p_jobworker.set_defaults(func=jobworker)

    p_resultworker = subparsers.add_parser(
        'resultworker',
        help='Consolidate and write out results.')
    p_resultworker.set_defaults(func=resultworker)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    mainfunc()
