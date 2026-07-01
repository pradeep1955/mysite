from django.urls import path

from . import views
from .views import stock_predict_api

urlpatterns = [
    path("", views.stock_chart, name="stock_chart"),
    path("internet-test/", views.test_internet, name="internet-test"),
    path("api/predict/", stock_predict_api, name="stock_predict"),
]
