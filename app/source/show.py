#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from ..configuration import (
    ARGUMENT_ALL,
    ARGUMENT_SILENT,
    EXIT_FAILURE,
    SHOW_KO,
    SHOW_OK,
    sys
)

if __name__ == '__main__':
    sys.exit(EXIT_FAILURE)


def _check_if_silent_mode(function):
    """
    """
    if ARGUMENT_SILENT in ARGUMENT_ALL:
        return lambda *arg, **k_arg: False
    return function

@_check_if_silent_mode
def add(message, ok=None, order=0):
    if not hasattr(add, 'stack'):
        add.stack = []
    order = ((order + 1) * '\t')

    if ok is not None:
        order += SHOW_OK if ok else SHOW_KO
    add.stack.append(order + message)

@_check_if_silent_mode
def launch(data):
    primary, posts = data['primary'], data['posts']

    if primary:
        add.stack.insert(0, '_' * 80)
        add.stack.insert(1, f">>> {primary['username']}")
        add(primary['url'], ok=True)
        add('Primary information [', order=1)
        add(f"- {primary['name']} ({primary['username']})", order=2)
        add(f"- {primary['posts']} post(s)", order=2)
        add(f"- {primary['followers']} follower(s)", order=2)
        add(f"- {primary['following']} following", order=2)
        add(f"- Biography : {primary['biography']}", order=2)
        add(']', order=1)
        add(f"It's a public account.", ok=(not primary['is_private']))
        if not primary['is_private']:
            add('Post(s) information [', order=1)
            for post in posts:
                add(f"{post['url']} [", ok=post['type'], order=2)
                if post['type']:
                    add(f"- The post is a {post['type']}", order=3)
                    add(f"- Posted on {post['date']}", order=3)
                    add(f"- Located in {post['location']}", order=3)
                    add(f"- {post['like']} like(s)", order=3)
                    add(f"- {len(post['comment'])} comment(s)", order=3)
                    add(f"- Description : {post['description']}", order=3)
                    add(f"- Recognization : {post['recognization']}", order=3)
                add(']', order=2)
            add(']', order=1)
    sys.stdout.write('\n'.join(add.stack) + '\n')
