from django.http import request
from django.urls import path
from .views import NewsCreate, Homepage, Main_view, Article_view
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', Homepage.as_view(), name='main'),
    path('news/', Main_view.as_view(), name='main'),
    # path('news/q=<str:search>', Main_view.as_view(), name='main'),
    path('news/<int:post_id>/', Article_view.as_view(), name="news"),
    path("news/create/", NewsCreate.as_view(), name="news_create"),

]
urlpatterns += static(settings.STATIC_URL)
