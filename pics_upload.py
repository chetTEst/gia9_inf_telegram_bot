# -*- coding: utf-8 -*-
'''
Телеграмм бот версии 0.1 для подготовки к ГИА по информатике
Бот написан учителем информатики Четверовым Алексеем Владимировичем
Бот основан на уроках по созданию музыкальной викторины https://www.gitbook.com/book/groosha/telegram-bot-lessons/details
Использована библиотека pyTelegramBotAPI https://github.com/eternnoir/pyTelegramBotAPI
В качестве источника данных для заданий используется база данных SQLLight
Информация о пользователях сохраняется в формете ключ-запись в отдельном файле
Загрузка картинок и получение их ID для экономии трафика. Выполняется перед заполнением базы данных
'''
import telebot
import config
import os
import time

bot = telebot.TeleBot(config.token)

@bot.message_handler(commands=['test'])
def find_file_ids(message):
    for file in os.listdir('pics/z12/'):
        if file.split('.')[-1] == 'png':
            f = open('pics/z12/'+file, 'rb')
            msg = bot.send_photo(message.chat.id, f, None)
            #f.close()
            # А теперь отправим вслед за файлом его file_id
            bot.send_message(message.chat.id, msg.photo, reply_to_message_id=msg.message_id)
        time.sleep(3)


if __name__ == '__main__':
    bot.polling(none_stop=True)