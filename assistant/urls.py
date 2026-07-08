from django.urls import path

from . import views

app_name = "assistant"

urlpatterns = [
    path("ask/", views.AskView.as_view(), name="ask"),
]
