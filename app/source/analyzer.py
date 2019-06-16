#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from ..configuration import (
    DATETIME_FORMAT,
    DATETIME_LIMIT,
    EXIT_FAILURE,
    sys,
    URL_PRIMARY,
    URL_TIMELINE
)

if __name__ == '__main__':
    sys.exit(EXIT_FAILURE)

import datetime

from .components import Post
from .tools import (
    launch_instances,
    request
)


class ProfilAnalyzer:
    """
    """

    def __init__(self, context, username):
        self.context = context
        self.username = username
        self._id = None
        self._is_private = None

    def get_primary_information(self, raw):
        """
        """
        data = raw.get('graphql', {})
        data = data.get('user', {})
        self._id = data.get('id')
        self._is_private = data.get('is_private')

        return {
            'biography':    data.get('biography'),
            'followers':    data.get('edge_followed_by', {}).get('count'),
            'following':    data.get('edge_follow', {}).get('count'),
            'id':           self._id,
            'is_private':   self._is_private,
            'name':         data.get('full_name'),
            'posts':
                data.get('edge_owner_to_timeline_media', {}).get('count'),
            'url':          URL_PRIMARY.format(self.username),
            'username':     self.username
        }

    def get_posts_information(self, raw):
        """
        """
        data = raw.get('graphql')
        datetime_limit_not_reached, posts = True, []

        while not self._is_private and data and datetime_limit_not_reached:
            data = data.get('user', {})
            data = data.get('edge_owner_to_timeline_media', {})
            end_cursor = data.get('page_info', {})
            end_cursor = end_cursor.get('end_cursor')
            data = data.get('edges', [])
            datetime_limit_not_reached = self._through_post(posts, data)

            if end_cursor is None:
                datetime_limit_not_reached = False
            if datetime_limit_not_reached:
                data = request(
                    URL_TIMELINE.format(self._id, end_cursor), self.context)
                data = data.get('data')
        return posts

    @launch_instances
    def _through_post(self, posts, data, instances=[]):

        for post_data in data:
            post_data = post_data.get('node', {})
            date = post_data.get('taken_at_timestamp')
            shortcode = post_data.get('shortcode')

            if date is None or shortcode is None:
                return False
            date = datetime.datetime.utcfromtimestamp(date)
            date = date.strftime(DATETIME_FORMAT)
            if date < DATETIME_LIMIT:
                return False
            instances.append(Post(posts, self.context, shortcode, date))
        else:
            return True
