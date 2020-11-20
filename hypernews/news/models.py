import itertools
import os
from django.db import models
import json
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NEWS_JSON_PATH = os.path.join(os.path.dirname(BASE_DIR), 'news.json')


# Create your models here.


def accessing_data(database):
    with open(database, "r") as json_data:
        data_articles = json.load(json_data)

    return data_articles


def writing_data(database, data_as_list):
    with open(database, 'r', encoding='utf-8') as data:
        feeds = json.load(data)

    with open(database, 'w', encoding='utf-8') as json_data:
        entry = data_as_list
        feeds.append(entry)
        json.dump(feeds, json_data, indent=4)


def accessing_data_by_time_of_creation(database):
    with open(database, "r") as json_data:
        posts = json.load(json_data)
        news_dates = sorted(set([date['created'][:10] for date in posts]), reverse=True)

    return news_dates


def search_by_title(database, research):
    with open(database, "r") as json_data:
        posts = json.load(json_data)
        search_results = []
        try:
            for i in range(0, len(posts), 1):
                if research in posts[i].get("title"):
                    search_results.append(posts[i])
        except TypeError:
            search_results = posts

    return search_results


def list_of_date_search(database, research):
    with open(database, "r") as json_data:
        posts = json.load(json_data)
        search_results = []
        try:
            for i in range(0, len(posts), 1):
                if research in posts[i].get("title"):
                    search_results.append(posts[i].get("title"))
        except TypeError:
            search_results = posts

        if len(search_results) == 0:
            for i in range(0, len(posts), 1):
                search_results.append(posts[i].get("title"))

    return search_results


print(list_of_date_search(NEWS_JSON_PATH, "test"))
