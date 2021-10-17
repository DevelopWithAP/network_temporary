from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from .models import User, Post, Profile, Like
import json


def index(request):
    posts = Post.objects.all().order_by("-date_posted") 
    return render(request, "network/index.html", {
        "posts": posts
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

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


@login_required
def create(request):
    if request.method == "POST":
        author = request.user
        content = request.POST["content"]
        date_posted = timezone.now()
        if content != "":
            post = Post.objects.create(author=author, date_posted=date_posted, content=content)
            return redirect("index")
        else:
            messages.info(request, "Please fill in this field")
            return redirect("create")
    else:
        return render(request, "network/create.html")
        



@login_required
def profile(request, user_id):
    profile_user = User.objects.get(pk=user_id)
    posts = Post.objects.filter(author=profile_user).order_by("-date_posted")
    
    #  Query to get all the followers of the profile_user
    followers = Profile.objects.filter(user=profile_user)

    #  Query to find all the users 'profile_user' is following
    following = Profile.objects.filter(follower=profile_user)

    #  Query to find if 'request.user' is a follower of 'profile_user'
    follower_count = Profile.objects.filter(user=profile_user, follower=request.user).count()

    #  Change DB field with a POST request
    if request.method == "POST":
        if "follow" in request.POST:
            Profile.objects.create(user=profile_user, follower=request.user)
            return redirect("profile", user_id=profile_user.id)
        elif "following" in request.POST:
            Profile.objects.filter(user=profile_user, follower=request.user).delete()
            return redirect("profile", user_id=profile_user.id)
    
    context = {
        "profile_user": profile_user,
        "posts": posts,
        "followers": followers,
        "following": following,
        "follower_count": follower_count
    }
    return render(request, "network/profile.html", context) 

@login_required
def following(request):
    user = request.user
    following = user.profile_follower.all().values("user_id")
    posts = Post.objects.filter(author__in = following).order_by("-date_posted")  
    context = {
        "following": following,
        "posts": posts
    }
    return render(request, "network/following.html", context)  

@csrf_exempt
@login_required
def edit(request, post_id):
    # Query the database for the post
    post = Post.objects.get(author=request.user, pk=post_id)
    if request.method == "GET":
        return JsonResponse(post.serialize_post())
    elif request.method == "PUT":
        data  = json.loads(request.body)
        if post.author.id != request.user.id:
            return HttpResponse(404)
        if data.get("content") is not None:
            if "content" != "":
                post.content = data["content"]
        post.save()
        return HttpResponse(status=206)

@csrf_exempt
@login_required
def like(request, post_id):
    # Query DB for the post and user
    post = Post.objects.get(pk=post_id)
    user = User.objects.get(id=request.user.id)

    # Make POST request
    if request.method == "POST":
        if user in post.likes.all():
            post.likes.remove(user)
        else:
            post.likes.add(user)

        like, created = Like.objects.get_or_create(user=user, post_id=post_id)

        if not created:
            if like.field == "Like":
                like.field = "Unlike"
            else:
                like.field = "Like"
        else:
            like.field = "Like"
        post.save()
        like.save()

        data = like.serialize()
        return JsonResponse(data)
    else:
        # GET request as a sanity check
        data = post.serialize_post()
        return JsonResponse(data)

    




