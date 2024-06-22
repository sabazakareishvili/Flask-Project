import requests
import json
source = 'GEL'
destination = 'EUR'
amount = 100
key = '8c1a1c768f-e9ab238224-sfhmys'
url = f'https://api.fastforex.io/convert?from={source}&to={destination}&amount={amount}&api_key={key}'
resp = requests.get(url)
data = json.loads(resp.text)

print(data)