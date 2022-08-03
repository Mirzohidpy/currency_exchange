from django.views.generic import ListView
from pyexpat import model
from re import template
from urllib import response
from django.shortcuts import render
import requests
from pprint import pp, pprint
from .models import *
from django.http import HttpResponse



def test1(request, lang):
    url = 'https://cbu.uz/oz/arkhiv-kursov-valyut/json/'
    response = requests.get(url)
    data = response.json()
    print(request)
    language = ['EN', 'RU', 'UZ', 'UZC']
    currencies = []

    for d in data:
        pn = d['id']
        code = d['Code']
        Currency = d['Ccy']
        Rate = d['Rate']
        valyuta = []
        language_type = None
        Currency_country = None
        for l in language:
             if l == lang:
                language_type = l
                Currency_country = d[f'CcyNm_{l}']

        valyuta.append({
            'language': language_type,
            'language_list': language,
            'pn': pn,
            'code': code,
            'Currency': Currency,
            'Rate' : Rate,
            'country': Currency_country,
                   
        })
    
        currencies.append(valyuta)
    pprint(currencies[0])    
    return render(request, 'index.html', {'currencies':currencies})




def exchange(request):
    template = 'echange.html'
    return render(request, template)
