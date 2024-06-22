import requests
import json
from translate import from_en_to_ka
from timechanger import timechanger


def find_out(arg):

    key = 'b0382a9da8d31051dd5eecdc220673dc'
    url = f'https://api.openweathermap.org/data/2.5/weather?q={arg}&appid={key}&units=metric'
    response = requests.get(url)
    data = json.loads(response.text)

    latitude = data.get('coord').get('lat')
    longitude = data.get('coord').get('lon')
    condition = from_en_to_ka(data.get('weather')[0].get('description'))
    temp = data.get('main').get('temp')
    feels_like = data.get('main').get('feels_like')
    temp_min = data.get('main').get('temp_min')
    temp_max = data.get('main').get('temp_max')
    humidity = data.get('main').get('humidity')
    sunrise = timechanger(data.get('sys').get('sunrise')).split(' ')[1]
    sunset = timechanger(data.get('sys').get('sunset')).split(' ')[1]


    return (arg, latitude, longitude,temp, condition, feels_like, temp_min,
            temp_max, humidity, sunrise, sunset)

