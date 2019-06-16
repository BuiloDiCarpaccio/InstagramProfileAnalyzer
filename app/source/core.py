#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from ..configuration import (
    EXIT_FAILURE,
    sys,
    URL_JSON_PRIMARY
)

if __name__ == '__main__':
    sys.exit(EXIT_FAILURE)

import app.source.show as show
import multiprocessing
import ssl

from .analyzer import ProfilAnalyzer
from .cache import (
    get_data_from_cache,
    set_data_into_cache,
    set_information_into_cache,
    username_present_in_cache
)
from .tools import (
    launch_instances,
    request
)
from .username import get_usernames



@launch_instances
def run(instances=[]):
    context = ssl.create_default_context()
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE
    lock_cache_data = multiprocessing.Lock()
    lock_cache_information = multiprocessing.Lock()
    usernames = get_usernames()

    for username in usernames:
        instances.append(multiprocessing.Process(
            target=analyze_profil,
            args=(context, username, lock_cache_data, lock_cache_information)
        ))

def analyze_profil(context, username, lock_cache_data, lock_cache_information):
    analyzer = ProfilAnalyzer(context, username)
    condition = username_present_in_cache(
        analyzer.username, lock_cache_information)

    if condition:
        data = cache_way(analyzer, lock_cache_data, lock_cache_information)
    else:
        data = request_way(analyzer, lock_cache_data, lock_cache_information)

    show.add('User data present in cache', ok=condition)
    show.launch(data)

def cache_way(analyzer, lock_cache_data, _):
    return get_data_from_cache(analyzer.username, lock_cache_data)

def request_way(analyzer, lock_cache_data, lock_cache_information):
    data = {'primary': None, 'posts': None}
    raw = request(URL_JSON_PRIMARY.format(analyzer.username), analyzer.context)

    if raw:
        data['primary'] = analyzer.get_primary_information(raw)
        data['posts'] = analyzer.get_posts_information(raw)
    set_data_into_cache(analyzer.username, data, lock_cache_data)
    set_information_into_cache(analyzer.username, lock_cache_information)
    return data
