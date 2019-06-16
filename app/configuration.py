#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import sys

# EXIT
EXIT_FAILURE = 84
EXIT_SUCCESS = 0

if __name__ == '__main__':
    sys.exit(EXIT_FAILURE)

import json


# ARGUMENT
ARGUMENT_ALL                = sys.argv[1:]
ARGUMENT_CLEAR_CACHE        = '--clear-cache'
ARGUMENT_IGNORE_CACHE       = '--ignore-cache'
ARGUMENT_HELP               = '--help'
ARGUMENT_SILENT             = '--silent'
ARGUMENT_USERNAME           = '--username'

# SETTINGS
SETTINGS_CONFIGURATION_PATH = 'app/settings/configuration.json'
SETTINGS_GLOBALS            = globals()

with open(SETTINGS_CONFIGURATION_PATH, 'r') as json_file:
    configuration = json.load(json_file)

    for category in configuration:
        for key in configuration[category]:
            SETTINGS_GLOBALS[f'{category}_{key}'] = configuration[category][key]

# SHOW
SHOW_KO = '[\033[31mKO\033[0m] '
SHOW_OK = '[\033[32mOK\033[0m] '

# USAGE
USAGE = """USAGE
    {0} [{1}] [{2}] [{3}] [{4} username[,...]]

DESCRIPTION
    Analyzes the instagram profiles of a user list (the list can be found in
    the file "username.json"). It is also possible to add these arguments:
       {1:<15}  clears the cache
       {2:<15}  ignores the cache
       {3:<15}  no message will be written
       {4:<15}  allows to add users to be analyzed
""".format(
    sys.argv[0],
    ARGUMENT_CLEAR_CACHE,
    ARGUMENT_IGNORE_CACHE,
    ARGUMENT_SILENT,
    ARGUMENT_USERNAME
)
