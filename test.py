import threading
import datetime
import time
import requests
from configuration import *

time_tgid = []
time_weather = '20:13'


def weather_send():
    print('Погода на сегодня')


def check_with_time():
    global time_weather
    # функция проверки времени и отправки сообщений пользователям с актуальной погодой
    # (только для пользователей, подписавшихся на уведомления через команду /edit_weather
    global time_tgid
    while True:
        now = datetime.datetime.now()
        current_time = str(now.strftime("%H:%M"))
        print(current_time)
        if current_time == time_weather:
            weather_send()
            time.sleep(61)
        else:
            time.sleep(15)


# t = threading.Thread(target = check_with_time)
# t.start()

s_city = "Petersburg,RU"
city_id = 0
appid = "f65786135d393116416809fadae92562"
try:
    res = requests.get("http://api.openweathermap.org/data/2.5/find",
                       params={'q': s_city, 'type': 'like', 'units': 'metric', 'APPID': appid})
    data = res.json()
    cities = ["{} ({})".format(d['name'], d['sys']['country'])
              for d in data['list']]
    print("city:", cities)
    city_id = data['list'][0]['id']
    print('city_id=', city_id)
except Exception as e:
    print("Exception (find):", e)
    pass
