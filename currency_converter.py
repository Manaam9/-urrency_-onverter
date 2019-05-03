from bs4 import BeautifulSoup
from decimal import Decimal
import requests


def convert(amount, cur_from, cur_to, date):

    """
    Function gets amount of value that you have(amount), name of the currency
    that you have(cur_from), name of the currency that you want to transfer to(cur_to)
    (according to the abbreviations of Central Bank of Russian Federation API),
    the date for which you want to get the calculation and the request to connect to the API (requests).
    """

    response = requests.get('http://www.cbr.ru/scripts/XML_daily.asp', {'date_req': date})
    soup = BeautifulSoup(response.content, 'lxml')
    currency_tree = soup.find('valcurs')
    currency_val = {}
    result = Decimal('0.0000')

    for cur in currency_tree:
        try:
            if cur.find('charcode').string == cur_from or cur.find('charcode').string == cur_to:
                currency_val[cur.charcode.string] = (cur.nominal.string, cur.value.string.replace(',', '.'))
        except AttributeError :
            continue

    if cur_from == 'RUR' and cur_to != 'RUR':
        result = Decimal(amount) * Decimal(currency_val[cur_to][0]) / Decimal(currency_val[cur_to][1])

    elif cur_to == 'RUR' and cur_from != 'RUR':
        result = Decimal(amount) * Decimal(currency_val[cur_from][1]) / Decimal(currency_val[cur_from][0])

    elif cur_from == cur_to:
        result = Decimal(amount)

    else:
        cur_from_rub = Decimal(amount) * Decimal(currency_val[cur_from][1]) / Decimal(currency_val[cur_from][0])
        result = cur_from_rub * Decimal(currency_val[cur_to][0]) / Decimal(currency_val[cur_to][1])

    result = Decimal(result).quantize(Decimal('1.0000'))  # не забыть про округление до 4х знаков после запятой

    return result
