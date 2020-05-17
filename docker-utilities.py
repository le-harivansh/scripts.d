"""
The purpose of this script is to manage docker resources.
"""

import logging
from argparse import ArgumentParser
from collections import namedtuple
from subprocess import run, PIPE
from types import SimpleNamespace

if __name__ == '__main__':
    logging.basicConfig(
        format='[%(levelname)s]: %(msg)s',
        level=logging.INFO
    )

    parser = namedtuple('Parser', ('main', 'subparser', 'subparsers'))(
        main := ArgumentParser(
            prog='docker-utilities',
            description='A script for high-level docker-management.',
            epilog='Goodbye, world!',
            allow_abbrev=False
        ),
        main.add_subparsers(
            title='Action',
            description='The action to take.',
            dest='action',
            required=True
        ),
        SimpleNamespace()
    )

    # purge
    parser.subparsers.purge = parser.subparser.add_parser(
        'purge',
        description='Purge all docker images, containers, and networks.',
        epilog='Purge all!',
        add_help=True,
        allow_abbrev=False
    )

    # status
    parser.subparsers.status = parser.subparser.add_parser(
        'status',
        description='Get the status of all docker images, containers, and networks.',
        epilog='Status!',
        add_help=True,
        allow_abbrev=False
    )

    # parse arguments
    arguments = parser.main.parse_args()

    if arguments.action == 'status':
        # Containers
        logging.info('** Containers **')
        run(('docker', 'container', 'ls', '--all'))
        print()

        # Volumes
        logging.info('** Volumes **')
        run(('docker', 'volume', 'ls'))
        print()

        # Images
        logging.info('** Images **')
        run(('docker', 'image', 'ls', '--all'))
        print()

        # Networks
        logging.info('** Networks **')
        run(('docker', 'network', 'ls'))
        print()

    elif arguments.action == 'purge':
        # Containers
        containers = tuple(
            container.strip() for container in
            run(
                ('docker', 'container', 'ls', '--all', '--quiet'),
                stdout=PIPE
            ).stdout.decode('utf-8').split()
        )

        # |---> stop
        logging.info('Stopping all containers...')
        for container in containers:
            run(('docker', 'container', 'stop', container))

        # |---> remove
        logging.info('Removing all containers...')
        for container in containers:
            run(('docker', 'container', 'rm', '--force', container))

        # Volumes
        volumes = tuple(
            volume.strip() for volume in
            run(
                ('docker', 'volume', 'ls', '--quiet'),
                stdout=PIPE
            ).stdout.decode('utf-8').split()
        )

        # |---> remove
        logging.info('Removing all volumes...')
        for volume in volumes:
            run(('docker', 'volume', 'rm', '--force', volume))

        # Images
        images = tuple(
            image.strip() for image in
            run(
                ('docker', 'image', 'ls', '--all', '--quiet'),
                stdout=PIPE
            ).stdout.decode('utf-8').split()
        )

        # |---> remove
        logging.info('Removing all images...')
        for image in images:
            run(('docker', 'image', 'rm', '--force', image))

        # Networks
        networks = tuple(
            network.strip() for network in
            run(
                ('docker', 'network', 'ls', '--quiet'),
                stdout=PIPE
            ).stdout.decode('utf-8').split()
        )

        # |---> remove
        logging.info('Removing all networks...')
        for network in networks:
            run(('docker', 'network', 'rm', network))
