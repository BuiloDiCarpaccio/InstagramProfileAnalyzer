#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from ...configuration import (
    EXIT_FAILURE,
    sys,
    URL_JSON_POST,
    URL_POST
)

if __name__ == '__main__':
    sys.exit(EXIT_FAILURE)

import threading

from ..tools import request


class Post(threading.Thread):
    """
    """

    def __init__(self, posts, context, shortcode, date):
        self._context = context
        self._post = {
            'comment':          [],
            'date':             date,
            'description':      None,
            'like':             None,
            'location':         None,
            'recognization':    [],
            'type':             None,
            'tagged_user':      [],
            'url':              URL_POST.format(shortcode)
        }
        self._posts = posts
        self._url = URL_JSON_POST.format(shortcode)

        threading.Thread.__init__(self)

    def run(self):
        """
        """
        data = request(self._url, self._context)
        data = data.get('graphql', {})
        data = data.get('shortcode_media', {})

        if data:
            self._post['type'] = 'picture'
        for extract_method in Post.EXTRACT_METHODS:
            extract_method(self, data)
        self._posts.append(self._post)

    def _extract_comment(self, data):
        comments = data.get('edge_media_preview_comment', {})
        comments = comments.get('edges', [])

        for comment in comments:
            comment = comment.get('node', {})

            self._post['comment'].append({
                'text':     comment.get('text'),
                'username': comment.get('owner', {}).get('username')
            })

    def _extract_description(self, data):
        self._post['description'] = data.get('edge_media_to_caption', {})
        self._post['description'] = self._post['description'].get('edges', [])

        if self._post['description'] == []:
            return
        self._post['description'] = self._post['description'][0].get('node', {})
        self._post['description'] = self._post['description'].get('text')

    def _extract_is_video(self, data):
        if data.get('is_video'):
            self._post['type'] = 'video'

    def _extract_like(self, data):
        self._post['like'] = data.get('edge_media_preview_like', {})
        self._post['like'] = self._post['like'].get('count')

    def _extract_location(self, data):
        self._post['location'] = data.get('location', {})

        if self._post['location']:
            self._post['location'] = self._post['location'].get('name')

    def _extract_recognization(self, data):
        self._post['recognization'] = data.get('accessibility_caption', [])

        if self._post['recognization'] == []:
            self._post['type']= 'sidecar'
            recognizations = data.get('edge_sidecar_to_children', {})
            recognizations = recognizations.get('edges', [])

            for recognization in recognizations:
                recognization = recognization.get('node', {})
                recognization = recognization.get('accessibility_caption')

                self._post['recognization'].append(recognization)

    def _extract_tagged_user(self, data):
        tagged_users = data.get('edge_media_to_tagged_user', {})
        tagged_users = tagged_users.get('edges', [])

        for tagged_user in tagged_users:
            tagged_user = tagged_user.get('node', {})
            tagged_user = tagged_user.get('user', {})
            tagged_user = tagged_user.get('username')

            self._post['tagged_user'].append(tagged_user) 

    EXTRACT_METHODS = [
        _extract_comment,
        _extract_description,
        _extract_is_video,
        _extract_like,
        _extract_location,
        _extract_recognization,
        _extract_tagged_user
    ]
