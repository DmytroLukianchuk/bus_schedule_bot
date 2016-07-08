import config
import telebot
from telebot import types
import functions
from flask import Flask
import os


bot = telebot.TeleBot(config.token)


# server = Flask(__name__)


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Hello, ' + message.from_user.first_name + " " +
                     message.from_user.last_name + config.WELCOME_HELP)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    itembtna = types.KeyboardButton('/%s' % config.FROM_Z)
    itembtnb = types.KeyboardButton('/%s' % config.FROM_O)
    itembtnc = types.KeyboardButton('/%s' % config.SCHEDULE_Z)
    itembtnd = types.KeyboardButton('/%s' % config.SCHEDULE_O)
    markup.row(itembtna, itembtnb)
    markup.row(itembtnc, itembtnd)
    bot.send_message(message.chat.id, 'Choose what you wanna do next from the following options: ', reply_markup=markup)


@bot.message_handler(commands=[('%s' % config.FROM_Z)])
def from_village(message):
    bot.send_message(message.chat.id, 'Your closest bus from Zaria is @:\n' + functions.find_nerest(config.bus_time_Z), parse_mode='HTML')


@bot.message_handler(commands=['%s' % config.FROM_O])
def from_city(message):
    bot.send_message(message.chat.id,
                     'Your closest bus from Ostrovskogo is @:\n' + functions.find_nerest(config.bus_time_O))


@bot.message_handler(commands=['%s' % config.SCHEDULE_O])
def schedule_from_city(message):
    bot.send_message(message.chat.id, 'Schedule from Ostrovskogo:\n' + str(functions.schedule(config.bus_time_O)))


@bot.message_handler(commands=['%s' % config.SCHEDULE_Z])
def schedule_from_village(message):
    bot.send_message(message.chat.id, 'Schedule from Zaria:\n' + str(functions.schedule(config.bus_time_Z)))


@bot.message_handler(content_types=["text"])
def repeat_all_messages(message):
    bot.reply_to(message, config.USE_START_COMMAND)


# server.run(host="0.0.0.0", port=os.environ.get('PORT', 5000))


if __name__ == '__main__':
    bot.polling(none_stop=True)
