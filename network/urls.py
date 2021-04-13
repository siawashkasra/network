
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("profile/<int:uid>", views.profile, name="profile"),
    path("profile/follow/<int:uid>", views.follow, name="follow"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),

     # API Routes
    path("post", views.post, name="post"),
    path("posts", views.load_posts, name="load_posts"),
]
