from django.urls import path
from django.urls.resolvers import URLPattern
from . import views

app_name = "users"
urlpatterns: list[URLPattern] = [
    path("delete/", views.delete_account, name="delete_account"),
    path("avatar/delete/", views.delete_avatar, name="delete_avatar"),
]