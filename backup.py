#!/usr/bin/env python3

import os
import tarfile
from argparse import ArgumentParser, Namespace
from collections import namedtuple
from datetime import date, datetime
from pathlib import Path
from types import SimpleNamespace
from typing import Tuple

from utilities import cd

if __name__ == '__main__':
    today: date = datetime.today().date()
    parser = namedtuple('Parser', ('main', 'subparser', 'subparsers'))(
        main := ArgumentParser(
            prog='backup',
            description='A script to backup important files.',
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
        default=f'backup__{today.year}_{today.month:02d}_{today.day:02d}.tar.gz',
        help='The name of the tar archive.'
    )

    # list
    parser.subparsers.list = parser.subparser.add_parser(
        'list',
        description='List all the files to back up.',
        add_help=True,
        allow_abbrev=False
    )

    files: Tuple = (
        Path(f'{Path.home()}/.gnupg'),
        Path(f'{Path.home()}/.password-store'),
        Path(f'{Path.home()}/.ssh'),
        Path(f'{Path.home()}/.vimrc'),
        Path(f'{Path.home()}/.zshenv'),
        Path(f'{Path.home()}/.zshrc'),
        Path(f'{Path.home()}/.backup'),
        Path(f'{Path.home()}/Storage/Documents'),
    )

    for file in files:
        if not file.exists():
            raise RuntimeError(f'The file {file} does not exist.')

    arguments: Namespace = parser.main.parse_args()

    if arguments.action == 'all':
        if not Path(arguments.destination).is_dir():
            raise RuntimeError(f'The destination: {arguments.destination} is not an existing directory.')

        if (filepath := Path(f'{arguments.destination}/{arguments.filename}')).is_file():
            raise RuntimeError(f'The file: {arguments.filename} already exists in {arguments.destination}.')

        print(f'Backing up the data to: {filepath}...')

        with tarfile.open(filepath, 'w:gz') as backup_file:
            for file in files:
                with cd(file.parent):
                    print(f'Backing up {file}...')
                    backup_file.add(file.name)

        print('Backup complete.')

    elif arguments.action == 'list':
        print('The following files/directories will be backed up:')

        for file in files:
            print(f'{file}')
