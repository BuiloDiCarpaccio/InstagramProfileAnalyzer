#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from .configuration import *

if __name__ == '__main__':
    sys.exit(EXIT_FAILURE)

import functools


def get_users(arguments):
    users = []

    with open(DEFAULT_USER_FILE, 'r') as file:
        users = [lines for lines in file.read().splitlines() if lines[0] != '#']
    for i, argument in enumerate(arguments):
        if argument == USERS_ARGUMENT and i + 1 < len(arguments):
            users.extend(arguments[i + 1].split(','))
    users.sort()
    return list(dict.fromkeys(users))

def extract_target_data(raw_data, key):
    index = raw_data.find(key)
    to_split = key[-1] if key[-1] in '"}]' else ','

    if index != -1:
        raw_data = raw_data[index + len(key):].split(to_split)[0]
        return functools.reduce(lambda rw, c: rw.replace(c, ''), [raw_data, *'"}]'])

def int_convertor(string):
    coefficient = {
        'k':    1000,
        'm':    1000000,
    }

    if string[-1] in coefficient.keys():
        return int(float(string[:-1]) * coefficient[string[-1]])
    else:
        return int(string.replace(',', ''))
