
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
import requests
from .models import User
from .forms import UserRegisterForm, UserLoginForm


def user_form(request):
    context = {
        "login_form": UserLoginForm(),
        "register_form": UserRegisterForm()
    }
    return render(request, "registration/user_form.html", context=context)


def user_register(request):

    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration was successful.")
            return redirect("user_form")
        messages.error(
            request, f"Unsuccessful registration. Invalid information.\n\n{form.error_messages}")

    context = {
        "login_form": UserLoginForm(request.POST),
        "register_form": UserRegisterForm()
    }

    return render(request, "registration/user_form.html", context=context)


def user_login(request):
    if request.user.is_authenticated:
        return redirect('index')
    form = UserLoginForm(request.POST)
    if form.is_valid():
        User.objects.get(username=form.POST.username)
        login(request, user)
        return redirect("index")
    else:
        messages.error(request, f"Error:\n\n{ form.error_messages }")
        return redirect('user_form')



# def country_names(request):
#     url = "https://api.apilayer.com/exchangerates_data/symbols"
#     data = []
#     payload = {}
#     headers = {
#         "apikey": "I87q645s98SI2L9ICa6FFajyRQZyzBvj"
#     }
#
#     response = requests.request("GET", url, headers=headers, data=payload)
#     results = response.json()
#     for result in results.values():
#         if isinstance(result, dict):
#             for res in result.values():
#                 data.append(res)
#     context = {
#         'country_names': data
#     }
#     print(data)
#     template = "registration/user_form.html"
#     return render(request, template, context=context)


