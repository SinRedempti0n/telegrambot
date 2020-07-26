import telebot; # API Бота
from telebot import types # Импорт инлайнов
import random;
import config; # Файл конфига
import time;

import sqlite3
DataBase = sqlite3.connect("Users.db") # Подключение БД
cursor = DataBase.cursor() # Создание указателя
cursor.execute("""CREATE TABLE IF NOT EXISTS Users (
	UserID INT PRIMARY KEY,
	Timer INT,
	Username TEXT);
""") # Создание таблицы если её нет
DataBase.commit()   # Сохранение изменений
cursor.execute("""CREATE TABLE IF NOT EXISTS SAP (
    CRMLogin TEXT PRIMARY KEY,
    UserID INT
    Username TEXT);
""") # Создание таблицы если её нет
DataBase.commit()   # Сохранение изменений
DataBase.close()    # Закрытие таблицы

bot = telebot.TeleBot(config.token);

def UserCheck(message):
    DataBase = sqlite3.connect("Users.db")  # Подключение БД
    cursor = DataBase.cursor()  # Создание указателя
    cursor.execute('SELECT UserId, Timer FROM Users WHERE UserID LIKE ' + str(message.chat.id)) # Поиск по ID если ли запись в таблице
    data = cursor.fetchall()    # Выгрузка найденных данных в список
    if not data: # Если данные пусты
        answerFile = open('Forms\\Answers\\' + str(random.randint(0, 4)) + '.txt')
        bot.send_message(message.chat.id, '{username}, '.format( username = message.chat.username) + answerFile.read(), parse_mode="HTML")  # Написать падажжи
        tmp = (message.chat.id, time.time(), message.chat.username) # Создать список (ID, Время обращения, UserName(Задел на будущее))
        query = "INSERT into Users values (?, ?, ?)"    # Строковый запрос
        cursor.execute(query, tmp)  # Создание записи в таблице с указанием написавшего и временем написания
    elif time.time() - data[0][1] > config.answer_delay:    # Если данные не пусты, сверить прошедшее время с временем из конфига
        answerFile = open('Forms\\Answers\\' + str(random.randint(0, 4)) + '.txt')
        bot.send_message(message.chat.id, '{username}, '.format( username = message.chat.username) + answerFile.read(), parse_mode="HTML")  # Написать падажжи
        cursor.execute('UPDATE Users SET Timer = ' + str(time.time()) + ' WHERE UserID = '+ str(message.chat.id))   # Обновить время
    DataBase.commit()   # Сохранение изменений
    DataBase.close()    # Закрытие таблицы



@bot.message_handler(commands=['start', 'help'])    # Обработка команд /help и /start
def send_welcome(message):
    try:
        helpInline = types.ForceReply(selective=False) # Обязательный reply
        helpInline = types.ReplyKeyboardRemove(selective=True)
        itembtn1 = types.KeyboardButton('/link')    # Элементы
        itembtn2 = types.KeyboardButton('/news')
        itembtn3 = types.KeyboardButton('/boss')
        helpInline.row(itembtn1, itembtn2, itembtn3)
        cid = message.chat.id
        bot.delete_message(message.chat.id, message.message_id) # Удаление сообщения с командой
        helpFile = open('Forms\\Help.txt', 'r') # Открытие файла
        bot.send_message(cid, helpFile.read(), parse_mode="HTML", disable_web_page_preview=True, reply_markup=helpInline) # Пересылка содержимого файла сообщением
        helpFile.close() #Закрытие файла
    except:
        cid = message.chat.id
        bot.delete_message(message.chat.id, message.message_id) # Удаление сообщения с командой
        helpFile = open('Forms\\Help.txt', 'r') # Открытие файла
        bot.send_message(cid, helpFile.read(), parse_mode="HTML", disable_web_page_preview=True) # Пересылка содержимого файла сообщением
        helpFile.close() #Закрытие файла

@bot.message_handler(commands=['link']) # Обработка команды /link
def send_link(message):
    try:
        cid = message.chat.id   # Сохранение id чата
        bot.delete_message(message.chat.id, message.message_id) # Удаление сообщения с командой
        linkFile = open('Forms\\Link.txt', 'r') # Открытие файла
        bot.send_message(cid, linkFile.read(), parse_mode="HTML", disable_web_page_preview=True) # Пересылка содержимого файла сообщением
        linkFile.close() #Закрытие файла
    except:
        pass    # Пропустить

@bot.message_handler(commands=['news']) # Обработка команды /news
def send_news(message):
    try:
        cid = message.chat.id   # Сохранение id чата
        bot.delete_message(message.chat.id, message.message_id) # Удаление сообщения с командой
        newsFile = open('Forms\\News.txt', 'r') # Открытие файла
        bot.send_message(cid, newsFile.read(), parse_mode="HTML", disable_web_page_preview=True)    # Пересылка содержимого файла сообщением
        newsFile.close()    # Закрытие файла
    except:
        pass    # Пропустить

@bot.message_handler(commands=['boss']) # Обработка команды /boss
def send_boss(message):
    try:
        cid = message.chat.id   # Сохранение id чата
        bot.delete_message(message.chat.id, message.message_id) # Удаление сообщения с командой
        bossFile = open('Forms\\Boss.txt', 'r') # Открытие файла
        bot.send_message(cid, bossFile.read(), parse_mode="HTML", disable_web_page_preview=True)
        bossFile.close() # Закрытие файла
    except:
        pass    # Пропустить

@bot.message_handler(commands=['returnID']) # Обработка команды /returnID
def send_message_id(message):
    bot.reply_to(message, message.chat.id)


@bot.message_handler(commands=['register']) # Обработка команды /register
def login_reg(message):
    params = message.text.upper().split(' ')
    if(len(params) == 2):
        DataBase = sqlite3.connect("Users.db")  # Подключение БД
        cursor = DataBase.cursor()  # Создание указателя
        cursor.execute('SELECT CRMLogin, UserID FROM SAP WHERE UserID = ' + str(message.chat.id) ) # Поиск по ID если ли запись в таблице
        data = cursor.fetchall()    # Выгрузка найденных данных в список
        if not data: # Если данные пусты
            bot.send_message(message.chat.id, '{username}, зарегистрирован как {crm}'.format( username = message.chat.username, crm = params[1]))
            tmp = (params[1], message.chat.id, message.chat.username) # Создать список (CRM, Chat ID)
            query = "INSERT INTO SAP VALUES (?, ?, ?)"    # Строковый запрос
            cursor.execute(query, tmp)  # Создание записи в таблице с указанием написавшего и временем написания
        elif time.time() - data[0][1] > config.answer_delay:    # Если данные не пусты, сверить прошедшее время с временем из конфига
            bot.send_message(message.chat.id, '{username}, обновлён как {crm}'.format( username = message.chat.username, crm = params[1]))
            cursor.execute('UPDATE SAP SET CRMLogin = "' + str(params[1]) + '" WHERE UserID = '+ str(message.chat.id))   # Обновить время
        DataBase.commit()   # Сохранение изменений
        DataBase.close()    # Закрытие таблицы
    else:
        bot.send_message(message.chat.id, 'Неверное количество параметров')

@bot.message_handler(commands=['unlock']) # Обработка команды /register
def send_unlock(message):
    params = message.text.upper().split(' ')
    if(len(params) == 2):
        DataBase = sqlite3.connect("Users.db")  # Подключение БД
        cursor = DataBase.cursor()  # Создание указателя
        cursor.execute('SELECT CRMLogin, UserID, Username FROM SAP WHERE CRMLogin ="' + str(params[1]) + '"') # Поиск по ID если ли запись в таблице
        data = cursor.fetchall()    # Выгрузка найденных данных в список
        if not data: # Если данные пусты
            bot.send_message(message.chat.id, 'К сожалению сотрудник {crm} не найден'.format(crm = params[1]))
        else:    # Если данные не пусты, сверить прошедшее время с временем из конфига
            try:
                bot.send_message(data[0][1], "@{username}, вас попросили выйти из карточки. Спасибо.".format(username = data[0][2]))
                bot.send_message(message.chat.id, "Сообщение специалисту отправлено.")
            except:
                bot.send_message(message.chat.id, "Упс, что-то пошло не так обратитесь к супервайзеру.")
    else:
        bot.send_message(message.chat.id, 'Неверное количество параметров')

@bot.message_handler(content_type=['new_chat_members']) # Обработка нового участника
def handle_new_chat_members(message):
    try:
        bossFile = open('Forms\\Hello.txt', 'r') # Открытие файла
        bot.send_message(message.chat.id, bossFile.read(), parse_mode="HTML", disable_web_page_preview=True)
        bossFile.close() # Закрытие файла
    except:
        bot.send_message(message.chat.id, "Упс, что-то пошло не так обратитесь к супервайзеру.")



@bot.message_handler(func=lambda message: True) # Обработка текста
def handle_text(message):
    if int(message.chat.id) == int(config.owner):   # Если id отправителя совпадает с id владельца из config
        try:
            bot.send_message(message.reply_to_message.forward_from.id, message.text) # Отправить текст ответа как сообщение владельцу пересланного
        except:
            pass
    else:
        UserCheck(message)
        # bot.forward_message(424238892, message.chat.id, message.message_id)  # Переслать сообщение @SinRedemption, для диагностики
        bot.forward_message(config.owner, message.chat.id, message.message_id)  # Переслать сообщение владельцу

@bot.message_handler(content_types=['sticker'])# Обработка медиа
def handle_sticker(message):
    if int(message.chat.id) == int(config.owner):   # Если id отправителя совпадает с id владельца из config
        try:
            bot.forward_message(message.reply_to_message.forward_from.id, message.chat.id, message.message_id)# Переслать сообщение владельцу
        except:
            bot.send_message(message.chat.id, "Упс, что-то пошло не так обратитесь к супервайзеру.")
    else:
        UserCheck(message)
        bot.forward_message(config.owner, message.chat.id, message.message_id)# Переслать сообщение владельцу

@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    if int(message.chat.id) == int(config.owner):   # Если id отправителя совпадает с id владельца из config
        try:
            bot.send_photo(message.reply_to_message.forward_from.id, message.photo[0].file_id)# Переслать сообщение владельцу
        except:
            bot.send_message(message.chat.id, "Упс, что-то пошло не так обратитесь к супервайзеру.")
    else:
        UserCheck(message)
        bot.forward_message(config.owner, message.chat.id, message.message_id)# Переслать сообщение владельцу

@bot.message_handler(content_types=['document'])
def handle_document(message):
    if int(message.chat.id) == int(config.owner):   # Если id отправителя совпадает с id владельца из config
        try:
            bot.send_document(message.reply_to_message.forward_from.id, message.document.file_id)# Переслать сообщение владельцу
        except:
            bot.send_message(message.chat.id, "Упс, что-то пошло не так обратитесь к супервайзеру.")
    else:
        UserCheck(message)
        bot.forward_message(config.owner, message.chat.id, message.message_id)# Переслать сообщение владельцу

@bot.message_handler(content_types=['video'])
def handle_video(message):
    if int(message.chat.id) == int(config.owner):   # Если id отправителя совпадает с id владельца из config
        try:
            bot.send_video(message.reply_to_message.forward_from.id, message.video.file_id)# Переслать сообщение владельцу
        except:
            bot.send_message(message.chat.id, "Упс, что-то пошло не так обратитесь к супервайзеру.")
    else:
        UserCheck(message)
        bot.forward_message(config.owner, message.chat.id, message.message_id)# Переслать сообщение владельцу

bot.polling()
# by SinRedemption
