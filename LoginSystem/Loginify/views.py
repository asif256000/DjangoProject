import json

from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

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


def get_all_users(request):
    users = UserDetails.objects.all()
    user_list = []
    for user in users:
        user_list.append(
            {
                "username": user.username,
                "email": user.email,
                "password": user.password,
            }
        )
    return JsonResponse(user_list, safe=False)


def get_user_by_email(request, email):
    user = get_object_or_404(UserDetails, email=email)
    return JsonResponse(
        {
            "username": user.username,
            "email": user.email,
            "password": user.password,
        }
    )


def update_user(request, email):
    user = get_object_or_404(UserDetails, email=email)
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            if "username" in data:
                user.username = data["username"]
            if "password" in data:
                user.password = data["password"]
            user.save()
            return JsonResponse(
                {
                    "message": "User updated successfully!",
                    "user": {"username": user.username, "email": user.email, "password": user.password},
                }
            )
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON data!"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Invalid request method! Use POST to update."}, status=400)


def delete_user(request, email):
    user = get_object_or_404(UserDetails, email=email)
    user.delete()
    messages.success(request, "User deleted successfully!")
    return JsonResponse({"message": "User deleted successfully!"})
