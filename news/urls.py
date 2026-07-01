from django.urls import path

from . import views

urlpatterns = [
    path("", views.show_news, name="news_home"),
]
