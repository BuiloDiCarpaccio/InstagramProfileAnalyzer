#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from ..configuration import *

if __name__ == '__main__':
    sys.exit(EXIT_FAILURE)

import bs4
import json
import time
import urllib.error
import urllib.request


class Superviser:
    def __init__(self, context):
        self._context = context
        self._likers = {}

    def _extract_raw_data_in_json(self, url):
        while True:
            try:
                raw_data = urllib.request.urlopen(url, context=self._context)
                break
            except urllib.error.URLError:
                time.sleep(0.5)
        raw_data = bs4.BeautifulSoup(raw_data.read(), 'html.parser')
        return json.loads(str(raw_data))

    def compute_data_from_post(self, post, pbar):
        likes_url = INSTAGRAM_LIKES_URL[0].format(post.link)
        stop = max(1, int(post.number_likes / 50))

        for _ in range(stop):
            raw_data = self._extract_raw_data_in_json(likes_url)
            pbar.update(70 / stop)
            index = raw_data["data"]["shortcode_media"]["edge_liked_by"]["page_info"]["end_cursor"]
            for username in raw_data["data"]["shortcode_media"]["edge_liked_by"]["edges"]:
                username = username["node"]["username"]
                if username not in post.likes:
                    post.likes.append(username)
                self._likers.setdefault(username, 0)
                self._likers[username] += 1
            pbar.update(30 / stop)
            if index:
                likes_url = INSTAGRAM_LIKES_URL[1].format(post.link, index)

    def get_data(self):
        return sorted(self._likers.items(), key=lambda x: x[1], reverse=True)
