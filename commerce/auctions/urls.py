from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("listing", views.create_Listing, name="listing"),
    path("view/<str:model>/<int:id>", views.view, name="view"),
    path("add/<str:model>/<int:id>", views.add, name="add"),
    path("remove/<str:model>/<int:id>", views.remove, name="remove"),
    path("close/<str:id>", views.close, name="close"),
    path("comment/<int:id>", views.comment, name="comment"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("category", views.category, name="category")
]
