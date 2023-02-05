import requests
import pprint
lat = '45.0448'
lon = '38.976'
appid = "f65786135d393116416809fadae92562"
city_id = '542420'

try:
    res = requests.get('https://api.open-meteo.com/v1/forecast?latitude=45.04&longitude=38.98&hourly=temperature_2m,precipitation,windspeed_10m,winddirection_10m&daily=sunrise,sunset&timezone=Europe%2FMoscow')
    # res = requests.get("https://api.openweathermap.org/data/3.0/onecall",
    #                    params={'id': city_id, 'type': 'like', 'units': 'metric', 'APPID': appid, 'lang': 'ru',
    #                            'exclude': 'daily'})

    # res = requests.get("http://api.openweathermap.org/data/2.5/weather",
    #                    params={'id': city_id, 'type': 'like', 'units': 'metric', 'APPID': appid, 'lang': 'ru'})
    data = res.json()
    pprint.pprint(data)

except Exception as e:
    print("Exception (find):", e)
    pass
