from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from .models import Following, User, Post




def index(request):
    return render(request, "network/index.html")




@login_required
def profile(request, uid):
    posts = Post.objects.filter(user_id=uid).order_by("-timestamp")
    user = User.objects.filter(id=uid).first()
    return render(request, "network/profile.html", {"user": user, "posts": posts, "is_following": user.followings.filter(user_id=request.user).exists()})




def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")




def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))




def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username=username, email=email, password=password, first_name=first_name, last_name=last_name)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")




@csrf_exempt
@login_required
def post(request):
    if request.method == 'POST':

        data = json.loads(request.body)
        current_user = request.user
        try:
            post = Post(
                user=current_user, 
                content=data.get("content")
                )

            post.save()
        except Exception as e:
            return render(request, "network/index.html", {
                "message": "Something went wrong!"
            })
        
        return JsonResponse({"message": "Post created successfully."}, status=200)




def load_posts(request):
    posts = Post.objects.all()
    return JsonResponse([post.serialize() for post in posts], safe=False)




@csrf_exempt
@login_required
def follow(request, uid):
    profile = User.objects.filter(id=uid).get()

    if request.user.id == profile.id:
        return render(request, "network/profile.html", {
                "message": "You can't follow yourself!"
            })
        
    if  profile.followings.filter(user_id=request.user).exists():
         return render(request, "network/profile.html", {
                "message": "You are already following this user!"
            })  

    f = Following()
    f.save()
    f.following_id.add(profile)
    f.user_id.add(request.user)

    return HttpResponseRedirect(reverse("profile", args=[uid]))




@csrf_exempt
@login_required
def unfollow(request, uid):
    profile = User.objects.filter(id=uid).get()

    if profile.followings.filter(user_id=request.user).exists():
        f = Following.objects.filter(user_id=request.user).get()
        f.following_id.remove(profile)
        f.user_id.remove(request.user)
        
    return HttpResponseRedirect(reverse("profile", args=[uid]))