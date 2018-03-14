# -*- coding: utf-8 -*-
'''
Телеграмм бот версии 0.1 для подготовки к ГИА по информатике
Бот написан учителем информатики Четверовым Алексеем Владимировичем
Бот основан на уроках по созданию музыкальной викторины https://www.gitbook.com/book/groosha/telegram-bot-lessons/details
Использована библиотека pyTelegramBotAPI https://github.com/eternnoir/pyTelegramBotAPI
В качестве источника данных для заданий используется база данных SQLLight
Информация о пользователях сохраняется в формете ключ-запись в отдельном файле
Этот файл функций работы с базами данных и форматирования ответов
'''
import shelve
from telebot import types
from SQLighter import SQLighter
from config import shelve_name, database_name
from random import shuffle

def count_rows():
    """
    Данный метод считает общее количество строк в базе данных и сохраняет в хранилище.
    Потом из этого количества будем выбирать музыку.
    """
    db = SQLighter(database_name)
    rowsnum1 = db.count_rows('1')
    rowsnum2 = db.count_rows('2')
    rowsnum3 = db.count_rows('3')
    rowsnum4 = db.count_rows('4')
    rowsnum5 = db.count_rows('5')
    rowsnum6 = db.count_rows('6')
    rowsnum7 = db.count_rows('7')
    rowsnum8 = db.count_rows('8')
    rowsnum9 = db.count_rows('9')
    rowsnum10 = db.count_rows('10')
    with shelve.open(shelve_name) as storage:
        storage['rows_count'] =[rowsnum1,rowsnum2,rowsnum3,rowsnum4,rowsnum5,rowsnum6,rowsnum7,rowsnum8,rowsnum9,rowsnum10]


def get_rows_count(table_number):
    """
    Получает из хранилища количество строк в БД
    :return: (int) Число строк
    """
    with shelve.open(shelve_name) as storage:
        rowsnum = storage['rows_count']
    return rowsnum [int(table_number)-1]


def set_user_game(chat_id, estimated_answer,memorial):
    """
    Записываем юзера в игроки и запоминаем, что он должен ответить, и текущий счет.
    :param chat_id: id юзера
    :param estimated_answer: правильный ответ (из БД)
    """
    with shelve.open(shelve_name) as storage:
    	try:
    		data_user=storage[str(chat_id)]
    		storage[str(chat_id)]=[estimated_answer,data_user[1],data_user[2],data_user[3],memorial]
    	except KeyError:
    		storage[str(chat_id)] = [estimated_answer,'0','0','',memorial]

def set_user_code_get(chat_id):
    """
    Записываем юзера в игроки и запоминаем, язык программирования
    """
    with shelve.open(shelve_name) as storage:
    	try:
    		data_user=storage[str(chat_id)]
    		return data_user[3]
    	except KeyError:
    		storage[str(chat_id)] = ['','0','0','','']
    		return None

def set_user_code(chat_id,code):
    """
    Записываем юзера в игроки и запоминаем, язык программирования
    """
    with shelve.open(shelve_name) as storage:
    	try:
    		data_user=storage[str(chat_id)]
    		storage[str(chat_id)]=['',data_user[1],data_user[2],code,'']
    	except KeyError:
    		storage[str(chat_id)] = ['','0','0',code,'']


def finish_user_game(chat_id,answer_1,answer_0):
    """
    Заканчиваем игру текущего пользователя и удаляем правильный ответ из хранилища
    :param chat_id: id юзера
    """
    with shelve.open(shelve_name) as storage:
        data_user=storage[str(chat_id)]
        data_user[1]=str(int(data_user[1])+answer_1)
        data_user[2]=str(int(data_user[2])+answer_0)
        storage[str(chat_id)]=['',data_user[1],data_user[2],data_user[3],'']

def finish_user_game_memorial(chat_id):
    """
    Заканчиваем игру текущего пользователя и удаляем правильный ответ из хранилища
    :param chat_id: id юзера
    """
    with shelve.open(shelve_name) as storage:
        data_user=storage[str(chat_id)]
        return data_user[4]

def finish_user_game_count(chat_id):
    """
    Заканчиваем игру текущего пользователя и удаляем правильный ответ из хранилища
    :param chat_id: id юзера
    """
    with shelve.open(shelve_name) as storage:
        data_user=storage[str(chat_id)]
        return 'Твой счет: ('+data_user[1]+') ответил верно; ('+data_user[2]+') ответил не верно.'

def get_answer_for_user(chat_id):
    """
    Получаем правильный ответ для текущего юзера.
    В случае, если человек просто ввёл какие-то символы, не начав игру, возвращаем None
    :param chat_id: id юзера
    :return: (str) Правильный ответ / None
    """
    with shelve.open(shelve_name) as storage:
        try:
            answer = storage[str(chat_id)]
            return answer[0]
        # Если человек не играет, ничего не возвращаем
        except KeyError:
            return None

def generate_markup(right_answer, wrong_answers,answer_number):
    """
    Создаем кастомную клавиатуру для выбора ответа
    :param right_answer: Правильный ответ
    :param wrong_answers: Набор неправильных ответов
    :return: Объект кастомной клавиатуры
    """
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    # Склеиваем правильный ответ с неправильными
    all_answers = '{},{}'.format(right_answer, wrong_answers)
    # Создаем лист (массив) и записываем в него все элементы
    list_items = []
    for item in all_answers.split(','):
        list_items.append(item)
    # Хорошенько перемешаем все элементы
    shuffle(list_items)
    # Заполняем разметку перемешанными элементами
    if answer_number=='4' or answer_number=='6':
        markup.row(list_items[0])
        markup.row(list_items[1])
        markup.row(list_items[2])
        markup.row(list_items[3])
    else:
        markup.row(list_items[0],list_items[1])
        markup.row(list_items[2],list_items[3])
    return markup

# функция вычисления правильного ответа для 9-го задания.
def generate_right_answer_9(right_answer,s,s1,r,k1):
    if right_answer=='add':
        return str(int(s+s1*(r+1)))
    if right_answer=='mult':
        return str(int(s*pow(s1,(r+1))))
    if right_answer=='aprog':
        for k in range(k1, k1+r+1):
            s = s+s1*k
        return str(int(s))
    if right_answer=='sub':
        return str(int(s-s1*(r+1)))

#функция вычисления правильного ответа для 9-го задания.
def generate_right_answer_10(right_answer,list1,k):
    if right_answer=='count':
        return str(list1.count(k))
    if right_answer=='min':
        return str(min(list1))
    if right_answer=='max':
        return str(max(list1))
    if right_answer=='minindex':
        return str(list1.index(min(list1)))
    if right_answer=='maxindex':
        return str(list1.index(max(list1)))
    if right_answer=='more':
        m=0
        for j in range(10):
            if list1[j]>k:
                m=m+1
        return str(int(m))
    if right_answer=='less':
        m=0
        for j in range(10):
            if list1[j]>k:
                m=m+1
        return str(int(m))
    if right_answer=='summ':
        m=0
        for j in range(10):
            if list1[j]>k:
                m=m+Dat[j]
        return str(int(m))
