#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from .configuration import *

if __name__ == '__main__':
    sys.exit(EXIT_FAILURE)

import bs4
import ssl
import tqdm
import urllib.error
import urllib.request
from .subclass import Post, Superviser
from .tools import extract_target_data, int_convertor


class Scrapper:
    def __init__(self, silent=False, until_date=DEFAULT_UNTIL_DATE):
        self._context = ssl.create_default_context()
        self._data = {'main': {}, 'posts': [], 'supervison': {}}
        self._silent = silent
        self._until_date = until_date

        self._context.check_hostname = False
        self._context.verify_mode = ssl.CERT_NONE

    def _extract_raw_data(self, user):
        def _display(self, user, state, url):
            self.display(0, f'-> {user}')
            self.display(1, f'{state} URL : {url}')

        raw_data, state = None, None
        url = INSTAGRAM_URL.format(user)

        try:
            raw_data = urllib.request.urlopen(url, context=self._context)
            raw_data = bs4.BeautifulSoup(raw_data.read(), 'html.parser')
            state = SUCCESS
        except (urllib.error.HTTPError, ConnectionResetError):
            raw_data = None
            state = FAILURE
        _display(self, user, state, url)
        return raw_data

    def _get_main_information(self, raw_data):
        def _display(self):
            self.display(1, f'{SUCCESS if len(self._data["main"].keys()) == 5 else FAILURE} Main information')
            self.display(3, f'User      : {self._data["main"]["name"]} {self._data["main"]["user_name"]}')
            self.display(3, f'Posts     : {self._data["main"]["posts"]}')
            self.display(3, f'Followers : {self._data["main"]["followers"]}')
            self.display(3, f'Following : {self._data["main"]["following"]}')

        followers, following, posts, state, user = None, None, None, None, None
        raw_data = raw_data.find_all('meta', attrs={'property': 'og:description'})
        raw_data = raw_data[0].get('content').split()
        redirect = {
            'Followers':    lambda i: self._data['main'].update(followers=int_convertor(raw_data[i - 1])),
            'Following':    lambda i: self._data['main'].update(following=int_convertor(raw_data[i - 1])),
            'Posts':        lambda i: self._data['main'].update(posts=int_convertor(raw_data[i - 1])),
            'from':         lambda i: self._data['main'].update(name=' '.join(raw_data[i+1:-1]))
        }

        for i, key in enumerate(raw_data):
            key = key.strip(', \t')
            if i > 0 and key in redirect.keys():
                redirect[key](i)
        self._data['main']['user_name'] = raw_data[-1]
        _display(self)

    def _get_posts_information(self, raw_data):
        def _display(self):
            self.display(1, f'{FAILURE if self._data["posts"] == [] else SUCCESS} Posts information')
            for post in self._data['posts']:
                if post.is_valid:
                    self.display(3, f'- {SUCCESS} {INSTAGRAM_IMAGE_URL.format(post.link)}')
                    self.display(4, f'Description        : {post.description}')
                    self.display(4, f'Location           : {post.location}')
                    self.display(4, f'Number of likes    : {post.number_likes}')
                    self.display(4, f'Number of comments : {post.number_comments}')
                    self.display(4, f'Date               : {post.date}')
                    self.display(4, f'Recognization      : {post.recognization}')
                else:
                    self.display(3, f'- {FAILURE} {INSTAGRAM_IMAGE_URL.format(post.link)}')

        raw_data = raw_data.find_all('script', attrs={'type': 'text/javascript'})
        raw_data = [rw for rw in raw_data if str(rw).find('window._sharedData = ') != -1]
        raw_data = str(raw_data).split('"node":{"__type')

        for rw in raw_data:
            link = extract_target_data(rw, 'shortcode":"')
            if link:
                self._data['posts'].append(Post(link, rw, self._until_date))
        _display(self)

    def _get_supervision_information(self):
        def _display1(self):
            self.display(1, f'{FAILURE} This person is too famous to perform surveillance.')
        def _display2(self):
            self.display(1, f'{FAILURE if self._data["supervison"]["likers"] == [] else SUCCESS} Top {TOP_SIZE} likers')
            for i, likers in enumerate(self._data['supervison']['likers'][:TOP_SIZE]):
                self.display(3, f'#{i + 1} {likers[0]} ({likers[1]} likes)')

        if self._data['main']['followers'] > 10000:
            _display1(self)
            return
        superviser = Superviser(self._context)
        with tqdm.tqdm(total=100 * len(self._data['posts'])) as pbar:
            for post in self._data['posts']:
                if post.is_valid:
                    superviser.compute_data_from_post(post, pbar)
                else:
                    pbar.update(100)
        self._data['supervison']['likers'] = superviser.get_data()
        _display2(self)

    def clear(self):
        self._data = {'main': {}, 'posts': [], 'supervison': {}}

    def display(self, order, *args, **named_args):
        if not self._silent:
            print('\t' * order, sep='', end='')
            print(*args, **named_args)

    def launch(self, user):
        raw_data = self._extract_raw_data(user)

        if raw_data:
            self._get_main_information(raw_data)
            self._get_posts_information(raw_data)
            self._get_supervision_information()

    def get_data(self):
        self._data['posts'] = [post.get_data() for post in self._data['posts']]
        return self._data.copy()
