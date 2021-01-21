"""
This module is in charge of backing up the current user's data.
"""

import logging
import os
import tarfile
from argparse import ArgumentParser
from collections import namedtuple
from datetime import datetime
from pathlib import Path
from types import SimpleNamespace

if __name__ == '__main__':
    logging.basicConfig(
        format='[%(levelname)s] [%(asctime)s]: %(msg)s',
        level=logging.INFO
    )

    today = datetime.today().date()
    parser = namedtuple('Parser', ('main', 'subparser', 'subparsers'))(
        main := ArgumentParser(
            prog='backup',
            description='A script to backup important files.',
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
        description='Backup all the necessary files.',
        epilog='Backup all!',
        add_help=True,
        allow_abbrev=False
    )
    parser.subparsers.all.add_argument(
        '--destination',
        default=os.getcwd(),
        help='The path to the directory which will contain the backed-up archive.'
    )
    parser.subparsers.all.add_argument(
        '--filename',
        default=f'{today.year}_{today.month:02d}_{today.day:02d}.tar.gz',
        help='The name of the tar archive.'
    )

    # list
    parser.subparsers.list = parser.subparser.add_parser(
        'list',
        description='List all the files to back up.',
        epilog='List all!',
        add_help=True,
        allow_abbrev=False
    )

    directories = (
        Path(f'{Path.home()}/.gnupg'),
        Path(f'{Path.home()}/.password-store'),
        Path(f'{Path.home()}/.ssh'),
        Path(f'{Path.home()}/.vimrc'),
        Path(f'{Path.home()}/.zshenv'),
        Path(f'{Path.home()}/.zshrc'),
        Path(f'{Path.home()}/.backup'),
        Path(f'{Path.home()}/Storage/Documents')
    )

    for directory in directories:
        if not directory.exists():
            raise RuntimeError(f'The file {directory} does not exist.')

    arguments = parser.main.parse_args()

    if arguments.action == 'all':
        if not Path(arguments.destination).is_dir():
            raise RuntimeError(f'The destination: {arguments.destination} is not an existing directory.')

        if (filepath := Path(f'{arguments.destination}/{arguments.filename}')).is_file():
            raise RuntimeError(f'The file: {arguments.filename} already exists in {arguments.destination}.')

        logging.info(f'Backing up the data to: {filepath}')

        with tarfile.open(filepath, 'w:gz') as backup_file:
            for directory in directories:
                logging.info(f'Backing up {directory}...')
                backup_file.add(directory)

        logging.info('Backup complete.')

    elif arguments.action == 'list':
        print('The following files/directories will be backed up:')

        for directory in directories:
            print(f'{directory}')
