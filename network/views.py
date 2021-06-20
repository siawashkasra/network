from typing import Counter
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, request
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from .models import Following, Like, User, Post
from django.core.paginator import Paginator




def index(request):
    posts = Post.objects.all().order_by('-timestamp')
    
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "network/index.html", {'posts': page_obj})




def profile(request, username):
    user = User.objects.filter(username=username).first()
    posts = Post.objects.filter(user_id=user.id).order_by("-timestamp")
    
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    is_following = False

    if request.user.is_authenticated:
        is_following = user.followeds.filter(follower_id=request.user).exists()

    return render(request, "network/profile.html", {
        "profile": user, 
        "posts": page_obj, 
        "is_following": is_following,
        })




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

        # data = json.loads(request.body)
        current_user = request.user
        try:
            post = Post(
                user=current_user, 
                # content=data.get("content")
                content=request.POST['content']
                )

            post.save()
        except Exception as e:
            return render(request, "network/index.html", {
                "message": "Something went wrong!"
            })
        
        return redirect("index")




def load_posts(request):
    posts = Post.objects.all()
    
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return JsonResponse([post.serialize() for post in page_obj], safe=False)




@csrf_exempt
@login_required
def follow(request, username):
    profile = User.objects.filter(username=username).get()

    if request.user.id == profile.id:
        return render(request, "network/profile.html", {
                "message": "You can't follow yourself!"
            })
        
    if  profile.followeds.filter(follower_id=request.user).exists():
         return render(request, "network/profile.html", {
                "message": "You are already following this user!"
            })  

    f = Following()
    f.save()
    f.followed_id.add(profile)
    f.follower_id.add(request.user)

    return HttpResponseRedirect(reverse("profile", args=[username]))




@csrf_exempt
@login_required
def unfollow(request, username):
    profile = User.objects.filter(username=username).get()

    if profile.followeds.filter(follower_id=request.user).exists():
        follow_obj = Following.objects.filter(follower_id=request.user.id, followed_id=profile.id).get()
        follow_obj.followed_id.remove(profile)
        follow_obj.follower_id.remove(request.user)

    return HttpResponseRedirect(reverse("profile", args=[username]))




@csrf_exempt
@login_required
def following(request):
    
    posts = map(lambda following: 
                Post.objects.filter(user_id=following.followed_id.get().id).order_by("-timestamp"), 
                            Following.objects.filter(follower_id=request.user.id))

    paginator = Paginator(list(posts), 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "network/following.html", {'posts': page_obj})




@csrf_exempt
@login_required
def update_post(request, id):
    post = Post.objects.get(id=id)
    if request.method == 'PUT':
        data = json.loads(request.body)
        post.content = data.get("content")
        post.save()

        return JsonResponse({"message": "Post updated successfully."}, status=201)




@csrf_exempt
@login_required
def like(request, pid):
    if request.method == 'POST':
        post = Post.objects.filter(id=pid).get() 

        l = Like()
        l.save()
        l.user_id.add(request.user)
        l.post_id.add(post)
        return JsonResponse({"message": "Post liked successfully."}, status=201)




@csrf_exempt
@login_required
def unlike(request, pid):
    if request.method == 'PUT':
        post = Post.objects.filter(id=pid).get()
        if post.posts.filter(post_id=pid).exists():
            like_obj = Like.objects.filter(user_id=request.user.id, post_id=post.id).get()
            like_obj.post_id.remove(post)
            like_obj.user_id.remove(request.user)

            return JsonResponse({"message": "Post unliked successfully."}, status=201)

        return JsonResponse({"message": "Post was not found."}, status=404)