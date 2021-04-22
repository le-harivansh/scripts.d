from contextlib import contextmanager
from os import chdir, getcwd


@contextmanager
def cd(destination: str) -> None:
    """
    A context manager to change directory. Mimics unix's cd.

    Args:
        destination (str): The directory to cd into.
    """
    current_working_directory = getcwd()

    try:
        chdir(destination)
        yield
    finally:
        chdir(current_working_directory)
