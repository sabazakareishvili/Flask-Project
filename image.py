import requests


def get_image_url(city):

    key = '44333800-a40172f429ed57fe2e4f7e00c'
    url = f'https://pixabay.com/api/?key={key}&q={city}'
    response = requests.get(url)
    image_source = response.json().get('hits')[0].get('webformatURL')

    return image_source


