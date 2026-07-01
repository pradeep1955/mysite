from django.urls import path

from . import views

urlpatterns = [
    path("", views.event_list, name="event_list"),
    path("<int:event_id>/edit/", views.event_edit, name="event_edit"),
    path("<int:event_id>/materials/add/", views.add_material, name="add_material"),
    path("<int:event_id>/", views.event_detail, name="event_detail"),
    path("<int:event_id>/tasks/add/", views.add_task, name="add_task"),
    path("materials/<int:material_id>/edit/", views.edit_material, name="edit_material"),
    path(
        "materials/<int:material_id>/delete/",
        views.delete_material,
        name="delete_material",
    ),
]
