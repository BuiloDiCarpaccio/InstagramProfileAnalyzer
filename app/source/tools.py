#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from ..configuration import (
    EXIT_FAILURE,
    json,
    sys
)

if __name__ == '__main__':
    sys.exit(EXIT_FAILURE)

import app.source.show as show
import urllib.request
import urllib.error


def launch_instances(function):
    def wrapper(*arg, instances=[], **k_arg):
        to_return = function(*arg, instances=instances, **k_arg)

        for instance in instances:
            instance.start()
        for instance in instances:
            instance.join()
        instances.clear()
        return to_return
    return wrapper

def request(url, context):
    """
    """
    try:
        with urllib.request.urlopen(url, context=context) as access:
            return json.loads(access.read().decode())
    except urllib.error.HTTPError:
        show.add(f'URL not found ({url})', ok=False)
        return {}
