from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("listings/<str:name>", views.listing, name="listing"),
    path("create", views.create, name = "create"),
    path("listings/<str:name>/close", views.close, name="close"),
    path("listings/<str:name>/add", views.add, name='add'),
    path("<str:user>/watchlist", views.watchlist, name='watchlist'),
    path("categories", views.categories, name = 'categories'),
    path("<str:cat>", views.category, name = 'category'),
    path("listings/<str:name>/comment", views.comment, name = 'comment')
]
