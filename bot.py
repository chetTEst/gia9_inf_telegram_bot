# -*- coding: utf-8 -*-
'''
Телеграмм бот версии 0.1 для подготовки к ГИА по информатике
Бот написан учителем информатики Четверовым Алексеем Владимировичем
Бот основан на уроках по созданию музыкальной викторины https://www.gitbook.com/book/groosha/telegram-bot-lessons/details
Использована библиотека pyTelegramBotAPI https://github.com/eternnoir/pyTelegramBotAPI
В качестве источника данных для заданий используется база данных SQLLight
Информация о пользователях сохраняется в формете ключ-запись в отдельном файле
Этот файл основной программы бота
'''
import config #
import telebot
from telebot import types
from SQLighter import SQLighter
import utils
import random

bot = telebot.TeleBot(config.token)


@bot.message_handler(commands=['game'])
def new_game(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=True)
    markup.row('/1', '/2', '/3', '/4', '/5', '/6')
    markup.row('/7', '/8', '/9', '/10', '/11', '/12')
    '''markup.row('/13', '/14', '/15', '/16', '/17', '/18')'''
    bot.send_message(message.chat.id, "Выбери номер задания для тренировки:", reply_markup=markup)


@bot.message_handler(commands=['1','2','3','4','5','6'])
def game_1_6(message):
    # Подключаемся к БД
    message_namber=message.text
    answer_number=message_namber.split('/')
    #keyboard_hider = types.ReplyKeyboardRemove()
    db_worker = SQLighter(config.database_name)
    # Получаем случайную строку из БД
    row = db_worker.select_single(random.randint(1, utils.get_rows_count(answer_number[1])),answer_number[1])
    # Формируем разметку
    markup = utils.generate_markup(row[4], row[5],answer_number[1])
    if answer_number[1]=='3' or answer_number[1]=='5':
        # Отправляем вводную часть вопроса
        bot.send_message(message.chat.id,row[2])
        # Отправляем картинку
        bot.send_photo(message.chat.id, row[1])
    if answer_number[1]=='4' or answer_number[1]=='6':
        # Отправляем вводную часть вопроса с форматированием
        bot.send_message(message.chat.id,row[2],parse_mode='HTML')
        # Отправляем основную часть вопроса с форматированием
        bot.send_message(message.chat.id, row[1],parse_mode='HTML')
    # Отправляем вопрос и заменяем кдавиатуру на варианты ответа
    bot.send_message(message.chat.id,row[3],reply_markup=markup)

    # Включаем "игровой режим"... ждем ответа от пользователя
    utils.set_user_game(message.chat.id, row[4],row[6])
    # Отсоединяемся от БД
    db_worker.close()

@bot.message_handler(commands=['7','8','11','12']) #,'13','14','15','16','17','18'])
def game_7_18_not_9_10(message):
    #получаем сообщение пользователя
    message_namber=message.text
    #разбиваем сообщение на части, делитель - символ /
    answer_number=message_namber.split('/')
    # Подключаемся к БД
    db_worker = SQLighter(config.database_name)
    # Получаем случайную строку из БД по номеру таблицы взятую из сообщения answer_number
    row = db_worker.select_single(random.randint(1, utils.get_rows_count(answer_number[1])),answer_number[1])
    if answer_number[1]=='7' or answer_number[1]=='11' or answer_number[1]=='12':
        # Отправляем вводную часть вопроса
        bot.send_message(message.chat.id,row[2])
        # Отправляем картинку
        bot.send_photo(message.chat.id, row[1])
    elif answer_number[1]=='8':
        # Отправляем вводную часть вопроса с форматированием
        bot.send_message(message.chat.id,row[2],parse_mode='HTML')
        # Отправляем основную часть вопроса
        bot.send_message(message.chat.id, row[1])
    # Отправляем вопрос
    bot.send_message(message.chat.id,row[3])
    # Включаем "игровой режим"... ждем ответа от пользователя
    utils.set_user_game(message.chat.id, row[4],row[5])
    # Отсоединяемся от БД
    db_worker.close()

@bot.message_handler(commands=['9']) #добавить 10
def game_9(message):
    code=utils.set_user_code_get(message.chat.id)
    if not code or code=='':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=True)
        markup.row('/sсhoolalgorithm')
        markup.row('/basic', '/pascal')
        markup.row('/python')
        bot.send_message(message.chat.id, 'ВНИМАНИЕ! Не выбран предпочитаемый язык программирования!\nВыбери предпочитаемый язык программирования:\n * shoolAlgorithm - Алгоритмический язык (КУМИР)\n * basic - бейсик\n * pascal - Паскаль\n * Pyhon - Пайтон (Питон)', reply_markup=markup)
    else:
        #получаем сообщение пользователя
        message_namber=message.text
        #разбиваем сообщение на части, делитель - символ /
        answer_number=message_namber.split('/')
        # Подключаемся к БД
        db_worker = SQLighter(config.database_name)
        # Получаем случайную строку из БД по номеру таблицы взятую из сообщения answer_number
        row = db_worker.select_single(random.randint(1, utils.get_rows_count(answer_number[1])),answer_number[1])
        #Отсоединяемся от БД
        db_worker.close()
        #Генерируем значение пременной для дополнительного сообщения:
        chat_message ={
        '2':'Алгоритмический язык',
        '3':'BASIC',
        '4':'Pascal',
        '5':'Pyhon'
        }
        #генерируем случайные числа для шаблона программы из базы данных
        s=random.randint(1,10)-1
        s1=random.randint(1,8)
        r=random.randint(4,9)
        k1=random.randint(4,9)
        #сохраняем в переменную текст шаюблона из базы данных
        result_code=row[int(code)]
        #заменяем данные в шаблоне
        result_code=result_code.replace('{s}',str(s))
        result_code=result_code.replace('{k1}',str(k1))
        result_code=result_code.replace('{k2}',str(k1+r))
        result_code=result_code.replace('{s1}',str(s1))
        # Отправляем вводную часть вопроса
        bot.send_message(message.chat.id,row[1])
        # Отправляем основную часть вопроса c форматированием
        bot.send_message(message.chat.id, '<pre>'+result_code+'</pre>',parse_mode='HTML')
        # Отправляем дополнительное сообщение
        bot.send_message(message.chat.id,'Текст программы приведён на языке программирования: '+chat_message[code])
        #сохраняем в переменную текст шаюблона пояснения из базы данных
        result_memorial=row[7]
        #заеняем данные в шаблоне
        result_memorial=result_memorial.replace('{s}',str(s))
        result_memorial=result_memorial.replace('{k1}',str(k1))
        result_memorial=result_memorial.replace('{k2}',str(k1+r))
        result_memorial=result_memorial.replace('{s1}',str(s1))
        result_memorial=result_memorial.replace('{r}',str(r+1))
        result_memorial=result_memorial.replace('{answer}',utils.generate_right_answer_9(row[6],s,s1,r,k1))
        # Включаем "игровой режим"... ждем ответа от пользователя
        utils.set_user_game(message.chat.id, utils.generate_right_answer_9(row[6],s,s1,r,k1),result_memorial)

@bot.message_handler(commands=['10'])
def game_10(message):
    code=utils.set_user_code_get(message.chat.id)
    if not code or code=='':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=True)
        markup.row('/sсhoolalgorithm')
        markup.row('/basic', '/pascal')
        markup.row('/python')
        bot.send_message(message.chat.id, 'ВНИМАНИЕ! Не выбран предпочитаемый язык программирования!\nВыбери предпочитаемый язык программирования:\n * shoolAlgorithm - Алгоритмический язык (КУМИР)\n * basic - бейсик\n * pascal - Паскаль\n * Pyhon - Пайтон (Питон)', reply_markup=markup)
    else:
        #получаем сообщение пользователя
        message_namber=message.text
        #разбиваем сообщение на части, делитель - символ /
        answer_number=message_namber.split('/')
        # Подключаемся к БД
        db_worker = SQLighter(config.database_name)
        # Получаем случайную строку из БД по номеру таблицы взятую из сообщения answer_number
        row = db_worker.select_single(random.randint(1, utils.get_rows_count(answer_number[1])),answer_number[1])
        #Отсоединяемся от БД
        db_worker.close()
        #Генерируем значение пременной для дополнительного сообщения:
        chat_message ={
        '2':'Алгоритмический язык',
        '3':'BASIC',
        '4':'Pascal',
        '5':'Pyhon'
        }
        #генерируем случайные числа для шаблона программы из базы данных
        Dat=[random.randint(10, 20) for i in range(10)]
        #Генерируем вспомогательное число для сравнения или подсчета
        t=random.randint(10, 20)
        #сохраняем в переменную текст шаюблона из базы данных
        result_code=row[int(code)]
        #заменяем данные в шаблоне
        for i in range(10):
            result_code=result_code.replace('{dat'+str(int(i))+'}',str(Dat[i]))
        result_code=result_code.replace('{t}',str(t))
        # Отправляем вводную часть вопроса
        bot.send_message(message.chat.id,row[1])
        # Отправляем основную часть вопроса c форматированием
        bot.send_message(message.chat.id, '<pre>'+result_code+'</pre>',parse_mode='HTML')
        # Отправляем дополнительное сообщение
        bot.send_message(message.chat.id,'Текст программы приведён на языке программирования: '+chat_message[code])
        #сохраняем в переменную текст шаюблона пояснения из базы данных
        result_memorial=row[7]
        #заеняем данные в шаблоне
        result_memorial=result_memorial.replace('{t}',str(t))
        result_memorial=result_memorial.replace('{answer}',utils.generate_right_answer_10(row[6],Dat,t))
        # Включаем "игровой режим"... ждем ответа от пользователя
        utils.set_user_game(message.chat.id, utils.generate_right_answer_10(row[6],Dat,t),result_memorial)


@bot.message_handler(commands=['schoolalgorithm','basic','pascal','python'])
def game_1_18_9(message):
    #убрать клавиатуру 
    keyboard_hider = types.ReplyKeyboardRemove()
    #получаем сообщение пользователя
    message_namber=message.text
    #разбиваем сообщение на части, делитель - символ /
    answer_number=message_namber.split('/')
    if answer_number[1]=='schoolalgorithm':
        code='2'
        chat_message='Алгоритмический язык'
    elif answer_number[1]=='basic':
        code='3'
        chat_message='BASIC'
    elif answer_number[1]=='pascal':
        code='4'
        chat_message='Pascal'
    elif answer_number[1]=='python':
        code='5'
        chat_message='Pyhon'
    utils.set_user_code(message.chat.id,code)
    bot.send_message(message.chat.id,'Вы установили в качестве основного языка: '+chat_message+'\nНаберите команду /9 или /10 для получения задания.',reply_markup=keyboard_hider)

@bot.message_handler(func=lambda message: True, content_types=['text'])
def check_answer(message):
    #убрать клавиатуру 
    keyboard_hider = types.ReplyKeyboardRemove()
    # Если функция возвращает None -> Человек не в игре
    answer = utils.get_answer_for_user(message.chat.id)
    # Как Вы помните, answer может быть либо текст, либо None
    # Если None:
    if not answer:
        bot.send_message(message.chat.id, 'Чтобы начать подготовку, набери команду /game')
    elif answer=='':
        bot.send_message(message.chat.id, 'Чтобы продолжить подготовку, набери команду /game')
    else:
        # Уберем клавиатуру с вариантами ответа.
        #keyboard_hider = types.ReplyKeyboardRemove() reply_markup=keyboard_hider
        # Если ответ правильный/неправильный
        if message.text == answer:
            bot.send_message(message.chat.id, 'Верно!')
            answer_game_1=1
            answer_game_0=0
        else:
            bot.send_message(message.chat.id, 'Увы, Вы ошиблись!')
            bot.send_message(message.chat.id, 'Пояснения:\n'+utils.finish_user_game_memorial(message.chat.id))
            answer_game_1=0
            answer_game_0=1
        # Сохраняем счет пользователя в базу данных (игра закончена)
        utils.finish_user_game(message.chat.id,answer_game_1,answer_game_0)
        bot.send_message(message.chat.id, utils.finish_user_game_count(message.chat.id),reply_markup=keyboard_hider)

if __name__ == '__main__':
    utils.count_rows()
    random.seed()
    bot.polling(none_stop=True)