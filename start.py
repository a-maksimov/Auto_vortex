def handle_start_help(bot, message):
    if message.chat.type == 'private':
        if message.chat.username:
            bot.send_message(message.chat.id, f'Привет, {message.chat.first_name}! Отправьте /help, чтобы узнать '
                                              f'доступные команды')
    else:
        bot.send_message(message.chat.id, f'Greetings, {message.chat.title}! Отправьте /help, чтобы узнать '
                                              f'доступные команды')
