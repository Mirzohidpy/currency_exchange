from django.contrib import admin
from .models import *


# Register your models here.
@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    list_per_page = 20
    list_display = ("curr_list", "bank_names_left", "prices_left", "bank_names_right", "prices_right")
