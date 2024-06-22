import random
import requests
import json
import sqlite3
from translate import from_en_to_ka
import time
from resources import urls, city_list




def weather_generator(cities, urls):

        key = 'b0382a9da8d31051dd5eecdc220673dc'
        for city, url in zip(cities, urls):
            url_api = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={key}&units=metric'
            response = requests.get(url_api)

            if response.status_code == 200:
                data = json.loads(response.text)


                latitude = data.get('coord').get('lat')
                longitude = data.get('coord').get('lon')
                condition = from_en_to_ka(data.get('weather')[0].get('description'))
                temp = data.get('main').get('temp')
                feels_like = data.get('main').get('feels_like')
                temp_min = data.get('main').get('temp_min')
                temp_max = data.get('main').get('temp_max')
                humidity = data.get('main').get('humidity')
                sunrise = data.get('sys').get('sunrise')
                sunset = data.get('sys').get('sunset')
                pressure = data.get('main').get('pressure')
                wind = data.get('wind').get('speed')
                time.sleep(random.randint(6,10))

                yield (
                city, latitude, longitude, condition, temp, feels_like, temp_min, temp_max, humidity, sunrise,
                sunset, pressure, wind, url)




            else:
                print(f'სამწუხაროდ {city}-ის შესახებ ინფორმაცია ვერ იქნა მოძიებული. HTTP კოდია: {response.status_code}')
                break




def insert_weather_data():
    conn = sqlite3.connect('weather.db')
    cursor = conn.cursor()



    cursor.execute('''
        CREATE TABLE IF NOT EXISTS weather (
            city TEXT,
            latitude REAL,
            longitude REAL,
            condition TEXT,
            temp REAL,
            feels_like REAL,
            temp_min REAL,
            temp_max REAL,
            humidity INTEGER,
            sunrise TEXT,
            sunset TEXT,
            pressure INTEGER,
            wind REAL,
            image_url TEXT
        )
        ''')


    for weather_data in weather_generator(city_list, urls):
        cursor.execute('''
            INSERT INTO weather (city, latitude, longitude, condition, temp, feels_like, temp_min, temp_max, humidity, sunrise, sunset, pressure, wind, image_url)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', weather_data)

    conn.commit()
    conn.close()

if __name__ == '__main__':
    print(weather_generator(city_list,urls))
    print(insert_weather_data())