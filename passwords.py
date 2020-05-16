"""
This module is used to back-up, and restore the user's passwords.
"""

import os
import logging
from argparse import ArgumentParser
from collections import namedtuple
from pathlib import Path
from subprocess import run, PIPE
from types import SimpleNamespace

if __name__ == '__main__':
    DEFAULT_PASSWORDS_FILE_NAME = 'passwords.txt'

    logging.basicConfig(
        format='[%(levelname)s]: %(msg)s',
        level=logging.INFO
    )

    parser = namedtuple('Parser', ('main', 'subparser', 'subparsers'))(
        main := ArgumentParser(
            prog='passwords',
            description='A script to manage passwords.',
            epilog='Lock it!',
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

    # import
    parser.subparsers.import_ = parser.subparser.add_parser(
        'import',
        description='Import passwords from a cleartext file.',
        epilog='Import it!',
        add_help=True,
        allow_abbrev=False
    )
    parser.subparsers.import_.add_argument(
        '--from',
        default=os.getcwd(),
        help='The path to the directory which contains the cleartext passwords file.'
    )
    parser.subparsers.import_.add_argument(
        '--filename',
        default=DEFAULT_PASSWORDS_FILE_NAME,
        help='The name of the cleartext passwords file.'
    )

    # export
    parser.subparsers.export_ = parser.subparser.add_parser(
        'export',
        description='Export passwords to a cleartext file.',
        epilog='Export it!',
        add_help=True,
        allow_abbrev=False
    )
    parser.subparsers.export_.add_argument(
        '--to',
        default=os.getcwd(),
        help='The path to the directory which will contain the cleartext passwords file.'
    )
    parser.subparsers.export_.add_argument(
        '--filename',
        default=DEFAULT_PASSWORDS_FILE_NAME,
        help='The name of the cleartext passwords file.'
    )

    # parse arguments
    arguments = parser.main.parse_args()

    if arguments.action == 'import':
        password_file = Path(f"{arguments.__getattribute__('from')}/{arguments.filename}")

        if not password_file.is_file():
            raise RuntimeError(f'The file: {password_file} does not exist.')

        logging.info("Restoring the passwords into 'pass'...")
        with open(password_file) as file:
            credentials = (tuple(token.strip() for token in item.split()) for item in file.read().splitlines())

            for username, password in credentials:
                run(('pass', 'insert', '--echo', username), input=password.encode('utf-8'))
        logging.info('Passwords restored.')

    elif arguments.action == 'export':
        password_store_path = Path(f'{Path.home()}/.password-store')

        if not Path(arguments.to).is_dir():
            raise RuntimeError(f'The destination: {arguments.to} is not an existing directory.')

        if (password_file := Path(f'{arguments.to}/{arguments.filename}')).is_file():
            raise RuntimeError(f'The file: {arguments.to} already exists in {arguments.to}.')

        credentials = {
            os.path.splitext(str(path.absolute()))[0].replace(f'{password_store_path}/', '', 1): None
            for path in password_store_path.rglob("*.gpg")
        }

        logging.info(f'Backing up the passwords in: {password_file}')

        for username in credentials:
            credentials[username] = run(('pass', username), stdout=PIPE).stdout.decode('utf-8').strip()

        with open(password_file, 'w') as file:
            for username, password in credentials.items():
                file.write(f'{username} {password}\n')

        logging.info('Passwords backed-up')
