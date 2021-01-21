"""
This script is used to clean up the system.
"""

import logging
import shutil
from argparse import ArgumentParser
from collections import namedtuple
from pathlib import Path
from subprocess import run, PIPE
from types import SimpleNamespace


class Clean:
    @staticmethod
    def bleachbit(root: bool = False) -> None:
        """Clean the system using bleachbit."""

        excluded_cleaners = ('system.free_disk_space', 'system.memory')
        cleaners = (
            cleaner.strip()
            for cleaner in
            run(('bleachbit', '--list-cleaners'), stdout=PIPE, check=True).stdout.decode('utf-8').split()
            if cleaner not in excluded_cleaners
        )

        command = ('bleachbit', '--clean', *cleaners)

        if root:
            command = ('sudo', *command)

        logging.info(f'Cleaning the {"system" if root else "user"}-space using bleachbit...')
        run(command, check=True)
        logging.info(f'Cleaned the {"system" if root else "user"}-space using bleachbit.')

    @staticmethod
    def system() -> None:
        """Clean the system using the various available tools."""

        # clean journalctl
        logging.info('Cleaning journalctl...')

        journalctl_config = {
            'vacuum_time': '30days',
            'vacuum_size': '50M'
        }

        run(
            ('sudo', 'journalctl',
             f'--vacuum-time={journalctl_config["vacuum_time"]}', f'--vacuum-size={journalctl_config["vacuum_size"]}'),
            check=True
        )

        logging.info('Cleaned journalctl.')

    @staticmethod
    def pacman() -> None:
        """Clean pacman."""

        logging.info('Cleaning pacman...')

        # Remove pacman's orphan packages
        logging.info("Removing pacman's orphan packages...")
        orphans = (orphan.strip() for orphan in run(('pacman', '-Qdtq'), stdout=PIPE).stdout.decode('utf-8').split())
        run(('sudo', 'pacman', '-Rs', *orphans))
        logging.info("Removed pacman's orphan packages.")

        # Clear pacman's cache
        logging.info("Clearing pacman's cache...")
        run(('sudo', 'pacman', '-Scc'))
        logging.info("Cleared pacman's cache.")

        # View pacdiff
        logging.info('Viewing pacdiff...')
        run(('sudo', 'pacdiff'))
        logging.info('Viewed pacdiff.')

        logging.info('Cleaned pacman.')

    @staticmethod
    def yaourt() -> None:
        """Clean yaourt."""

        logging.info("Removing yaourt's orphan packages...")
        run(('yaourt', '-Qdtq'))
        logging.info("Removed yaourt's orphan packages.")

    @staticmethod
    def jetbrains() -> None:
        """Clean JetBrains application configurations."""

        logging.info("Removing JetBrains applications' configurations...")
        for path in Path.home().glob('.*/**/JetBrains'):
            shutil.rmtree(path)
        shutil.rmtree(Path(f'{str(Path.home())}/.java'))
        logging.info("Removed JetBrains applications' configurations.")

    @staticmethod
    def docker() -> None:
        """Remove all docker images, containers, networks, and volumes."""

        logging.info("Purging all docker images, containers, networks, and volumes...")
        run((f'{Path.cwd()}/docker-utilities.py', 'purge'))
        logging.info("Purged all docker images, containers, networks, and volumes.")


if __name__ == '__main__':
    logging.basicConfig(
        format='[%(levelname)s] [%(asctime)s]: %(msg)s',
        level=logging.INFO
    )

    parser = namedtuple('Parser', ('main', 'subparser', 'subparsers'))(
        main := ArgumentParser(
            prog='clean',
            description='A script to clean the system.',
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
        description='Clean the system.',
        epilog='Clean all!',
        add_help=True,
        allow_abbrev=False
    )
    parser.subparsers.all.add_argument(
        '--jetbrains',
        action='store_true',
        help="Clean jetbrains applications' configurations."
    )
    parser.subparsers.all.add_argument(
        '--bleachbit-root',
        action='store_true',
        help="Clean the system's configurations using bleachbit."
    )

    arguments = parser.main.parse_args()

    if arguments.action == 'all':
        if arguments.bleachbit_root:
            Clean.bleachbit(root=True)

        Clean.bleachbit()
        Clean.system()
        Clean.pacman()
        Clean.yaourt()
        Clean.docker()

        if arguments.jetbrains:
            Clean.jetbrains()
