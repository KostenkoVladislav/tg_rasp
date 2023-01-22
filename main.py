import telebot
from telebot import types
import datetime
import pprint
import json
from configuration import *

bot = telebot.TeleBot(mconf())
pprint.pprint('ok')
Migalka = 0  # 1- числитель
group = -1


def adm(iid):
    bot.send_message(759333833, f'Hey, new start user.\n Id= {iid}')
    # 0- знаменатель
    #   Порядковый номер дня недели-сегодня


def day():
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
    day()

    if group == -1:
        bot.send_message(commands.from_user.id, 'Запусти команду /start')
    else:
        print("today")
        bot.send_message(commands.from_user.id, f'{data[group][Migalka][day()]}\n\n{datetime.datetime.now()}')


@bot.message_handler(commands=['week'])
def today(commands):
    day()
    if group == -1:
        bot.send_message(commands.from_user.id, 'Запусти команду /start')
    else:
        print("week")
        for i in range(7):
            bot.send_message(commands.from_user.id, f'{data[group][Migalka][str(i)]}')


@bot.message_handler(commands=['next_week'])
def today(commands):
    day()

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
        bot.send_message(commands.from_user.id, f'{data[group][str(Migalka)][tomorrow_str()]}\n\n{datetime.datetime.now()}')


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /start.")


bot.polling(none_stop=True, interval=1)
