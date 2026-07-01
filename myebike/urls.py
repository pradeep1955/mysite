from django.urls import path

from . import views

app_name = "myebike"
urlpatterns = [
    path("", views.myebike_home, name="myebike_home"),
    path("log_location/", views.log_location, name="log_location"),
    path("api/start_new_ride/", views.start_new_ride, name="start_new_ride"),
    path(
        "api/generate_story/<int:ride_id>/",
        views.generate_ride_story,
        name="generate_ride_story",
    ),
]
