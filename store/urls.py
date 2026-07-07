from django.urls import path

from . import views

app_name = "store"

urlpatterns = [
    path("", views.StoreHomeView.as_view(), name="home"),
    path("products/", views.ProductListView.as_view(), name="product-list"),
    path("kits/<slug:slug>/", views.KitDetailView.as_view(), name="kit-detail"),
    path("kits/<slug:slug>/preorder/", views.PreorderCreateView.as_view(), name="preorder"),
]
