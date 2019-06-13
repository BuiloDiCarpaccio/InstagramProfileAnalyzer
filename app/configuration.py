#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import sys

EXIT_FAILURE = 84
EXIT_SUCCESS = 0

if __name__ == '__main__':
    sys.exit(EXIT_FAILURE)


ARGUMENTS           = sys.argv[1:]
USERS_ARGUMENT      = '--users'
SILENT_ARGUMENT     = '--silent'

DEFAULT_USER_FILE   = 'users.txt'
DEFAULT_UNTIL_DATE  = '1019-01-01 00:00:00'

INSTAGRAM_URL       = 'https://www.instagram.com/{}/'
INSTAGRAM_IMAGE_URL = 'https://www.instagram.com/p/{}/'
INSTAGRAM_LIKES_URL = (
    'https://www.instagram.com/graphql/query/?query_hash=d5d763b1e2acf209d62d22d184488e57&variables={{"shortcode":"{}","include_reel":true,"first":50}}',
    'https://www.instagram.com/graphql/query/?query_hash=d5d763b1e2acf209d62d22d184488e57&variables={{"shortcode":"{}","include_reel":true,"first":50,"after":"{}"}}'
)

FAILURE             = '[\033[31mFAILURE\033[0m]'
SUCCESS             = '[\033[32mSUCCESS\033[0m]'
WARNING             = '[\033[33mWARNING\033[0m]'

TOP_SIZE            = 10