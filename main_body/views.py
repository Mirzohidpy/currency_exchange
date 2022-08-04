from contextlib import contextmanager
from unittest import result
from django.forms import BooleanField
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


def converter(request):
    first = None
    second = None
    amount1 = None
    if request.method == 'POST':
        first = request.POST.get('first')
        second = request.POST.get('second')
        amount1 = request.POST.get('amount1')
    url1 = f"https://api.apilayer.com/exchangerates_data/convert?to={second}&from={first}&amount={amount1}"
    payload1 = {}
    headers= {
        "apikey": "i41QoylmY1AzJu7ZICbTnquVcWR7BdMP"
    }

    response1 = requests.request("GET", url1, headers=headers, data = payload1)
    result1 = response1.json()
    list_data = []
    date = None
    rate = None
    items = None
    url2 = "https://api.apilayer.com/exchangerates_data/symbols"
    currency_list = []
    payload2 = {}
    headers= {
         "apikey": "tPohXG3CMoH2azBrRdaxlWrMoJBTSs45"
    }

    response2 = requests.request("GET", url2, headers=headers, data = payload2)
    result2 = response2.json()
    for currency in result2.values():
        # currency_list.append(currency)
        if isinstance(currency, dict):
            for smth in currency.keys():
                currency_list.append(smth)
    
    # for currencies in currency_list:
    #     if isinstance(currencies, dict):
    #         list_data.remove(currencies)

    for data in result1.values():
        list_data.append(data)
    

    for items in list_data:
        if isinstance(items, bool):
            list_data.remove(items)
        elif isinstance(items, str):
            date = items
        elif isinstance(items, float) or isinstance(items, int):
            rate = items  

    context={
        'rate': rate,
        'date': date,
        'currency': currency_list
    }    
    template = 'echange.html'
    return render(request, template, context)




