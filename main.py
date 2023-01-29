import telebot
from telebot import types
import datetime
import pprint
import json
from configuration import *
from read_write_weather import *
import threading

bot = telebot.TeleBot(mconf())
pprint.pprint('ok')
Migalka = 0  # 1- числитель
group = -1
time_tgid = {}  # словарь:айди в тг-время напоминания


def check_wth_time():   # функция проверки времени и отправки сообщений пользователю с актуальной погодой
	global time_tgid
	now = datetime.now()
	current_time = str(now.strftime("%H:%M"))
	for key, value in time_tgid.items():
		if current_time == value:
			bot.send_message(key,'А это погода')



def adm(iid):
	bot.send_message(759333833, f'Hey, new start user.\n Id= {iid}')
	# 0- знаменатель
	#   Порядковый номер дня недели-сегодня


def day_str():
	global Migalka
	dt_obj = datetime.datetime.now()
	dt_string = dt_obj.strftime("%w")
	Migalka = str(datetime.datetime.now().isocalendar().week % 2)

	if dt_string == '0':
		return '6'
	else:
		return str(int(dt_string) - 1)


def tomorrow_str():
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
		bot.send_message(commands.from_user.id, f'{data[group][Migalka][day_str()]}')


@bot.message_handler(commands=['week'])
def week(commands):
	day_str()
	if group == -1:
		bot.send_message(commands.from_user.id, 'Запусти команду /start')
	else:
		print("week")
		for i in range(7):
			bot.send_message(commands.from_user.id, f'{data[group][Migalka][str(i)]}')


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
			bot.send_message(commands.from_user.id, f'{data[group][next_week_count][str(i)]}')


@bot.message_handler(commands=['tomorrow'])
def tomorrow(commands):
	tomorrow_str()
	if group == -1:
		bot.send_message(commands.from_user.id, 'Запусти команду /start')
	else:
		print("tomorrow")
		bot.send_message(commands.from_user.id, f'{data[group][str(Migalka)][tomorrow_str()]}')


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
