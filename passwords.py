#!/usr/bin/env python3

import os
from argparse import ArgumentParser, Namespace
from collections import namedtuple
from pathlib import Path
from subprocess import run, PIPE
from types import SimpleNamespace
from typing import Generator, Mapping, Tuple, Union

if __name__ == '__main__':
    DEFAULT_PASSWORDS_FILE_NAME = 'passwords.txt'

    parser = namedtuple('Parser', ('main', 'subparser', 'subparsers'))(
        main := ArgumentParser(
            prog='passwords',
            description='A script to manage passwords.',
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
        add_help=True,
        allow_abbrev=False
    )
    parser.subparsers.export_.add_argument(
        '--to',
        default=f'{Path.home()}/.backup',
        help='The path to the directory which will contain the cleartext passwords file.'
    )
    parser.subparsers.export_.add_argument(
        '--filename',
        default=DEFAULT_PASSWORDS_FILE_NAME,
        help='The name of the cleartext passwords file.'
    )

    arguments: Namespace = parser.main.parse_args()

    if arguments.action == 'import':
        password_file: Path = Path(f"{arguments.__getattribute__('from')}/{arguments.filename}")

        if not password_file.is_file():
            raise RuntimeError(f'The file: {password_file} does not exist.')

        print("Restoring the passwords into 'pass'...")
        with open(password_file) as file:
            credentials: Generator[Tuple[str, ...]] = (tuple(token.strip() for token in item.split()) for item in
                                                       file.read().splitlines())

            for username, password in credentials:
                run(('pass', 'insert', '--echo', username), input=password.encode('utf-8'))
        print('Passwords restored.')

    elif arguments.action == 'export':
        password_store: Path = Path(f'{Path.home()}/.password-store')

        if not Path(arguments.to).is_dir():
            raise RuntimeError(f'The destination: {arguments.to} is not an existing directory.')

        if (password_file := Path(f'{arguments.to}/{arguments.filename}')).is_file():
            raise RuntimeError(f'The file: {arguments.filename} already exists in {arguments.to}.')

        credentials: Mapping[str, Union[str, None]] = {
            os.path.splitext(str(path.absolute()))[0].replace(f'{password_store}/', '', 1): None
            for path in password_store.rglob("*.gpg")
        }

        print(f'Backing up the passwords in: {password_file}...')

        for username in credentials:
            credentials[username] = run(('pass', username), stdout=PIPE).stdout.decode('utf-8').strip()

        with open(password_file, 'w') as file:
            for username, password in credentials.items():
                file.write(f'{username} {password}\n')

        print('Passwords backed-up.')
