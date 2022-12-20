import telebot
import datetime
import pprint
from telebot import types

bot = telebot.TeleBot('5688159206:AAFxbhxdHY9WUiX3q424abv_pOLwK-bgTvY')
pprint.pprint('ok')

Migalka = 0  # 1- числитель
group = -1


# 0- знаменатель
#   Порядковый номер дня недели-сегодня
def day():
    global Migalka
    dt_obj = datetime.datetime.now()
    dt_string = dt_obj.strftime("%w")
    Migalka = datetime.datetime.now().isocalendar().week % 2
    return dt_string


day()

text0 = [1, 1,
        1, 1, ]
text1 = [1, 1,
        1, 1, ]
for i in range(4):
    text0[i] = [f'{i}'] * 7  # type: ignore #   пустой массив 4х7
    text1[i] = [f'{i}'] * 7  # type: ignore


#   pprint.pprint(text)
    # Чтение расписания из файлов и заполненние массива
for i in range(4):
    fls=[11, 12, 21, 22]
    for k in fls:
        for j in range(7):
            f = open(f'data/{k}/{j+1}.txt', 'r', encoding="utf-8")
            text0[i][j] = f.read()  # type: ignore
            print(f'i={i} j={j} file={text0[i][j]}')
            f.close()

            f = open(f'data/{k}/{j + 1}1.txt', 'r', encoding="utf-8")
            text1[i][j] = f.read()  # type: ignore
            print(f'i={i} j={j} file={text1[i][j]}')
            f.close()

#   pprint.pprint(text)



@bot.message_handler(commands=['start'])  # start и инициализация кнопок под сообщением
def start_message(message):
    #   bot.send_message(message.from_user.id, )
    keyboard = types.InlineKeyboardMarkup()  #  наша клавиатура
    key_1_1 = types.InlineKeyboardButton(text='1-1', callback_data='1-1')
    keyboard.add(key_1_1)   #   добавляем кнопку в клавиатуру
    key_1_2 = types.InlineKeyboardButton(text='1-2', callback_data='1-2')
    keyboard.add(key_1_2)
    key_2_1 = types.InlineKeyboardButton(text='2-1', callback_data='2-1')
    keyboard.add(key_2_1)   #   добавляем кнопку в клавиатуру
    key_2_2 = types.InlineKeyboardButton(text='2-2', callback_data='2-2')
    keyboard.add(key_2_2)
    bot.send_message(message.from_user.id, 'Привет, я буду твоим помощником в учёбе. В какой ты группе ИСов?',
                     reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)  #  присвоение группы
def callback_worker(call):
    global group
    if call.data == "1-1":
        bot.send_message(call.message.chat.id, f'ок, ты в {call.data}')
        print(f"Группа ИС1.1, id={call.message.chat.username}")
        group = 0
    elif call.data == "1-2":
        bot.send_message(call.message.chat.id, f'ок, ты в {call.data}')
        print(f"Группа ИС1.2, id={call.message.chat.username}")
        group = 1
    elif call.data == "2-1":
        bot.send_message(call.message.chat.id, f'ок, ты в {call.data}')
        print(f"Группа ИС2.1, id={call.message.chat.username}")
        group = 2
    elif call.data == "2-2":
        bot.send_message(call.message.chat.id, f'ок, ты в {call.data}')
        print(f"Группа ИС2.2, id={call.message.chat.username}")
        group = 3


@bot.message_handler(commands=['today'])
def today(commands):
    if group == -1:
        bot.send_message(commands.from_user.id, 'Запусти команду /start')
    else:
        print("today")
        if Migalka == 0:
            bot.send_message(commands.from_user.id, f'nice\n{text0[group][int(day()) - 1]}')
            print(f'Group={group}')
        else:
            bot.send_message(commands.from_user.id, f'nice\n{text1[group][int(day()) - 1]}')
            print(f'Group={group}')


@bot.message_handler(commands=['tomorrow'])
def tomorrow(commands):
    if group == -1:
        bot.send_message(commands.from_user.id, 'Запусти команду /start')
    else:
        print("tomorrow")
        if Migalka == 0:
            bot.send_message(commands.from_user.id, f'nice\n{text0[group][int(day())]}')
            print(f'Group={group}')
        else:
            bot.send_message(commands.from_user.id, f'nice\n{text1[group][int(day())]}')
            print(f'Group={group}')

@bot.message_handler(commands=['change'])
def change(message):
    #bot.send_message(message.from_user.id, )
    keyboard = types.InlineKeyboardMarkup()  # наша клавиатура
    key_1_1 = types.InlineKeyboardButton(text='1-1', callback_data='1-1')
    keyboard.add(key_1_1)  # добавляем кнопку в клавиатуру
    key_1_2 = types.InlineKeyboardButton(text='1-2', callback_data='1-2')
    keyboard.add(key_1_2)
    key_2_1 = types.InlineKeyboardButton(text='2-1', callback_data='2-1')
    keyboard.add(key_2_1)  # добавляем кнопку в клавиатуру
    key_2_2 = types.InlineKeyboardButton(text='2-2', callback_data='2-2')
    keyboard.add(key_2_2)
    bot.send_message(message.from_user.id, 'В какой ты группе ИСов?', reply_markup=keyboard)


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /start.")


#def today(message):
#  f = open('1.txt','w')
# bot.send_message(message.chat.id, f.read())


bot.polling(none_stop=True, interval=1)