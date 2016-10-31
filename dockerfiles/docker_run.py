import os
import shutil
import sys
import argparse
import subprocess
import dockerpty

from docker import Client

client = Client(base_url='unix://var/run/docker.sock')
current_directory = os.path.dirname(os.path.realpath(__file__))


def build_container_if_not_exist(path, name):
    try:
        if not client.images(name):
            dockerfile_path = path + 'Dockerfile'
            if os.path.isfile(dockerfile_path):
                _ = [print(line.decode("utf-8")) for line in client.build(rm=True, tag=name, path=path)]
            else:
                print("Can't find the file: " + path)
                sys.exit()
    except IOError:
        print('To work with docker you need root permissions.')
        sys.exit()


def stop_running_container(name):
    containers = client.containers(filters={'name': name})
    if containers:
        client.stop(name)


def remove_container_if_exist(name):
    containers = client.containers(all=True, filters={'name': name})
    if containers:
        stop_running_container(name)
        client.remove_container(name)


def create_container_if_not_exist(image=None, volumes=None, ports=None, name=None, tty=False, stdin_open=False):
    remove_container_if_exist(name)
    return client.create_container(image=image, volumes=volumes, ports=ports, name=name, tty=tty, stdin_open=stdin_open)

#docker run -d --name crosswalk_redis -p 40001:40001 -p 40002:40002 -p 40003:40003 -v .redis/:/redis crosswalk_redis:latest
def redis():
    path = current_directory + '/redis/'
    name = 'crosswalk_redis'
    redis_port = 40001
    redis_dashboard = 40002
    visualize_port = 40003
    build_container_if_not_exist(path, name + ':latest')
    container = create_container_if_not_exist(image=name, volumes=current_directory + '/redis:/redis/',
                                              ports=[redis_port, redis_dashboard, visualize_port], name=name)
    client.start(container,
                 port_bindings={redis_port: ('0.0.0.0', redis_port), redis_dashboard: ('0.0.0.0', redis_dashboard)})

#nvidia-docker run -it --name crosswalk_detection -v .crosswalks/:/crosswalks crosswalk_detection:latest bash
def detection():
    path = current_directory + '/detection/'
    name = 'crosswalk_detection'
    volume = current_directory + 'crosswalks:/crosswalks/'
    build_container_if_not_exist(path, name + ':latest')
    if shutil.which('nvidia-docker'):
        remove_container_if_exist(name)
        subprocess.run('nvidia-docker run -it -v ' + volume + ' -t ' + name + ' ' + name + ' bash')
    else:
        container = create_container_if_not_exist(image=name, volumes=volume, name=name, tty=True, stdin_open=True)
        dockerpty.start(client, container)


def switch(args):
    if args.crosswalk_redis:
        redis()
    if args.crosswalk_detection:
        detection()


def run():
    parser = argparse.ArgumentParser(description='Detect crosswalks.', )

    group = parser.add_mutually_exclusive_group(required=True)

    group.add_argument(
        '-r',
        '--crosswalk_redis',
        action='store_true',
        dest='crosswalk_redis',
        help='runs a docker container with a redis instance')
    group.add_argument(
        '-d',
        '--crosswalk_detection',
        action='store_true',
        dest='crosswalk_detection',
        help='runs a docker container for the detection algorithm')
    group.set_defaults(func=switch)
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    run()
