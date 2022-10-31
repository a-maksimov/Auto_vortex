# -*- coding: utf-8 -*-
"""
Created on Oct 20, 2022

@author:
"""
from datetime import time

import telebot
from telegram_bot_calendar import WYearTelegramCalendar
import config
# import csv
# import time
# import datetime
# import logging

# bot plugins
import start
import mini_project_hangman
import vortex_plugin

commands = {  # command description used in the "help" command
    'start': 'Познакомьтесь с ботом',
    'help': 'Список доступных команд',
    'vortex': 'Салон красоты',
    'hangman': 'Игра в Виселицу'
}


# включение отображения лога в консоли
# logger = telebot.logger
# telebot.logger.setLevel(logging.DEBUG)  # Outputs debug messages to console


# telebot.apihelper.proxy = {
#   'https':'socks5://{}:{}'.format(config.ip,config.port)
# }

def listener(messages):
    """
    When new messages arrive TeleBot will call this function.
    """
    for message in messages:
        if message.content_type == 'text':
            # print the sent message to the console
            if message.chat.type == 'private':
                if message.chat.username:
                    print(message.chat.username + " [" + str(message.chat.id) + "]: " + message.text)
                else:
                    print(message.chat.first_name + " [" + str(message.chat.id) + "]: " + message.text)
            else:
                print(message.chat.title + " [" + str(message.chat.id) + "]: " + message.text)


bot = telebot.TeleBot(config.token)
bot.remove_webhook()
bot.set_update_listener(listener)  # register listener


# handle the "/start" command
@bot.message_handler(commands=['start'])
def handle_start_help(message):
    start.handle_start_help(bot, message)


# help page
@bot.message_handler(commands=['help'])
def command_help(message):
    help_text = "Доступны следующие команды: \n"
    for key in commands:  # generate help text out of the commands dictionary defined at the top
        help_text += "/" + key + ": "
        help_text += commands[key] + "\n"
    bot.send_message(message.chat.id, help_text)  # send the generated help page


@bot.message_handler(commands=['hangman'])
def hangman(message):
    mini_project_hangman.play_hangman(bot, message)


@bot.message_handler(commands=['vortex'])
def vortex(message):
    vortex_plugin.start_vortex(bot, message)


# календарь для записи на маникюр
@bot.callback_query_handler(WYearTelegramCalendar.func(calendar_id=1))
def handle_calendar(call):
    vortex_plugin.callback_calendar(bot, call)


# календарь для записи на мейкап
@bot.callback_query_handler(WYearTelegramCalendar.func(calendar_id=2))
def handle_calendar(call):
    vortex_plugin.callback_calendar(bot, call)


# календарь для записи на стайлинг
@bot.callback_query_handler(WYearTelegramCalendar.func(calendar_id=3))
def handle_calendar(call):
    vortex_plugin.callback_calendar(bot, call)


# календарь для записи на массаж лица
@bot.callback_query_handler(WYearTelegramCalendar.func(calendar_id=4))
def handle_calendar(call):
    vortex_plugin.callback_calendar(bot, call)


# обработчик кнопок плагина vortex
@bot.callback_query_handler(func=lambda call: True)
def handle_button(call):
    vortex_plugin.callback_query(bot, call)
    bot.answer_callback_query(call.id)


@bot.message_handler(content_types=['document'])
def handle_docs_audio(message):
    #    bot.reply_to(message, "Sorry, I don't work with documents.")
    pass


# default handler for every other text
@bot.message_handler(func=lambda message: True, content_types=['text'])
def command_default(message):
    # this is the standard reply to a normal message
    #    bot.send_message(m.chat.id, "I don't understand \"" + m.text + "\"\nMaybe try the help page at /help")
    pass


@bot.message_handler(func=lambda msg: msg.text == u'\U0001F4A9')
def set_ro(message):
    bot.send_message(message.chat.id, "Sorry, no shit posting.", reply_to_message_id=message.message_id)
    bot.restrict_chat_member(message.chat.id, message.from_user.id, until_date=time.time() + 31)


bot.infinity_polling()

# def telegram_polling():
#     """
#     https://github.com/eternnoir/pyTelegramBotAPI/issues/206
#     https://github.com/eternnoir/pyTelegramBotAPI/issues/401
#     """
#     try:
#         bot.polling(none_stop=True, timeout=100)  # constantly get messages from Telegram
#     except Exception as err:
#         logging.error(err)
#         bot.stop_polling()
#         print("Internet error!")
#         time.sleep(10)
#         telegram_polling()
#
#
# if __name__ == '__main__':
#     telegram_polling()
