from django.urls import path

from . import views

urlpatterns = [
    path("timer/", views.get_timer_config),
]
