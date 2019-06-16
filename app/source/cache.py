#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from ..configuration import (
    ARGUMENT_ALL,
    ARGUMENT_IGNORE_CACHE,
    DATETIME_FORMAT,
    DATETIME_REFRESH,
    EXIT_FAILURE,
    json,
    PATH_CACHE_DATA,
    PATH_CACHE_INFORMATION,
    sys
)

if __name__ == '__main__':
    sys.exit(EXIT_FAILURE)

import os

from datetime import datetime, timedelta


def clear_cache():
    """
    """
    os.system('rm -rf app/__pycache__')
    os.system('rm -rf app/source/__pycache__')
    os.system('rm -rf app/source/components/__pycache__')
    with open(PATH_CACHE_DATA, 'w') as json_file:
        json.dump({}, json_file, sort_keys=True, ensure_ascii=False, indent=4)
    with open(PATH_CACHE_INFORMATION, 'w') as json_file:
        json.dump({}, json_file, sort_keys=True, ensure_ascii=False, indent=4)

def _check_if_cache_ignored(function):
    """
    """
    if ARGUMENT_IGNORE_CACHE in ARGUMENT_ALL:
        return lambda *arg, **k_arg: False
    return function

@_check_if_cache_ignored
def get_data_from_cache(username, lock_cache_data):
    """
    """
    lock_cache_data.acquire()
    with open(PATH_CACHE_DATA, 'r') as json_file:
        data = json.load(json_file)
    lock_cache_data.release()

    return data[username].copy()

@_check_if_cache_ignored
def set_data_into_cache(username, new_data, lock_cache_data):
    """
    """
    lock_cache_data.acquire()
    with open(PATH_CACHE_DATA, 'r') as json_file:
        data = json.load(json_file)
    lock_cache_data.release()

    data.update({username: new_data})

    lock_cache_data.acquire()
    with open(PATH_CACHE_DATA, 'w') as json_file:
        json.dump(
            data, json_file, sort_keys=True, ensure_ascii=False, indent=4)
    lock_cache_data.release()

@_check_if_cache_ignored
def set_information_into_cache(username, lock_cache_information):
    """
    """
    lock_cache_information.acquire()
    with open(PATH_CACHE_INFORMATION, 'r') as json_file:
        data = json.load(json_file)
    lock_cache_information.release()

    data.update({username: datetime.now().strftime(DATETIME_FORMAT)})

    lock_cache_information.acquire()
    with open(PATH_CACHE_INFORMATION, 'w') as json_file:
        json.dump(data, json_file, sort_keys=True, ensure_ascii=False, indent=4)
    lock_cache_information.release()

@_check_if_cache_ignored
def username_present_in_cache(username, lock_cache_information):
    """
    """
    lock_cache_information.acquire()
    with open(PATH_CACHE_INFORMATION, 'r') as json_file:
        username_date = json.load(json_file)
    lock_cache_information.release()

    username_date = username_date.get(username)
    if not username_date:
        return False
    username_date = datetime.strptime(username_date, DATETIME_FORMAT)
    return (datetime.now() - username_date) < timedelta(**DATETIME_REFRESH)
