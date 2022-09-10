from django.http import JsonResponse
from django.shortcuts import render
import requests
from .models import *
from django.views.decorators.csrf import csrf_exempt
from bs4 import BeautifulSoup as b
from pprint import pprint
from datetime import datetime
import json


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
            'Rate': Rate,
            'country': Currency_country,

        })

        currencies.append(valyuta)
    return render(request, 'index.html', {'currencies': currencies})


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
    headers = {
        "apikey": "QCGWr2sEt19zBmXXP46GXWc1G1oSmVId"
    }

    response1 = requests.request("GET", url1, headers=headers, data=payload1)
    result1 = response1.json()
    list_data = []
    date = None
    rate = None
    items = None
    url2 = "https://api.apilayer.com/exchangerates_data/symbols"
    currency_list = []
    payload2 = {}
    header = {
        "apikey": "QCGWr2sEt19zBmXXP46GXWc1G1oSmVId"
    }

    response2 = requests.request("GET", url2, headers=header, data=payload2)
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

    context = {
        'rate': rate,
        'date': date,
        'currency': currency_list
    }
    template = 'echange.html'
    return render(request, template, context)


@csrf_exempt
def json_converter(request):
    print('salom')
    first = None
    second = None
    amount1 = None
    if request.method == 'POST':
        data = json.loads(request.body)
        first = data.get('first')
        second = data.get('second')
        amount1 = data.get('value')
    url1 = f"https://api.apilayer.com/exchangerates_data/convert?to={second}&from={first}&amount={amount1}"
    payload1 = {}
    headers = {
        "apikey": "QCGWr2sEt19zBmXXP46GXWc1G1oSmVId"
    }

    response1 = requests.request("GET", url1, headers=headers, data=payload1)
    result1 = response1.json()
    list_data = []
    date = None
    rate = None
    items = None
    url2 = "https://api.apilayer.com/exchangerates_data/symbols"
    currency_list = []
    payload2 = {}
    header = {
        "apikey": "QCGWr2sEt19zBmXXP46GXWc1G1oSmVId"
    }

    response2 = requests.request("GET", url2, headers=header, data=payload2)
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

    context = {
        'rate': rate,
    }
    return JsonResponse(context)


# # TODO: Parse_data funksiyani yozish
# def parse_currencies():
#     #TODO: Parse qilingan ma'lumotni qaytarish.
#     return
def parsing(request, currency):
    # last_update_date = LastUpdatedDate.objects.first()
    # # TODO: Check if the lates element in the LastUpdatedDate is older than
    # if last_update_date - datetime.now() > 24:
    #     # TODO: Agar ma'lumot eski bo'sa Parse qisin
    #     currencies = parse_currencies()
    #     #TODO: write currencies to DB
    #     LastUpdatedDate.objects.create(date=datetime.now())
    # else:
    #     # TODO: agar ma'lumot yangi bo'sa DB dan obchiqsin
    #     currencies = Currency.objects.all

    response = requests.get('https://bank.uz/currency/dollar-ssha')
    html = response.text
    soup = b(html, 'html.parser')
    data_curr = soup.find('ul', class_='nav nav-tabs')
    curr = data_curr.find_all('li', class_='nav-item')
    data_item = soup.find('div', id='tab1')
    bank_name_left = []
    bank_name_right = []
    prices_left = []
    prices_right = []
    curr_list = []

    for cur in curr:
        cur_name = cur.find('span', class_='medium-text').get_text(strip=True)
        curr_list.append(cur_name)

    for cur_list in curr_list:
        if cur_list == currency:
            divs = data_item.find('div', id=f'best_{cur_list}')
            bank_names_left = divs.find('div', class_='bc-inner-block-left')
            bank_names_right = divs.find('div', class_='bc-inner-blocks-right')
            left_texts = bank_names_left.find_all('div', class_='bc-inner-block-left-texts')
            right_texts = bank_names_right.find_all('div', class_='bc-inner-block-left-texts')
            for left_text in left_texts:
                names1 = left_text.find('span', class_='medium-text').get_text(strip=True)
                price1 = left_text.find('span', class_='green-date').get_text(strip=True)
                bank_name_left.append(names1)
                prices_left.append(price1)
            for right_text in right_texts:
                names = right_text.find('span', class_='medium-text').get_text(strip=True)
                price = right_text.find('span', class_='green-date').get_text(strip=True)
                bank_name_right.append(names)
                prices_right.append(price)

            # obj.set_arguments(cur_list, )

    context = {
        'curr_list': curr_list,
        'bank_names_left': bank_name_left,
        'bank_names_right': bank_name_right,
        'prices_left': prices_left,
        'prices_right': prices_right,
    }

    # pprint(context)

    # for category in data:
    #     for bank_price_info in category:
    #         price = bank_price_info['price']
    #         bank = bank_price_info['']

    # arr = []
    # for i in context.values():
    #     arr.append(i)
    #
    # for cur_list in arr[0]:
    #     if request.method == 'GET' and cur_list == currency:
    #         for i in range(len(arr[1])):
    #             obj = Currency()
    #             obj.set_arguments(cur_list, arr[1][i], arr[2][i], arr[3][i], arr[4][i])
    #             obj.save()
    # print(obj)
    # obj.save()
    template = 'parsed_data.html'
    return render(request, template, context)


def currencys(request, currency):
    curr_list = ['USD', 'RUB', 'EUR', 'GBP', 'JPY', 'KZT']
    bank_names_left = []
    bank_names_right = []
    prices_left = []
    prices_right = []
    allCurrency = Currency.objects.all()
    context = {'currency':allCurrency}
    for i in curr_list:
        if i == currency:
            for j in allCurrency:
                # print(j.curr_list)
                if i == j.curr_list:
                    bank_names_left.append(j.bank_names_left)
                    bank_names_right.append(j.bank_names_right)
                    prices_left.append(j.prices_left)
                    prices_right.append(j.prices_right)

    context = {
        'curr_list': curr_list,
        'bank_names_left': bank_names_left,
        'bank_names_right': bank_names_right,
        'prices_left': prices_left,
        'prices_right': prices_right,
    }

    return render(request, 'parsed_data.html', context)
