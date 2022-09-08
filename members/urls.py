from django.urls import path
from .views import *

urlpatterns = [
    path("user-form/", user_form, name="user_form"),
    path("register/", user_register, name="user_register"),
    path("login/", user_login, name="user_login")
]
