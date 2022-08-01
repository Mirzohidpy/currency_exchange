from re import template
from django.shortcuts import render
import requests
import json
from pprint import pprint


# resp = requests.get('https://v6.exchangerate-api.com/v6/95d4d844929f34f45bd0da41/latest/USD')
# data = resp.json()
# currency = data['conversion_rates']
# for i in currency.items():
#     print(list(i)[0])


def index(request):
    template = 'index.html'
    return render(request, template)
