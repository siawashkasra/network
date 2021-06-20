
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("profile/<str:username>", views.profile, name="profile"),
    path("profile/follow/<str:username>", views.follow, name="follow"),
    path("profile/unfollow/<str:username>", views.unfollow, name="unfollow"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("following", views.following, name="following"),

     # API Routes
    path("post", views.post, name="post"),
    path("post/update/<int:id>", views.update_post, name="update_post"),
    path("post/like/<int:pid>", views.like, name="like"),
    path("post/unlike/<int:pid>", views.unlike, name="unlike"),
    # path("posts", views.load_posts, name="load_posts"),
]
