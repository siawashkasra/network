
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("profile/<str:username>", views.profile, name="profile"),
    path("profile/follow/<int:uid>", views.follow, name="follow"),
    path("profile/unfollow/<int:uid>", views.unfollow, name="unfollow"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("following", views.following, name="following"),

     # API Routes
    path("post", views.post, name="post"),
    path("post/update/<int:id>", views.update_post, name="update_post"),
    # path("posts", views.load_posts, name="load_posts"),
]
