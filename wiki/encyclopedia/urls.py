from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:entry>", views.entry, name="entry"),
    path("search/", views.search, name="search"),
    path("newpage/", views.newpage, name="newpage"),
    path("wiki/", views.randompage, name="randompage"),
    path("edit/<str:entry>", views.edit, name="edit")
]
