# -*- coding: utf-8 -*-
import config
import telebot
from telebot import types
from SQLighter import SQLighter
import utils
import random

bot = telebot.TeleBot(config.token)

@bot.message_handler(commands=['test'])
def game(message):
    message_namber=message.text
    answer_number=message_namber.split('/')
    keyboard_hider = types.ReplyKeyboardRemove()
    db_worker = SQLighter(config.database_name,'6')
    # Получаем случайную строку из БД
    row = db_worker.select_single(1,'6')
    # Формируем разметку
    markup = utils.generate_markup(row[4], row[5],'6')
    # Отправляем картинку с сообщением с вариантами ответа
    bot.send_message(message.chat.id,row[2],parse_mode='HTML')
    bot.send_message(message.chat.id, row[1],parse_mode='HTML',reply_markup=markup)
    db_worker.close()
    
if __name__ == '__main__':
    bot.polling(none_stop=True)