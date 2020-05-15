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
        format='[%(levelname)s]: %(msg)s',
        level=logging.INFO
    )
    today = datetime.today().date()
    parser = namedtuple('Parser', ('main', 'subparser', 'subparsers'))(
        main := ArgumentParser(
            prog='backup',
            description='A utility to backup important files.',
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
        '--name',
        default=f'{today.year}_{today.month:02d}_{today.day:02d}.tar.gz',
        help='The name of the backup tar file.'
    )

    # list
    parser.subparsers.list = parser.subparser.add_parser(
        'list',
        description='List all the files to back up.',
        epilog='List all!',
        add_help=True,
        allow_abbrev=False
    )

    files = (
        Path(f'{Path.home()}/.gnupg'),
        Path(f'{Path.home()}/.password-store'),
        Path(f'{Path.home()}/.ssh'),
        Path(f'{Path.home()}/.vimrc'),
        Path(f'{Path.home()}/.zshenv'),
        Path(f'{Path.home()}/.zshrc'),
        Path(f'{Path.home()}/.miscellaneous'),
        Path(f'{Path.home()}/Storage/Documents')
    )

    for file in files:
        if not file.exists():
            raise RuntimeError(f'The file {file} does not exist.')

    # parse arguments
    arguments = parser.main.parse_args()

    if arguments.action == 'all':
        if not Path(arguments.destination).is_dir():
            raise RuntimeError(f'The destination: {arguments.destination} is not an existing directory.')

        if (filepath := Path(f'{arguments.destination}/{arguments.name}')).is_file():
            raise RuntimeError(f'The file: {arguments.name} already exists in {arguments.destination}.')

        logging.info(f'Starting backup to: {filepath}')

        with tarfile.open(filepath, 'w:gz') as backup_file:
            for file in files:
                logging.info(f'Backing up {file}')
                backup_file.add(file)

        logging.info('Backup complete.')

    elif arguments.action == 'list':
        print('The following files/directories will be backed up:')

        for file in files:
            print(f'{file}')
