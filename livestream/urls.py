from django.urls import path

from . import views

urlpatterns = [
    path("live/", views.live_stream, name="live_stream"),
]
