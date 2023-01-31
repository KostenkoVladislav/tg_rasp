import threading
import datetime

time_tgid = []
time_weather = '08:00'


def ssum(a, b):
    print(' ')


t = threading.Timer(3, ssum, args=(3, 5))
t.start()
# print('hello')


def check_wth_time():
    # функция проверки времени и отправки сообщений пользователям с актуальной погодой
    # (только для пользователей, подписавшихся на уведомления через команду /edit_weather
    global time_tgid
    now = datetime.datetime.now()
    current_time = str(now.strftime("%H:%M"))
    print(current_time)

check_wth_time()
