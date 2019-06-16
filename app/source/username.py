#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from ..configuration import (
    ARGUMENT_ALL,
    ARGUMENT_USERNAME,
    EXIT_FAILURE,
    json,
    PATH_USERNAME,
    sys
)

if __name__ == '__main__':
    sys.exit(EXIT_FAILURE)


def get_usernames():
    """
    """
    usernames = [
        *_extract_usernames_from_arguments(ARGUMENT_ALL),
        *_extract_usernames_from_file(PATH_USERNAME)
    ]

    usernames.sort()
    return list(dict.fromkeys(usernames))

def _extract_usernames_from_arguments(arguments):
    if ARGUMENT_USERNAME in arguments:
        index = arguments.index(ARGUMENT_USERNAME)

        if 0 < index + 1 < len(arguments):
            return arguments[index + 1].split(',')
    return []

def _extract_usernames_from_file(filepath):
    with open(filepath, 'r') as json_file:
        return json.load(json_file)
