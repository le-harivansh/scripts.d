"""
The purpose of this script is to upgrade the system, and the packages within.
"""

import logging
from argparse import ArgumentParser
from collections import namedtuple
from subprocess import run
from types import SimpleNamespace

if __name__ == '__main__':
    logging.basicConfig(
        format='[%(levelname)s]: %(msg)s',
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
        description='Update the system.',
        epilog='Backup all!',
        add_help=True,
        allow_abbrev=False
    )
    parser.subparsers.all.add_argument(
        '--refresh-mirrors',
        action='store_true',
        help="Refresh pacman's mirrors."
    )

    # parse arguments
    arguments = parser.main.parse_args()

    if arguments.action == 'all':
        logging.info('Starting update...')

        if arguments.refresh_mirrors:
            logging.info("Refreshing pacman's mirrors.")
            run(('sudo', 'pacman-mirrors', '-f'), check=True)

        # update pacman's packages
        logging.info("Updating pacman's packages.")
        run(('sudo', 'pacman', '-Syyu'), check=True)

        # update yaourt's packages
        logging.info("Updating yaourt's packages.")
        run(('yaourt', '-Syuua'), check=True)

        logging.info('Update complete.')
