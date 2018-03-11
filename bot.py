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
    '''markup.row('/7', '/8', '/9', '/10', '/11', '/12')
    markup.row('/13', '/14', '/15', '/16', '/17', '/18')'''
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
    # Отправляем картинку с сообщением с вариантами ответа
    if answer_number[1]=='3' or answer_number[1]=='5':
        bot.send_message(message.chat.id,row[2])
        bot.send_photo(message.chat.id, row[1])
    if answer_number[1]=='4' or answer_number[1]=='6':
        bot.send_message(message.chat.id,row[2],parse_mode='HTML')
        bot.send_message(message.chat.id, row[1],parse_mode='HTML')
    bot.send_message(message.chat.id,row[3],reply_markup=markup)

    # Включаем "игровой режим"
    utils.set_user_game(message.chat.id, row[4],row[6])
    # Отсоединяемся от БД
    db_worker.close()

@bot.message_handler(commands=['7','8','9','10','11','12','13','14','15','16','17','18'])
def game_1_18(message):
	message_namber=message.text
	answer_number=message_namber.split('/')
	if answer_number[1]==7:
		pass
	else if answer_number[1]==8:
		pass
	else if answer_number[1]==9:
		code=utils.set_user_code_get
		if not code:
			markup = types.ReplyKeyboardMarkup()
			markup.row('/shoolAlgorithm')
			markup.row('/basic', '/pascal')
			bot.send_message(message.chat.id, "Выбери предпочитаемый язык программирования:\n * shoolAlgorithm - Алгоритмический язык (КУМИР)\n * basic - бейсик\n * pascal - Паскаль", reply_markup=markup)
		else:
			pass



@bot.message_handler(func=lambda message: True, content_types=['text'])
def check_answer(message):
    # Если функция возвращает None -> Человек не в игре
    answer = utils.get_answer_for_user(message.chat.id)
    # Как Вы помните, answer может быть либо текст, либо None
    # Если None:
    if not answer:
        bot.send_message(message.chat.id, 'Чтобы начать подготовку, набери команду /game')
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
        # Удаляем юзера из хранилища (игра закончена)
        utils.finish_user_game(message.chat.id,answer_game_1,answer_game_0)
        bot.send_message(message.chat.id, utils.finish_user_game_count(message.chat.id))

if __name__ == '__main__':
    utils.count_rows()
    random.seed()
    bot.polling(none_stop=True)