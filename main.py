import telebot
import config
from telebot import types

bot = telebot.TeleBot(config.TOKEN)


TOTAL_SUM = ''
START_OF_RANGE = ''
END_OF_RANGE = ''
RESULT = ''
LIST = []


@bot.message_handler(commands=['start', 'help'])
def welcome_message(message):
    send_mess = f'''
Welcome, {message.from_user.first_name}! This bot is designed to calculate the integer division of the total in a specified range of numbers.

Respond to bot requests.

TOTAL SUM - the number from which the results of all integer divisions will be found.

START OF RANGE - corresponds the beginning of the range of numbers from which the divisors are to be found.

END OF RANGE - corresponds to the end of this range. lol

Enter message 'go' or tap key 'GO'!
 
'''
    keyboard = types.ReplyKeyboardMarkup()
    key_go = types.KeyboardButton(text='GO')
    keyboard.add(key_go)
    bot.send_message(message.chat.id, send_mess, reply_markup=keyboard)


@bot.message_handler(func=lambda m: True)
def echo(message):
    try:
        if message.text == 'go' or message.text == 'GO':
            bot.send_message(message.from_user.id, 'Enter the TOTAL SUM: ')
            bot.register_next_step_handler(message, total_sum)
    except Exception:
        bot.reply_to(message, 'Something went wrong...')


def total_sum(message):
    try:
        global TOTAL_SUM

        TOTAL_SUM = int(message.text)
        bot.send_message(message.from_user.id, 'Enter the START OF RANGE: ')
        bot.register_next_step_handler(message, start_of_range)
    except Exception:
        img = open('img/error.tgs', 'rb')
        bot.send_sticker(message.chat.id, img)
        bot.reply_to(message, 'Something went wrong...')


def start_of_range(message):
    try:
        global START_OF_RANGE

        START_OF_RANGE = int(message.text)
        bot.send_message(message.from_user.id, 'Enter the END OF RANGE: ')
        bot.register_next_step_handler(message, end_of_range)
    except Exception:
        img = open('img/error.tgs', 'rb')
        bot.send_sticker(message.chat.id, img)
        bot.reply_to(message, 'Something went wrong...')


def end_of_range(message):
    try:
        global END_OF_RANGE
        global LIST
        global RESULT

        RESULT = ''
        LIST = []
        END_OF_RANGE = int(message.text)
        for i in range(int(START_OF_RANGE), int(END_OF_RANGE) + 1):
            if int(TOTAL_SUM) % i == 0:
                LIST.append(str(i))
        print(LIST)
        RESULT = '\n'.join(e for e in LIST)
        if len(LIST) > 0:
            for i in LIST:
                bot.send_message(message.from_user.id, f'{TOTAL_SUM} : {str(i)} = {int(TOTAL_SUM) / int(i)}')
            img = open('img/result.tgs', 'rb')
            bot.send_sticker(message.chat.id, img)
        else:
            img = open('img/none_result.tgs', 'rb')
            bot.send_sticker(message.chat.id, img)
            bot.send_message(message.from_user.id, 'No results!')
    except Exception:
        img = open('img/error.tgs', 'rb')
        bot.send_sticker(message.chat.id, img)
        bot.reply_to(message, 'Something went wrong...')


bot.enable_save_next_step_handlers(delay=2)
bot.load_next_step_handlers()

if __name__ == '__main__':
    bot.polling(none_stop=True)
