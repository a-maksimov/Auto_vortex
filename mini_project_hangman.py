from random import sample
from telebot import types

word_list = ['Кант',
             'Хроника',
             'Зал',
             'Галера',
             'Балл',
             'Вес',
             'Кафель',
             'Знак',
             'Фильтр',
             'Башня',
             'Кондитер',
             'Омар',
             'Чан',
             'Пламя',
             'Банк',
             'Тетерев',
             'Муж',
             'Камбала',
             'Груз',
             'Кино',
             'Лаваш',
             'Калач',
             'Геолог',
             'Бальзам',
             'Бревно',
             'Жердь',
             'Борец',
             'Самовар',
             'Карабин',
             'Подлокотник',
             'Барак',
             'Мотор',
             'Шарж',
             'Сустав',
             'Амфитеатр',
             'Скворечник',
             'Подлодка',
             'Затычка',
             'Ресница',
             'Спичка',
             'Кабан',
             'Муфта',
             'Синоптик',
             'Характер',
             'Мафиози',
             'Фундамент',
             'Бумажник',
             'Библиофил',
             'Дрожжи',
             'Казино',
             'Конечность',
             'Пробор',
             'Дуст',
             'Комбинация',
             'Мешковина',
             'Процессор',
             'Крышка',
             'Сфинкс',
             'Пассатижи',
             'Фунт',
             'Кружево',
             'Агитатор',
             'Формуляр',
             'Прокол',
             'Абзац',
             'Караван',
             'Леденец',
             'Кашпо',
             'Баркас',
             'Кардан',
             'Вращение',
             'Заливное',
             'Метрдотель',
             'Клавиатура',
             'Радиатор',
             'Сегмент',
             'Обещание',
             'Магнитофон',
             'Кордебалет',
             'Заварушка']


# функция получения текущего состояния
def display_hangman(tries):
    stages = [  # финальное состояние: голова, торс, обе руки, обе ноги
        '''
--------
|      |
|    \U0001F480
|     \\|/
|      |
|     / \\
-
''',
        # голова, торс, обе руки, одна нога
        '''
--------
|      |
|    \U0001F975
|     \\|/
|      |
|     / 
-
''',
        # голова, торс, обе руки
        '''
--------
|      |
|    \U0001F914
|     \\|/
|      |
|      
-
''',
        # голова, торс и одна рука
        '''
--------
|      |
|    \U0001F610
|     \\|
|      |
|     
-
''',
        # голова и торс
        '''
 --------
|      |
|    \U0001F642
|      |
|      |
|     
-
''',
        # голова
        '''
--------
|      |
|    \U0001F605
|    
|      
|     
-
''',
        # начальное состояние
        '''
--------
|      |
|      
|    
|      
|     
-
'''
    ]
    return stages[tries]


def get_word(dictionary):
    random_word = sample(dictionary, 1)
    return random_word[0]


def char_spread(string):
    spread_string = ''
    for i in range(len(string)):
        spread_string += string[i] + ' '
    return spread_string


def check_letter(word, letter, string):
    for i in range(len(word)):
        if letter == word.lower()[i]:
            string = string[:i] + letter + string[i + 1:]
    return string


def check_word(message, bot, word, guess_word):
    # проверяем, что длина опробованного слова равна длине задуманного слова
    if not len(guess_word) == len(word):
        if len(guess_word) == 1:  # если длина слова 1, то это буква, поэтому выходим из функции со значением 0
            return 1
        else:  # если длина слова не равна загаданному, выходим из функции со значением 1
            bot.send_message(message.chat.id, f'\U0001F921 Слово должно быть из {len(word)} букв',
                             reply_to_message_id=message.message_id)
            return 2
    else:
        if guess_word == word.lower():  # если слово совпало с загаданным
            return 0
        else:
            return 3  # если слово не совпало с загаданным


def yes_or_no():
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True, one_time_keyboard=True)
    button1 = types.KeyboardButton('Да')
    button2 = types.KeyboardButton('Нет')
    markup.add(button1, button2)
    return markup


def step_play_again(message, bot):
    answer = message.text  # считываем ответ пользователя
    if 'да' not in answer.lower() and 'нет' not in answer.lower():
        # повторяем вопрос
        msg = bot.send_message(message.chat.id, 'Да или нет', reply_markup=yes_or_no())
        bot.register_next_step_handler(msg, step_play_again, bot)
    elif answer.lower() == 'да':
        play_hangman(bot, message)
    else:
        bot.send_message(message.chat.id, 'Пока! \U0001F44B')


def check_guessed(message, bot, guessed, tries):
    if guessed:
        bot.send_message(message.chat.id, 'Вы победили! \U0001F973')
        msg = bot.send_message(message.chat.id, 'Хотите сыграть еще? \U0001F480 Да/Нет', reply_markup=yes_or_no())
        bot.register_next_step_handler(msg, step_play_again, bot)  # переходим в функцию перезапуска игры
    else:
        bot.send_message(message.chat.id, 'Вас повесили')
        bot.send_message(message.chat.id, display_hangman(tries))  # отправляем повешенного в исходном состоянии
        msg = bot.send_message(message.chat.id, 'Хотите попробовать снова? \U0001F9DF Да/Нет', reply_markup=yes_or_no())
        bot.register_next_step_handler(msg, step_play_again, bot)  # переходим в функцию перезапуска игры


def play_hangman(bot, message):
    tries = 6
    word = get_word(word_list)  # выбираем случайное задуманное слово из списка

    bot.send_message(message.chat.id, 'Давайте сыграем в виселицу! \U0001F480',
                     reply_to_message_id=message.message_id)

    bot.send_message(message.chat.id, display_hangman(tries))  # отправляем повешенного в исходном состоянии

    msg = bot.send_message(message.chat.id, 'Открыть первую и последнюю буквы? \U0001F60F', reply_markup=yes_or_no())
    bot.register_next_step_handler(msg, step_set_start, bot, word, tries)


def step_set_start(message, bot, word, tries):
    guessed_letters = []  # список уже названных букв
    guessed_words = []  # список уже названных слов
    guessed = False  # сигнальная метка
    answer = message.text  # принимаем ответ пользователя о том, показать ли первую и последнюю буквы задуманного слова
    word_completion = '_' * len(word)  # строка, содержащая символы "_" на каждую букву задуманного слова

    if 'да' not in answer.lower() and 'нет' not in answer.lower():  # если в ответе пользователя нет ни "да", ни "нет"
        # повторяем вопрос
        msg = bot.send_message(message.chat.id, 'Да или нет?', reply_markup=yes_or_no())
        bot.register_next_step_handler(msg, step_set_start, bot, word)  # перезапускаем эту функцию
    elif answer.lower() == 'да':
        word_completion = word[0] + word_completion[1:len(word_completion) - 1] + word[
            -1]  # заменяем "_" в исходной строке на первую и последнюю буквы задуманного слова
        bot.send_message(message.chat.id, char_spread(word_completion))  # отображаем строку
        msg = bot.send_message(message.chat.id, 'Введите букву или слово')
        bot.register_next_step_handler(msg, step_set_guess, bot, word, word_completion,
                                       guessed_letters, guessed_words, guessed, tries)  # переходим в функцию угадывания
    else:
        bot.send_message(message.chat.id, char_spread(word_completion))  # отображаем исходную строку
        msg = bot.send_message(message.chat.id, 'Введите букву или слово')
        bot.register_next_step_handler(msg, step_set_guess, bot, word, word_completion,
                                       guessed_letters, guessed_words, guessed, tries)  # переходим в функцию угадывания


# функция угадывания
def step_set_guess(message, bot, word, word_completion, guessed_letters, guessed_words, guessed, tries):
    guess = message.text  # принимаем попытку от пользователя

    # проверяем, является ли ответ пользователя буквой или словом
    if not guess.isalpha():
        msg = bot.send_message(message.chat.id, 'Пожалуйста, введите букву или слово',
                               reply_to_message_id=message.message_id)
        bot.register_next_step_handler(msg, step_set_guess, bot, word,
                                       word_completion)  # если не буква, и не слово, то перезапускаем эту функцию
    else:
        guess = guess.lower()  # приводим все текстовые догадки к нижнему регистру

        # обработка слов
        if len(guess) > 1:

            # если данное слово уже есть в списке слов
            if guess in guessed_words:
                bot.send_message(message.chat.id, 'Это слово вы уже пробовали',
                                 reply_to_message_id=message.message_id)
                msg = bot.send_message(message.chat.id, 'Введите другое слово или букву')
                bot.register_next_step_handler(msg, step_set_guess, bot, word, word_completion,
                                               guessed_letters, guessed_words, guessed,
                                               tries)  # перезапускаем эту функцию
            else:
                guessed_words.append(guess)  # добавляем новое слово в список попробованных слов

                # переходим в проверку слова
                check_w = check_word(message, bot, word, guess)
                if check_w == 0:  # если слово совпало с загаданным
                    bot.send_message(message.chat.id, 'Правильно!',
                                     reply_to_message_id=message.message_id)
                    guessed = True
                    check_guessed(message, bot, guessed, tries)
                elif check_w == 1:  # если после слова была введена буква
                    # если данная буква уже есть в списке букв
                    if guess in guessed_letters:
                        bot.send_message(message.chat.id, 'Эту букву вы уже пробовали',
                                         reply_to_message_id=message.message_id)
                        msg = bot.send_message(message.chat.id, 'Введите другую букву или слово')
                        bot.register_next_step_handler(msg, step_set_guess, bot, word, word_completion,
                                                       guessed_letters, guessed_words, guessed,
                                                       tries)  # перезапускаем эту функцию
                    guessed_letters.append(guess)  # добавляем букву в список попробованных букв
                    word_completion_updated = check_letter(word, guess, word_completion)  # переходим в проверку буквы
                    if word_completion_updated == word_completion:
                        tries -= 1
                        bot.send_message(message.chat.id, 'Такой буквы нет!',
                                         reply_to_message_id=message.message_id)
                        bot.send_message(message.chat.id, char_spread(word_completion).capitalize())
                    else:
                        word_completion = word_completion_updated  # дополняем строку угаданными буквами
                        bot.send_message(message.chat.id, char_spread(word_completion).capitalize())
                elif check_w == 2:  # если длина слова не совпала с загаданным
                    msg = bot.send_message(message.chat.id, 'Введите букву или слово')
                    bot.register_next_step_handler(msg, step_set_guess, bot, word, word_completion,
                                                   guessed_letters, guessed_words, guessed,
                                                   tries)  # перезапускаем функция угадывания
                else:
                    bot.send_message(message.chat.id, '\U0001F921 Не угадали!',
                                     reply_to_message_id=message.message_id)
                    tries -= 1  # уменьшаем количество доступных попыток
                    if tries <= 0:  # проверяем, остались ли попытки
                        guessed = False
                        check_guessed(message, bot, guessed, tries)
                    else:  # если ещё остались попытки
                        bot.send_message(message.chat.id,
                                         display_hangman(tries))  # отображаем повешенного в новом состоянии
                        bot.send_message(message.chat.id,
                                         char_spread(
                                             word_completion).capitalize())  # отображаем строку с заполненными буквами
                        msg = bot.send_message(message.chat.id, 'Введите букву или слово')
                        bot.register_next_step_handler(msg, step_set_guess, bot, word, word_completion,
                                                       guessed_letters, guessed_words, guessed,
                                                       tries)  # перезапускаем эту функцию угадывания
        # обработка букв
        else:
            # если данная буква уже есть в списке букв
            if guess in guessed_letters:
                bot.send_message(message.chat.id, 'Эту букву вы уже пробовали',
                                 reply_to_message_id=message.message_id)
                msg = bot.send_message(message.chat.id, 'Введите другую букву или слово')
                bot.register_next_step_handler(msg, step_set_guess, bot, word, word_completion,
                                               guessed_letters, guessed_words, guessed,
                                               tries)  # перезапускаем эту функцию
            else:
                guessed_letters.append(guess)  # добавляем букву в список попробованных букв
                word_completion_updated = check_letter(word, guess, word_completion)  # переходим в проверку буквы
                if word_completion_updated == word_completion:
                    tries -= 1
                    bot.send_message(message.chat.id, 'Такой буквы нет!',
                                     reply_to_message_id=message.message_id)
                    bot.send_message(message.chat.id, char_spread(word_completion).capitalize())
                else:
                    word_completion = word_completion_updated  # дополняем строку угаданными буквами
                    bot.send_message(message.chat.id, char_spread(word_completion).capitalize())
                if word_completion.lower() == word.lower():  # если модифицированная строка совпала с загаданным
                    # словом -- победа!
                    guessed = True
                    check_guessed(message, bot, guessed, tries)
                else:
                    if tries <= 0:  # проверяем, остались ли попытки
                        guessed = False
                        check_guessed(message, bot, guessed, tries)
                    else:  # если ещё остались попытки
                        bot.send_message(message.chat.id,
                                         display_hangman(tries))  # отображаем повешенного в новом состоянии
                        msg = bot.send_message(message.chat.id, 'Введите букву или слово')
                        bot.register_next_step_handler(msg, step_set_guess, bot, word, word_completion,
                                                       guessed_letters, guessed_words, guessed,
                                                       tries)  # перезапускаем эту функцию угадывания
