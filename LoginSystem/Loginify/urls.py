from django.urls import path

from . import views

app_name = "loginify"

urlpatterns = [
    path("hello/", views.hello_world, name="hello_world"),
    path("signup/", views.signup, name="signup"),
    path("login/", views.login, name="login"),
]
