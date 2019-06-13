#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from .configuration import *

if __name__ == '__main__':
    sys.exit(EXIT_FAILURE)

from .scrapper import Scrapper
from .tools import get_users


def run():
    users = get_users(ARGUMENTS)
    scrapper = Scrapper(SILENT_ARGUMENT in ARGUMENTS)

    for user in users:
        scrapper.launch(user)
        scrapper.clear()
