# -*- coding: utf-8 -*-
'''
Телеграмм бот версии 0.1 для подготовки к ГИА по информатике
Бот написан учителем информатики Четверовым Алексеем Владимировичем
Бот основан на уроках по созданию музыкальной викторины https://www.gitbook.com/book/groosha/telegram-bot-lessons/details
Использована библиотека pyTelegramBotAPI https://github.com/eternnoir/pyTelegramBotAPI
В качестве источника данных для заданий используется база данных SQLLight
Информация о пользователях сохраняется в формете ключ-запись в отдельном файле
Это файл является классом для работы с базой данных SQLighter
'''
import sqlite3

class SQLighter:

    def __init__(self, database):
        self.connection = sqlite3.connect(database)
        self.cursor = self.connection.cursor()

    def select_all(self,table_numder):
        """ Получаем все строки """
        with self.connection:
            return self.cursor.execute('SELECT * FROM question'+table_numder).fetchall()

    def select_single(self, rownum,table_numder):
        """ Получаем одну строку с номером rownum """
        with self.connection:
            return self.cursor.execute('SELECT * FROM question'+table_numder+' WHERE id = ?', (rownum,)).fetchall()[0]

    def count_rows(self,table_numder):
        """ Считаем количество строк """
        with self.connection:
            result = self.cursor.execute('SELECT * FROM question'+table_numder).fetchall()
            return len(result)

    def close(self):
        """ Закрываем текущее соединение с БД """
        self.connection.close()