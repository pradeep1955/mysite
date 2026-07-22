from django.urls import path

from . import views

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("api/sensor-data/", views.sensor_data_api, name="sensor-data-api"),
    path("privacy/", views.PrivacyPolicyView.as_view(), name="privacy"),
    path("subscribe/", views.SubscribeView.as_view(), name="subscribe"),

]
