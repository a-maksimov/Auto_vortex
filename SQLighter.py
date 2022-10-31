# -*- coding: utf-8 -*-
"""
Created on Oct 22, 2017

@author: Administrator
"""
import sqlite3


class SQLighter:
    def __init__(self, database):
        self.connection = sqlite3.connect(database)
        self.cursor = self.connection.cursor()

    def select_all(self, table):
        """ Получаем все строки """
        with self.connection:
            return self.cursor.execute('SELECT * FROM {}'.format(table)).fetchall()

    def add_client(self, client):
        """ Add a new booking into the table """
        with self.connection:
            return self.cursor.execute(f'INSERT OR IGNORE INTO clients (user_id, first_name, last_name, phone) VALUES '
                                       f'(?, ?, ?, ?)', client)

    def add_booking(self, user_id, table, booking_date):
        """ Add a new booking into the table """
        with self.connection:
            self.cursor.execute(f'INSERT INTO {table} (first_name, last_name, phone, year, month, day)'
                                f'VALUES ((SELECT first_name FROM clients WHERE user_id = {user_id}),'
                                f'(SELECT last_name FROM clients WHERE user_id = {user_id}), '
                                f'(SELECT phone FROM clients WHERE user_id = {user_id}),'
                                f' ?, ?, ?)', booking_date)

    def close(self):
        """ Закрываем текущее соединение с БД """
        self.connection.close()