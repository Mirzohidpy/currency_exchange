from contextlib import contextmanager
from html.entities import html5
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
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from bs4 import BeautifulSoup as b
from .translate import to_latin
import sqlite3 as sql



def test1(request, lang):
    url = 'https://cbu.uz/oz/arkhiv-kursov-valyut/json/'
    response = requests.get(url)
    data = response.json()
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
    return render(request, 'index.html', {'currencies':currencies})


@csrf_exempt
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
        "apikey": "aE9dlfzS73DtaIUWcW6eGppSe2hnNhmA"
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
    header= {
         "apikey": "aE9dlfzS73DtaIUWcW6eGppSe2hnNhmA"
    }

    response2 = requests.request("GET", url2, headers=header, data = payload2)
    result2 = response2.json()
    for currency in result2.values():
        if isinstance(currency, dict):
            for smth in currency.keys():
                currency_list.append(smth)

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


def parsing(request, currency):
    response = requests.get('https://bank.uz/currency/dollar-ssha')
    html = response.text
    soup = b(html, 'html.parser')
    data_curr = soup.find('ul', class_='nav nav-tabs')
    curr = data_curr.find_all('li', class_='nav-item')
    data_item = soup.find('div', id='tab1')
    bank_namess = html
    bank_names = []
    prices = []
    curr_list = []
    for cur in curr:
        cur_name = cur.find('span', class_='medium-text').get_text(strip=True)
        curr_list.append(cur_name)
            
    for cur_list in curr_list:
        if cur_list == currency:
            divs = data_item.find('div', id=f'best_{cur_list}')  
            bank_namess = divs.find_all('div', class_='bc-inner-block-left-text')
            price_items = divs.find_all('div', class_='bc-inner-block-left-texts')
            print(price_items)

    for bank_name in bank_namess:
        names = bank_name.find('span', class_='medium-text').get_text(strip=True)
        bank_names.append(names)
    
    for amount in price_items:
        narx = amount.find('span', class_='green-date').get_text(strip=True)
        prices.append(narx)


    # conn = sql.connect('database.db')
    # c = conn.cursor()

    # c.execute('''
    #     CREATE TABLE IF NOT EXISTS bankitems (
    #     bank_id INTEGER PRIMARY KEY AUTOINCREMENT,
    #     bank_name TEXT,
    #     bank_prices TEXT
    #  )
    # ''')

    # c.executemany('''
    #     INSERT INTO president(bank_id, bank_name, bank_prices)
    #     VALUES (?, ?, ?)
    # ''', bank_names, prices)
    # conn.commit()
    # conn.close()

    context = {
        'curr_list': curr_list,
        'bank_names': bank_names,
        'prices': prices
    }

    template = 'parsed_data.html'
    return render(request, template, context)   



