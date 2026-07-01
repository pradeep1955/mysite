from django.urls import path

from . import views
from .views import chatbot_view, receive_sensor_data

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("chat/", chatbot_view, name="chatbot"),
    path("sensor/", receive_sensor_data, name="sensor"),
]
