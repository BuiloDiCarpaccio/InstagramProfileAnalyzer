#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import requests
import urllib.request
import urllib.parse
import urllib.error
from bs4 import BeautifulSoup
import ssl
import math
import json
import time
from datetime import datetime


def print_percentage(total, actual):
    percentage_actual = int(actual / total * 100)
    eta = "["
    for i in range(0, percentage_actual):
        eta += "-"
    for j in range(0, 100 - percentage_actual):
        eta += " "
    eta += "] ~ "
    eta += str(percentage_actual) + '%'
    print(eta, end='\r')

class InstaInfoScraper:
    def __init__(self):
        pass

    liked_by_url = 'https://www.instagram.com/graphql/query/?query_hash=d5d763b1e2acf209d62d22d184488e57&variables={"shortcode":"'
    comment_url = 'https://www.instagram.com/graphql/query/?query_hash=477b65a610463740ccdb83135b2014db&variables={"shortcode":"'
    end_comment_url ='","child_comment_count":3,"fetch_comment_count":40,"parent_comment_count":24,"has_threaded_comments":true}'
    _posts_data = []
    _likers = dict()

    def get_json_from_url(self, url):
        status = 1
        while status == 1:
            try:
                pics_comment = urllib.request.urlopen(url, context=self.ctx).read()
            except:
                print("error")
                time.sleep(5)
                continue
            status = 0
        status = 1
        soup = BeautifulSoup(pics_comment, 'html.parser')
        soup = json.loads(str(soup))
        return soup

    class PhotoAnalyzer:

        def get_comment(self):
            eta = 36
            for pics_data in InstaInfoScraper._posts_data:
                new_url = self.comment_url + pics_data["link"] + self.end_comment_url
                pics_data["comment"] = dict()
                soup = self.get_json_from_url(new_url)
                pics_data["tagged_user"] = []
                for tagged in soup["data"]["shortcode_media"]["edge_media_to_tagged_user"]["edges"]:
                    pics_data["tagged_user"].append(tagged["node"]["user"]["username"])
                print(pics_data["tagged_user"])
                for truc in soup["data"]["shortcode_media"]["edge_media_to_parent_comment"]["edges"]:
                    if truc["node"]["owner"]["username"] in pics_data["comment"]:
                        pics_data["comment"][truc["node"]["owner"]["username"]].append(truc["node"]["text"])
                    else:
                        pics_data["comment"][truc["node"]["owner"]["username"]] = [truc["node"]["text"]]
                # for j in range(0, len(soup["data"]["shortcode_media"]["edge_media_to_parent_comment"]["edges"])):
                #     if soup["data"]["shortcode_media"]["edge_media_to_parent_comment"]["edges"][j]["node"]["owner"]["username"] in pics_data["comment"]:
                #         pics_data["comment"][soup["data"]["shortcode_media"]["edge_media_to_parent_comment"]["edges"][j]["node"]["owner"]["username"]].append(soup["data"]["shortcode_media"]["edge_media_to_parent_comment"]["edges"][j]["node"]["text"])
                #     else:
                #         pics_data["comment"][soup["data"]["shortcode_media"]["edge_media_to_parent_comment"]["edges"][j]["node"]["owner"]["username"]] = [soup["data"]["shortcode_media"]["edge_media_to_parent_comment"]["edges"][j]["node"]["text"]]
                eta += 1
                print_percentage(48, eta)

        def pic_by_pic(self, url):
            eta = 24
            end_cursor = ""
            for pics_data in InstaInfoScraper._posts_data:
                new_url = self.liked_by_url + pics_data["link"] + '","include_reel":true,"first":50}'
                pics_data["likers"] =[]
                for count in range (0, math.ceil(int(pics_data["nb_like"])/50)):
                    soup = ""
                    soup = self.get_json_from_url(new_url)
                    for j in range(0, len(soup["data"]["shortcode_media"]["edge_liked_by"]["edges"])):
                        end_cursor = soup["data"]["shortcode_media"]["edge_liked_by"]["page_info"]["end_cursor"]
                        if soup["data"]["shortcode_media"]["edge_liked_by"]["edges"][j]["node"]["username"] in self._likers:
                            self._likers[soup["data"]["shortcode_media"]["edge_liked_by"]["edges"][j]["node"]["username"]] += 1
                        else:
                            self._likers[soup["data"]["shortcode_media"]["edge_liked_by"]["edges"][j]["node"]["username"]] = 1
                        pics_data["likers"].append(soup["data"]["shortcode_media"]["edge_liked_by"]["edges"][j]["node"]["username"])
                    eta += 1
                    print_percentage(48, eta)
                    if end_cursor is not None:
                        new_url = self.liked_by_url + pics_data["link"] + '","include_reel":true,"first":50,"after":"'+ end_cursor + '"}'
                        soup = self.get_json_from_url(new_url)
                time.sleep(1)
            self._likers = sorted(self._likers.items(), key=lambda x: x[1], reverse=True)

    def get_var_data(self, paraph, var):
        start = paraph.find(var) + len(var)
        if start == len(var) - 1:
            return "Not found"
        end = paraph.find(',', start)
        paraph = paraph[start:end].replace('"', "")
        paraph = paraph.replace('}', "")
        paraph = paraph.replace(']', "")
        return paraph

    def get_post_info(self, post_data):
        eta = 12
        for i in post_data:
            link = self.get_var_data(str(i), "shortcode\":\"")
            if link == "Not found":
                continue
            self._posts_data.append({"link": link})
            self._posts_data[-1]["timestamp"] = self.get_var_data(str(i), "taken_at_timestamp\":")
            self._posts_data[-1]["timestamp"] = datetime.utcfromtimestamp(int(self._posts_data[-1]["timestamp"])).strftime('%d-%m-%Y %H:%M:%S')
            self._posts_data[-1]["accessibility_caption"] = self.get_var_data(str(i), 'accessibility_caption":"')
            self._posts_data[-1]["nb_like"] = self.get_var_data(str(i), '"edge_media_preview_like":{"count":')
            self._posts_data[-1]["tagged_users"] = self.get_var_data(str(i), "")
            eta += 1
            print_percentage(48, eta)

    def get_info(self, url):
        html = urllib.request.urlopen(url, context=self.ctx).read()
        soup = BeautifulSoup(html, 'html.parser')
        data = soup.find_all('meta', attrs={'property': 'og:description'})
        script = soup.find_all('script', attrs={'type': 'text/javascript'})
        i = 0
        while i < len(script):
            if str(script[i]).find("window._sharedData = ") == -1:
                script.pop(i)
                i -= 1
            i += 1
        script = str(script).split('"node":{"__type')
        text = data[0].get('content').split()
        user = '%s %s %s' % (text[-3], text[-2], text[-1])
        followers = text[0]
        following = text[2]
        posts = text[4]
        print('User:', user)
        print('Followers:', followers)
        print('Following:', following)
        print('Posts:', posts)
        print('---------------------------')
        return (script)

    def scrap(self):
        self.ctx = ssl.create_default_context()
        self.ctx.check_hostname = False
        self.ctx.verify_mode = ssl.CERT_NONE

        with open('users.txt') as f:
            self.content = f.readlines()
        self.content = [x.strip() for x in self.content]
        for url in self.content:
            post_data = self.get_info(url)
            print_percentage(48, 12)
            post_parsed = self.get_post_info(post_data)
            print_percentage(48, 24)
            time.sleep(2)
            self.PhotoAnalyzer.pic_by_pic(self, url)
            print_percentage(48, 38)
            self.PhotoAnalyzer.get_comment(self)
            print_percentage(48, 48)
            print(self._posts_data)
            print(self._likers)


if __name__ == '__main__':
    obj = InstaInfoScraper()
    obj.scrap()
