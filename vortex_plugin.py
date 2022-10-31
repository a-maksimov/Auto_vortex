import config
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from telegram_bot_calendar import WYearTelegramCalendar
from datetime import date
from SQLighter import SQLighter
from correct_number import correct_number

LSTEP = {'y': 'год', 'm': 'месяц', 'd': 'день'}


# user_id = 346521502
# user_id = 267560822  # Настин user_id

# начало воронки
def markup_start():
    markup = InlineKeyboardMarkup()
    item1 = InlineKeyboardButton('Скрыть', callback_data='hide')
    markup.row(item1)
    item2 = InlineKeyboardButton('Давно', callback_data='long_ago')
    item3 = InlineKeyboardButton('Недавно', callback_data='not_long_ago')
    markup.row(item2, item3)
    return markup


# предложение записи на маникюр
def markup_nails():
    markup = InlineKeyboardMarkup()
    item1 = InlineKeyboardButton('Записаться 📅', callback_data='calendar_nails')
    item2 = InlineKeyboardButton('Скрыть', callback_data='hide')
    markup.add(item1, item2)
    return markup


# предложение записи на мейкап
def markup_makeup():
    markup = InlineKeyboardMarkup()
    item1 = InlineKeyboardButton('Записаться 📅', callback_data='calendar_makeup')
    item2 = InlineKeyboardButton('Скрыть', callback_data='hide')
    markup.add(item1, item2)
    return markup


# предложение записи на стайлинг
def markup_styling():
    markup = InlineKeyboardMarkup()
    item1 = InlineKeyboardButton('Записаться 📅', callback_data='calendar_styling')
    item2 = InlineKeyboardButton('Скрыть', callback_data='hide')
    markup.add(item1, item2)
    return markup


# предложение записи на массаж лица
def markup_face_massage():
    markup = InlineKeyboardMarkup()
    item1 = InlineKeyboardButton('Записаться 📅', callback_data='calendar_face_massage')
    item2 = InlineKeyboardButton('Скрыть', callback_data='hide')
    markup.add(item1, item2)
    return markup


# предложение записи на остальные процедуры
def markup_other():
    markup = InlineKeyboardMarkup()
    item1 = InlineKeyboardButton('Скрыть', callback_data='hide')
    markup.row(item1)
    item2 = InlineKeyboardButton('Маникюр 💅', callback_data='book_nails')
    item3 = InlineKeyboardButton('Мейкап 💄', callback_data='book_makeup')
    item4 = InlineKeyboardButton('Стайлинг 💇', callback_data='book_styling')
    markup.row(item2, item3, item4)
    item5 = InlineKeyboardButton('Массаж лица 💆', callback_data='book_face_massage')
    markup.row(item5)
    return markup


def start_vortex(bot, message):
    markup = markup_start()
    bot.send_message(message.chat.id, f'Привет, {message.chat.first_name}!\n'
                                      f'Я Вортекс из Индустрии красоты.\n'
                                      f'Как давно вы делали 💅?',
                     reply_markup=markup)


def step_set_first_name(message, bot, call, cal_id):
    first_name = message.text  # принимаем имя от пользователя
    # проверяем, является ли имя буквой или словом
    if not first_name.isalpha():
        msg = bot.send_message(message.chat.id, 'Имя должно состоять из букв',
                               reply_to_message_id=message.message_id)
        bot.register_next_step_handler(msg, step_set_first_name, bot, call, cal_id)  # если не буква, и не слово, то
        # перезапускаем эту функцию
    else:
        first_name = first_name.capitalize()  # капитализируем имя
        msg = bot.send_message(call.message.chat.id, 'Ведите фамилию')
        bot.register_next_step_handler(msg, step_set_last_name, bot, call, cal_id, first_name)  # переходим в функцию
        # задания имени


def step_set_last_name(message, bot, call, cal_id, first_name):
    last_name = message.text  # принимаем фамилию от пользователя
    # проверяем, является ли фамилия буквой или словом
    if not last_name.isalpha():
        msg = bot.send_message(message.chat.id, 'Фамилия должна состоять из букв',
                               reply_to_message_id=message.message_id)
        bot.register_next_step_handler(msg, step_set_last_name, bot, call, cal_id, first_name)  # если не буква, и не
        # слово, то перезапускаем эту функцию
    else:
        last_name = last_name.capitalize()  # капитализируем фамилию
        msg = bot.send_message(call.message.chat.id, 'Ведите ваш номер телефона в формате "7-123-456-7890" 📲')
        bot.register_next_step_handler(msg, step_set_phone, bot, call, cal_id, first_name, last_name)  # переходим в
        # функцию задания телефона


def step_set_phone(message, bot, call, cal_id, first_name, last_name):
    global LSTEP
    phone = message.text  # принимаем номер телефона от пользователя
    # проверяем, является ли номер корректным
    if not correct_number(phone):
        msg = bot.send_message(message.chat.id, 'Номер телефона должен быть в формате "7-123-456-7890"',
                               reply_to_message_id=message.message_id)
        bot.register_next_step_handler(msg, step_set_phone, bot, call, cal_id, first_name, last_name)  # если
        # неправильный формат, то перезапускаем эту функцию
    else:
        client = (call.from_user.id, first_name, last_name, phone)
        add_client(client)  # добавляем клиента в таблицу
        calendar, step = WYearTelegramCalendar(calendar_id=cal_id, locale='ru',
                                               min_date=date.today()).build()  # формируем календарь
        if cal_id == 1:
            string = 'маникюр'
        elif cal_id == 2:
            string = 'мейкап'
        elif cal_id == 3:
            string = 'стайлинг'
        else:
            string = 'массаж лица'
        bot.send_message(call.message.chat.id, f'Выберите {LSTEP[step]} записи на {string}', reply_markup=calendar)


# обработчик календаря
def callback_calendar(bot, call):
    global LSTEP
    cal_id = int(call.data.split('_')[1])
    if cal_id == 1:
        string = 'маникюр 💅'
    elif cal_id == 2:
        string = 'мейкап 💄'
    elif cal_id == 3:
        string = 'стайлинг 💇'
    else:
        string = 'массаж лица 💆'

    result, key, step = WYearTelegramCalendar(calendar_id=cal_id, locale='ru', min_date=date.today()).process(call.data)
    if not result and key:
        bot.edit_message_text(f'Выберите {LSTEP[step]} записи на {string}',
                              call.message.chat.id, call.message.message_id, reply_markup=key)
    elif result:
        add_booking(call, call.from_user.id, result)
        bot.answer_callback_query(call.id, text='Дата выбрана')
        bot.edit_message_text(f'Вы записаны.\n'
                              f'Ждем вас {result} на {string}', call.message.chat.id, call.message.message_id)


# функция добавления нового клиента
def add_client(client):
    db_worker = SQLighter(config.database_name)
    db_worker.add_client(client)
    db_worker.close()


# функция добавления даты записи
# TODO: user_id is not unique for client if someone gets booked by another user_id
# TODO: and phone can't be passed to booking; try using increment id for booking
def add_booking(call, user_id, result):
    booking_date = (result.year, result.month, result.day)
    cal_id = int(call.data.split('_')[1])
    if cal_id == 1:
        table = 'calendar_nails'
    elif cal_id == 2:
        table = 'calendar_makeup'
    elif cal_id == 3:
        table = 'calendar_styling'
    else:
        table = 'calendar_face_massage'
    db_worker = SQLighter(config.database_name)
    db_worker.add_booking(user_id, table, booking_date)
    db_worker.close()


# обработчик кнопок
def callback_query(bot, call):
    req = call.data

    if req == 'hide':
        bot.delete_message(call.message.chat.id, call.message.message_id)

    elif req == 'long_ago':
        bot.delete_message(call.message.chat.id, call.message.message_id)
        markup = markup_nails()
        img_url = 'https://image.shutterstock.com/image-photo/close-process-manicure-beauty-salon-600w-174272696.jpg'
        title = 'В таком случае записываемся на маникюр 💅!'
        bot.send_photo(call.message.chat.id, img_url, caption=title, reply_markup=markup)

    elif req == 'not_long_ago':
        bot.delete_message(call.message.chat.id, call.message.message_id)
        markup = markup_other()
        bot.send_message(call.message.chat.id,
                         'Мы предлагаем широкий спектр бьюти-процедур.\n'
                         'На что хотите записаться?',
                         reply_markup=markup)

    elif req == 'book_nails':
        bot.delete_message(call.message.chat.id, call.message.message_id)
        markup = markup_nails()
        img_url = 'https://image.shutterstock.com/image-photo/close-process-manicure-beauty-salon-600w-174272696.jpg'
        title = 'Записываемся на маникюр 💅!'
        bot.send_photo(call.message.chat.id, img_url, caption=title, reply_markup=markup)

    elif req == 'book_makeup':
        bot.delete_message(call.message.chat.id, call.message.message_id)
        markup = markup_makeup()
        img_url = 'https://image.shutterstock.com/image-photo/make-products-prsented-on-white-600w-1885493167.jpg'
        title = 'Записываемся на мейкап!'
        bot.send_photo(call.message.chat.id, img_url, caption=title, reply_markup=markup)

    elif req == 'book_styling':
        bot.delete_message(call.message.chat.id, call.message.message_id)
        markup = markup_styling()
        img_url = 'https://image.shutterstock.com/image-photo/set-hairdressers-accessories-on-grey-600w-1695994237.jpg'
        title = 'Записываемся на стайлинг!'
        bot.send_photo(call.message.chat.id, img_url, caption=title, reply_markup=markup)

    elif req == 'book_face_massage':
        bot.delete_message(call.message.chat.id, call.message.message_id)
        markup = markup_face_massage()
        img_url = 'https://image.shutterstock.com/image-photo/woman-receiving-head-massage-bali-600w-1909994005.jpg'
        title = 'Записываемся на массаж лица!'
        bot.send_photo(call.message.chat.id, img_url, caption=title, reply_markup=markup)
    # запись на бьюти-услуги
    elif req == 'calendar_nails' or 'calendar_makeup' or 'calendar_styling' or 'calendar_face_massage':
        if req == 'calendar_nails':
            cal_id = 1
        elif req == 'calendar_makeup':
            cal_id = 2
        elif req == 'calendar_styling':
            cal_id = 3
        else:
            cal_id = 4
        msg = bot.send_message(call.message.chat.id, 'Ведите имя')
        bot.register_next_step_handler(msg, step_set_first_name, bot, call, cal_id)  # переходим в функцию задания имени
