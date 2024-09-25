from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import redirect, render

from .models import UserDetails


# Create your views here.
def hello_world(request):
    return HttpResponse("Hello, world!")


def signup(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]

        if UserDetails.objects.filter(username=username).exists():
            messages.error(request, "Username already exists!")
            return redirect("loginify:signup")
        elif UserDetails.objects.filter(email=email).exists():
            messages.error(request, "Email already exists!")
            return redirect("loginify:signup")
        else:
            user = UserDetails(username=username, email=email, password=password)
            user.save()
            messages.success(request, "Account created successfully!")
            return redirect("loginify:login")
    return render(request, "signup.html")


def login(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]

        if UserDetails.objects.filter(email=email, password=password).exists():
            messages.success(request, "Login successful!")
            return render(request, "success.html")
        else:
            messages.error(request, "Invalid credentials!")
            return redirect("loginify:login")
    return render(request, "login.html")
