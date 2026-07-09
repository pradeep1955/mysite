from django.urls import path

from . import views

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("privacy/", views.PrivacyPolicyView.as_view(), name="privacy"),
]
