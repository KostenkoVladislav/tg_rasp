from email.mime import message
from tracemalloc import start
import telebot
import os
import datetime
import pprint
from telebot import types
bot = telebot.TeleBot('5688159206:AAFxbhxdHY9WUiX3q424abv_pOLwK-bgTvY')
print('ok')

Migalka = 0  ## 1- числитель
             ## 0- знаменатель

def day():  ##Порядковый номер дня недели-сегодня
    global Migalka
    dt_obj =datetime.datetime.now()
    dt_string = dt_obj.strftime("%w")
    Migalka= datetime.datetime.now().isocalendar().week % 2
    return dt_string        

day()

text=[1,1,
      1,1,]
for i in range(4):
    text[i] = [f'{i}']*7   # type: ignore ## пустой массив 4х7
    
    
       
    
##pprint.pprint(text)

def rd(i):          ##Чтение расписания из файлов и заполненние массива
    for j in range(7):
        f = open(f'{j+1}.txt','r', encoding="utf-8")
        text[i][j]=f.read()  # type: ignore
        ##print(f'i={i} j={j} file={text[i][j]}')
        f.close()

os.chdir("C:\\Users\\SaMuRaI\\Desktop\\tg_rasp\\data\\11")
rd(0)
os.chdir("C:\\Users\\SaMuRaI\\Desktop\\tg_rasp\\data\\12")
rd(1)
os.chdir("C:\\Users\\SaMuRaI\\Desktop\\tg_rasp\\data\\21")
rd(2)
os.chdir("C:\\Users\\SaMuRaI\\Desktop\\tg_rasp\\data\\22")
rd(3)

##pprint.pprint(text)
group = -1


@bot.message_handler(commands=['start'])            ##start и инициализация кнопок под сообщением
def start_message(message):
    ##bot.send_message(message.from_user.id, )
    keyboard = types.InlineKeyboardMarkup(); #наша клавиатура
    key_1_1 = types.InlineKeyboardButton(text='1-1', callback_data='1-1') 
    keyboard.add(key_1_1); #добавляем кнопку в клавиатуру
    key_1_2 = types.InlineKeyboardButton(text='1-2', callback_data='1-2')
    keyboard.add(key_1_2)
    key_2_1 = types.InlineKeyboardButton(text='2-1', callback_data='2-1')
    keyboard.add(key_2_1); #добавляем кнопку в клавиатуру
    key_2_2 = types.InlineKeyboardButton(text='2-2', callback_data='2-2')
    keyboard.add(key_2_2)        
    bot.send_message(message.from_user.id,'Привет, я буду твоим помощником в учёбе. В какой ты группе ИСов?', reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: True)     ##присвоение группы 
def callback_worker(call):
    global group 
    if call.data == "1-1":
        bot.send_message(call.message.chat.id, f'ок, ты в {call.data}')
        print(f"Группа ИС1.1, id={call.message.chat.username}")
        group=0
    elif call.data == "1-2":
        bot.send_message(call.message.chat.id, f'ок, ты в {call.data}')
        print(f"Группа ИС1.2, id={call.message.chat.username}")
        group=1
    elif call.data == "2-1": 
        bot.send_message(call.message.chat.id, f'ок, ты в {call.data}')
        print(f"Группа ИС2.1, id={call.message.chat.username}")
        group=2
    elif call.data == "2-2": 
        bot.send_message(call.message.chat.id, f'ок, ты в {call.data}')
        print(f"Группа ИС2.2, id={call.message.chat.username}")
        group=3



@bot.message_handler(commands=['today'])
def today(commands):
    if group==-1:
        bot.send_message(commands.from_user.id, 'Запусти команду /start')
    else:
        print("today")
        raspisanie=text[group][int(day())-1]  # type: ignore
        bot.send_message(commands.from_user.id, f'nice\n{raspisanie}')

@bot.message_handler(commands=['tomorrow'])
def tomorrow(commands):
    if group==-1:
        bot.send_message(commands.from_user.id, 'Запусти команду /start')
    else:
        print("tomorrow")
        raspisanie=text[group][int(day())]  # type: ignore

        bot.send_message(commands.from_user.id, f'nice\n{raspisanie}')

@bot.message_handler(commands=['change'])
def change(message):
    ##bot.send_message(message.from_user.id, )
    keyboard = types.InlineKeyboardMarkup(); #наша клавиатура
    key_1_1 = types.InlineKeyboardButton(text='1-1', callback_data='1-1') 
    keyboard.add(key_1_1); #добавляем кнопку в клавиатуру
    key_1_2 = types.InlineKeyboardButton(text='1-2', callback_data='1-2')
    keyboard.add(key_1_2)
    key_2_1 = types.InlineKeyboardButton(text='2-1', callback_data='2-1')
    keyboard.add(key_2_1); #добавляем кнопку в клавиатуру
    key_2_2 = types.InlineKeyboardButton(text='2-2', callback_data='2-2')
    keyboard.add(key_2_2)        
    bot.send_message(message.from_user.id,'В какой ты группе ИСов?', reply_markup=keyboard)

    
   


   

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /start.")
##def today(message):
  ##  f = open('1.txt','w')
   ## bot.send_message(message.chat.id, f.read())





   

  
         
      
      

bot.polling(none_stop=True, interval=1)