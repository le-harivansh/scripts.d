#!/usr/bin/env python3

import shutil
from argparse import ArgumentParser, Namespace
from pathlib import Path
from subprocess import run, PIPE
from typing import Generator, Mapping, Tuple


def bleachbit(*, root: bool = False) -> None:
    """Clean the system using bleachbit."""

    excluded_cleaners: Tuple[str, ...] = ('system.free_disk_space', 'system.memory')
    cleaners: Generator[str] = (
        cleaner.strip()
        for cleaner in
        run(('bleachbit', '--list-cleaners'), stdout=PIPE, check=True).stdout.decode('utf-8').split()
        if cleaner not in excluded_cleaners
    )

    command: Tuple[str, ...] = ('bleachbit', '--clean', *cleaners)

    if root:
        command = ('sudo', *command)

    print(f'Cleaning the {"system" if root else "user"}-space using bleachbit...')
    run(command, check=True)
    print(f'Cleaned the {"system" if root else "user"}-space using bleachbit.')


def system() -> None:
    """Clean the system using the various available tools."""

    # clean journalctl
    print('Cleaning journalctl...')

    journalctl_config: Mapping[str, str] = {
        'vacuum_time': '30days',
        'vacuum_size': '50M'
    }

    run(
        ('sudo', 'journalctl',
         f'--vacuum-time={journalctl_config["vacuum_time"]}', f'--vacuum-size={journalctl_config["vacuum_size"]}'),
        check=True
    )

    print('Cleaned journalctl.')


def pacman() -> None:
    """Clean pacman."""

    print('Cleaning pacman...')

    # Remove pacman's orphan packages
    print("Removing pacman's orphan packages...")
    orphans: Generator[str] = (orphan.strip() for orphan in
                               run(('pacman', '-Qdtq'), stdout=PIPE).stdout.decode('utf-8').split())
    run(('sudo', 'pacman', '-Rs', *orphans))
    print("Removed pacman's orphan packages.")

    # Clear pacman's cache
    print("Clearing pacman's cache...")
    run(('sudo', 'pacman', '-Scc'))
    print("Cleared pacman's cache.")

    # View pacdiff
    print('Viewing pacdiff...')
    run(('sudo', 'pacdiff'))
    print('Viewed pacdiff.')

    print('Cleaned pacman.')


def pamac() -> None:
    """Clean pamac."""

    print("Removing pamac's orphan packages...")
    run(('pamac', 'remove', '--orphans'))
    print("Removed pamac's orphan packages.")


def jetbrains() -> None:
    """Clean JetBrains application configurations."""

    print("Removing JetBrains applications' configurations...")
    for path in Path.home().glob('.*/**/JetBrains'):
        shutil.rmtree(path)
    shutil.rmtree(Path(f'{str(Path.home())}/.java'))
    print("Removed JetBrains applications' configurations.")


if __name__ == '__main__':
    main_parser: ArgumentParser = ArgumentParser(
        prog='clean',
        description='A script to clean the system.',
        allow_abbrev=False
    )

    all_subparser: ArgumentParser = main_parser.add_subparsers(
        title='Action',
        description='The action to take.',
        dest='action',
        required=True
    ).add_parser(
        'all',
        description='Clean the system.',
        add_help=True,
        allow_abbrev=False
    )

    arguments: Namespace = main_parser.parse_args()

    if arguments.action == 'all':
        bleachbit(root=True)

        bleachbit()

        system()

        pacman()

        pamac()

        jetbrains()
