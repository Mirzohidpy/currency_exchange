"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import  function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from inspect import Parameter
from django.contrib import admin
from django.urls import path, re_path, include
from main_body import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.converter, name='index'),
    path('language/<str:lang>', views.test1, name='language'),
    path('currency/<str:currency>', views.currencys, name='currency'),
    path('members/', include('django.contrib.auth.urls')),
    path('members/', include('members.urls')),
    path('json-converter/', views.json_converter, name='json_converter'),
]
