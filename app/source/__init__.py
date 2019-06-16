#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from ..configuration import (
    ARGUMENT_ALL,
    ARGUMENT_CLEAR_CACHE,
    ARGUMENT_HELP,
    EXIT_FAILURE,
    EXIT_SUCCESS,
    sys,
    USAGE
)

if __name__ == '__main__':
    sys.exit(EXIT_FAILURE)

from .cache import clear_cache
from .core import run


def pre_run(run):
    if ARGUMENT_CLEAR_CACHE in ARGUMENT_ALL:
        clear_cache()
        sys.exit(EXIT_SUCCESS)
    if ARGUMENT_HELP in ARGUMENT_ALL:
        sys.stdout.write(USAGE)
        sys.exit(EXIT_SUCCESS)
    return run

run = pre_run(run)
