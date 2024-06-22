import requests
import json
from datetime import datetime
import sqlite3




def currency_converter(source, destination, amount):
    key = '8c1a1c768f-e9ab238224-sfhmys'
    if source is None and destination is None and amount is None:
        return ''

    else:
        url = f'https://api.fastforex.io/convert?from={source}&to={destination}&amount={amount}&api_key={key}'
        resp = requests.get(url)
        data = json.loads(resp.text)
        answer = data.get('result').get(f'{destination.upper()}')
        return answer



def get_currencies():

    conn = sqlite3.connect('currency.db')
    c = conn.cursor()


    date = datetime.now()
    formatted_date = date.strftime("%Y-%m-%d")


    url = f'https://nbg.gov.ge/gw/api/ct/monetarypolicy/currencies/ka/json/?date={formatted_date}'
    response = requests.get(url)
    data = json.loads(response.text)[0].get('currencies')
    with open('currency.json', 'w') as file:
        json.dump(data, file, indent=3)

    c.execute('''
    CREATE TABLE IF NOT EXISTS VALUTA
    (
    Currency TEXT PRIMARY KEY,
    Code TEXT NOT NULL,
    Quantity INTEGER NOT NULL,
    Price REAL NOT NULL,
    ChangePercentage REAL NOT NULL,
    Posted_date TEXT NOT NULL,
    Posted_hour TEXT NOT NULL
    )
    ''')


    for currency in data:
        country = currency.get('name')
        code = currency.get('code')
        quantity = currency.get('quantity')
        price = float(currency.get('rateFormated').replace(',', ''))
        change_percentage = float(currency.get('diffFormated').replace(',', ''))
        posted_date = currency.get('date').split('T')[0]
        posted_hour = currency.get('date').split('T')[1].split('.')[0]




        c.execute('''
        INSERT INTO VALUTA (Currency, Code, Quantity, Price, ChangePercentage, Posted_date, Posted_hour) VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (country, code, quantity, price, change_percentage, posted_date, posted_hour))


    conn.commit()
    conn.close()


if __name__ == '__main__':
    print(get_currencies())