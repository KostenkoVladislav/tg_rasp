import telebot
from telebot import types
import datetime
import pprint
import json
from configuration import *
from read_write_weather import *
import threading
import time
import requests

bot = telebot.TeleBot(mconf('tg'))
pprint.pprint('ok')
Migalka = 0  # 1- числитель
group = -1
time_tgid = []  # список тг айди для напоминания о погоде
time_weather = '07:00'


def weather_send():
	weather_today = {}
	try:
		res = requests.get(
			'https://api.open-meteo.com/v1/forecast?latitude=45.04&longitude=38.98&hourly=temperature_2m,'
			'precipitation,windspeed_10m,winddirection_10m&daily=sunrise,sunset&timezone=Europe%2FMoscow')
		data = res.json()
		weather_today = {
			'weather_0': data['hourly']['temperature_2m'][0],
			'weather_6': data['hourly']['temperature_2m'][6],
			'weather_9': data['hourly']['temperature_2m'][9],
			'weather_12': data['hourly']['temperature_2m'][12],
			'weather_15': data['hourly']['temperature_2m'][15],
			'weather_18': data['hourly']['temperature_2m'][18],
			'weather_21': data['hourly']['temperature_2m'][21],
		}

	except Exception as e:
		print("Exception (find):", e)

	if len(weather_today) == 0:
		for i in weather_file('r'):
			if 100000000 < int(i) < 999999999:
				bot.send_message(int(i), f'<b>Доброго утра, сорри но погоды сегодня не будет\n'
				                         f'Сегодня без извинений, так что тыкните @SaMuRa_III</b>')
		return 0

	for i in weather_file('r'):
		if 100000000 < int(i) < 999999999:
			bot.send_message(int(i), f'<b>Доброго утра и прекрасного настроения\n\n</b>'
			                         f'Погода в славном городе <b>Краснодаре</b> \nпо данным сервиса open-meteo.\n\n'
			                         f'<b>00:00   </b>{weather_today["weather_0"]} °C\n'
			                         f'<b>06:00   </b>{weather_today["weather_6"]} °C\n'
			                         f'<b>09:00   </b>{weather_today["weather_9"]} °C\n'
			                         f'<b>12:00   </b>{weather_today["weather_12"]} °C\n'
			                         f'<b>15:00   </b>{weather_today["weather_15"]} °C\n'
			                         f'<b>18:00   </b>{weather_today["weather_18"]} °C\n'
			                         f'<b>21:00   </b>{weather_today["weather_21"]} °C\n',
			                 parse_mode="html")


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
			time.sleep(45)


t = threading.Thread(target=check_with_time)
t.start()


def adm(iid):
	bot.send_message(759333833, f'Hey, new start user.\n Id= {iid}')


def day_str():
	# Определение дня недели(сегодня)(пн-вс), в str 0-6. и
	# присваивание значения переменной Мигалка(числитель/знаменатель)
	global Migalka
	dt_obj = datetime.datetime.now()
	dt_string = dt_obj.strftime("%w")
	Migalka = str(datetime.datetime.now().isocalendar().week % 2)

	if dt_string == '0':
		return '6'
	else:
		return str(int(dt_string) - 1)


def tomorrow_str():
	# Определение дня недели(завтра)(пн-вс), в str 0-6. и
	# присваивание значения переменной Мигалка(числитель/знаменатель)
	global Migalka
	dt_obj = datetime.datetime.now()
	dt_string = dt_obj.strftime("%w")
	Migalka = str(datetime.datetime.now().isocalendar().week % 2)

	if dt_string == '0':
		if Migalka == '0':
			Migalka = '1'
		else:
			Migalka = '0'
	return dt_string


with open("data/data_file.json", "r") as read_file:
	data = json.load(read_file)


@bot.message_handler(commands=['stop'])
def stop(message):
	if message.from_user.id == 759333833:
		bot.send_message(message.from_user.id, 'Жаль')
		print(data[-99999])
	else:
		bot.send_message(message.from_user.id, 'А тебе нельзя')


@bot.message_handler(commands=['start'])
# start и инициализация кнопок под сообщением
def start_message(message):
	adm(message.chat.username)
	#   bot.send_message(message.from_user.id, )
	keyboard = types.InlineKeyboardMarkup()
	#  наша клавиатура
	key_1_1 = types.InlineKeyboardButton(text='ИС 1-1', callback_data='1-1')
	keyboard.add(key_1_1)  # добавляем кнопку в клавиатуру
	key_1_2 = types.InlineKeyboardButton(text='ИС 1-2', callback_data='1-2')
	keyboard.add(key_1_2)
	key_2_1 = types.InlineKeyboardButton(text='ИС 2-1', callback_data='2-1')
	keyboard.add(key_2_1)
	key_2_2 = types.InlineKeyboardButton(text='ИС 2-2', callback_data='2-2')
	keyboard.add(key_2_2)
	key_19_03 = types.InlineKeyboardButton(text='ЮФ-1903', callback_data='1903')
	keyboard.add(key_19_03)
	bot.send_message(message.from_user.id, 'Привет, я буду твоим помощником в учёбе. Какое расписание тебе нужно?',
	                 reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)  # присвоение группы
def callback_worker(call):
	global group
	if call.data == "1-1":
		bot.send_message(call.message.chat.id, f'ок, ты в {call.data}')
		print(f"Группа ИС1.1, id={call.message.chat.username}")
		group = '0'
	elif call.data == "1-2":
		bot.send_message(call.message.chat.id, f'ок, ты в {call.data}')
		print(f"Группа ИС1.2, id={call.message.chat.username}")
		group = '1'
	elif call.data == "2-1":
		bot.send_message(call.message.chat.id, f'ок, ты в {call.data}')
		print(f"Группа ИС2.1, id={call.message.chat.username}")
		group = '2'
	elif call.data == "2-2":
		bot.send_message(call.message.chat.id, f'ок, ты в {call.data}')
		print(f"Группа ИС2.2, id={call.message.chat.username}")
		group = '3'
	elif call.data == "1903":
		bot.send_message(call.message.chat.id, f'ок, ты в ЮФ{call.data}')
		print(f"ЮФ1903, id={call.message.chat.username}")
		group = '4'


@bot.message_handler(commands=['today'])
def today(commands):
	day_str()

	if group == -1:
		bot.send_message(commands.from_user.id, 'Запусти команду /start')
	else:
		print("today")
		bot.send_message(commands.from_user.id, f'{data[group][Migalka][day_str()]}', parse_mode="html")


@bot.message_handler(commands=['week'])
def week(commands):
	day_str()
	if group == -1:
		bot.send_message(commands.from_user.id, 'Запусти команду /start')
	else:
		print("week")
		for i in range(7):
			bot.send_message(commands.from_user.id, f'{data[group][Migalka][str(i)]}', parse_mode="html")


@bot.message_handler(commands=['next_week'])
def next_week(commands):
	day_str()

	if Migalka == '1':
		next_week_count = '0'
	else:
		next_week_count = '1'

	if group == -1:
		bot.send_message(commands.from_user.id, 'Запусти команду /start')
	else:
		print("next_week")
		for i in range(7):
			bot.send_message(commands.from_user.id, f'{data[group][next_week_count][str(i)]}', parse_mode="html")


@bot.message_handler(commands=['tomorrow'])
def tomorrow(commands):
	tomorrow_str()
	if group == -1:
		bot.send_message(commands.from_user.id, 'Запусти команду /start')
	else:
		print("tomorrow")
		bot.send_message(commands.from_user.id, f'{data[group][str(Migalka)][tomorrow_str()]}', parse_mode="html")


@bot.message_handler(commands=['edit_weather'])
def edit_weather(commands):
	if weather_file('c', commands.from_user.id):
		msg = bot.send_message(commands.from_user.id, f'Уведомления включены. Хотите их отключить?\n(Да/нет)')
		bot.register_next_step_handler(msg, answer_weather)
	else:
		msg = bot.send_message(commands.from_user.id, f'Уведомления отключены. Хотите их включить?\n(Да/нет)')
		bot.register_next_step_handler(msg, answer_weather1)


def answer_weather(msg):
	if msg.text == 'ДА' or msg.text == 'Да' or msg.text == 'да' or msg.text == 'дА':
		weather_file('d', msg.chat.id)
		bot.send_message(msg.chat.id, 'Уведомления отключены.')


def answer_weather1(msg):
	if msg.text == 'ДА' or msg.text == 'Да' or msg.text == 'да' or msg.text == 'дА':
		weather_file('a', msg.chat.id)
		bot.send_message(msg.chat.id, 'Уведомления включены.')


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
	bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /start.")


bot.polling(none_stop=True, interval=1)
