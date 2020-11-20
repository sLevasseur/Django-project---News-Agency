import datetime
import os
import random

from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect
from django.views.generic.base import View
from .models import accessing_data,list_of_date_search, accessing_data_by_time_of_creation, writing_data, search_by_title
from django.conf import settings
from django.conf.urls.static import static


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NEWS_JSON_PATH = os.path.join(os.path.dirname(BASE_DIR), 'news.json')


# Create your views here.

class Homepage(View):
    def get(self):
        html = "Coming soon"
        return html


class Main_view(View):
    def get(self, request):
        data_to_process = accessing_data(NEWS_JSON_PATH)
        ordered_timestamps = accessing_data_by_time_of_creation(NEWS_JSON_PATH)
        search_user = request.GET.get("q")
        search_data = search_by_title(NEWS_JSON_PATH, search_user)
        title_found = list_of_date_search(NEWS_JSON_PATH, search_user)

        if len(search_data) == len(data_to_process) or len(search_data) == 0:
            context = {"data": data_to_process, "ordered_timestamps": ordered_timestamps,
                       "search_user": search_user, "title": title_found}
        else:
            context = {"data": search_data, "ordered_timestamps": ordered_timestamps,
                       "search_user": search_user, "title": title_found}

        return render(request, "news/main_article_view.html", context=context)


class Article_view(View):
    def get(self, request, post_id):
        data_to_process = accessing_data(NEWS_JSON_PATH)
        error404 = ""
        title_date_text = []
        context = {}

        for i in range(0, len(data_to_process), 1):
            if data_to_process[i].get("link") == post_id:
                title_date_text.append(data_to_process[i].get("title"))
                title_date_text.append(data_to_process[i].get("created"))
                title_date_text.append(data_to_process[i].get("text"))
                error404 = "False"
                title = title_date_text[0]
                date = title_date_text[1]
                text = title_date_text[2]
                context = {"title": title, "date": date, "text": text}
                break
            else:
                error404 = "True"

        if error404 == "True":
            raise Http404
        else:
            return render(request, "news/article.html", context=context)


class NewsCreate(View):
    def get(self, request):
        return render(request, "news/create_news.html")

    def post(self, request):
        id_link = str(random.sample(range(9), 4)).replace(", ", "").replace("[", "").replace("]", "")
        data_list = {"created": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                     "text": request.POST.get("text"),
                     "title": request.POST.get("title"),
                     "link": int(id_link)}
        writing_data(NEWS_JSON_PATH, data_list)
        return redirect("/news/")
