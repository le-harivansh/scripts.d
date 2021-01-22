"""
The purpose of this script is to upgrade the system and the packages within.
"""

import logging
from argparse import ArgumentParser
from collections import namedtuple
from subprocess import run
from types import SimpleNamespace

if __name__ == '__main__':
    logging.basicConfig(
        format='[%(levelname)s] [%(asctime)s]: %(msg)s',
        level=logging.INFO
    )

    parser = namedtuple('Parser', ('main', 'subparser', 'subparsers'))(
        main := ArgumentParser(
            prog='upgrade',
            description='A script to upgrade the system, and its packages.',
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

    # all
    parser.subparsers.all = parser.subparser.add_parser(
        'all',
        description='Upgrade the system.',
        epilog='Upgrade all!',
        add_help=True,
        allow_abbrev=False
    )
    parser.subparsers.all.add_argument(
        '--refresh-mirrors',
        action='store_true',
        help="Refresh pacman's mirrors."
    )

    arguments = parser.main.parse_args()

    if arguments.action == 'all':
        logging.info('Starting upgrade...')

        if arguments.refresh_mirrors:
            logging.info("Refreshing pacman's mirrors.")
            run(('sudo', 'pacman-mirrors', '-f'), check=True)

        logging.info("Upgrading pacman packages...")
        run(('sudo', 'pacman', '-Syyu'), check=True)

        logging.info("Upgrading AUR packages...")
        run(('pacaur', '-Syuua'), check=True)

        logging.info('Upgrade complete.')
