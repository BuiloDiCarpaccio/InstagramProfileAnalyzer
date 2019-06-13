#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from ..configuration import *

if __name__ == '__main__':
    sys.exit(EXIT_FAILURE)

import datetime
from ..tools import extract_target_data


class Post:
    def __init__(self, link, raw_data, until_date):
        self._until_date = until_date
        self.comments = []
        self.date = '1970-01-01 00:00:00'
        self.description = ''
        self.is_valid = True
        self.likes = []
        self.link = link
        self.location = ''
        self.number_comments = 0
        self.number_likes = 0
        self.recognization = ''

        self._extract_post_information(raw_data)

    def _extract_post_information(self, raw_data):
        if self.is_valid:
            self.date = int(extract_target_data(raw_data, '"taken_at_timestamp":'))
            self.date = datetime.datetime.utcfromtimestamp(self.date)
            self.date = self.date.strftime('%Y-%m-%d %H:%M:%S')
            self.description = self._inside_extract_target_data(raw_data, ('"edge_media_to_caption":{', '"text":"'))
            self.location = self._inside_extract_target_data(raw_data, ('"location":{', '"name":"'))
            self.number_comments = int(extract_target_data(raw_data, '"edge_media_to_comment":{"count":'))
            self.number_likes = int(extract_target_data(raw_data, '"edge_media_preview_like":{"count":'))
            self.recognization = extract_target_data(raw_data, '"accessibility_caption":"')
            self.is_valid &= self.date >= self._until_date

    def _inside_extract_target_data(self, raw_data, keys):
        for key in keys[:-1]:
            index = raw_data.find(key)
            if index == -1:
                return None
            raw_data = raw_data[index + len(key):]
        return extract_target_data(raw_data, keys[-1])

    def get_data(self):
        return {
            'comments':         self.comments,
            'date':             self.date,
            'description':      self.description,
            'likes':            self.likes,
            'link':             self.link,
            'location':         self.location,
            'number_comments':  self.number_comments,
            'number_likes':     self.number_likes,
            'recognization':    self.recognization
        }
