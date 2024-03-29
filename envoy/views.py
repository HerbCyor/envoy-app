from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required


def index(request):
    return render(request, "index.html")


def login(request):

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = auth.authenticate(username=username, password=password)

        if user:
            auth.login(request, user)
            return redirect("geolocation")

    return render(request, "index.html")


@login_required(login_url="login")
def logout(request):
    auth.logout(request)
    return redirect("index")
