from flask import Flask, request
import telebot

import config
import functions


app = Flask(__name__)
bot = telebot.TeleBot(config.token)


bot.set_webhook(url="https://schedulebot.herokuapp.com/hook")


@app.route("/")
def index():
    return "Hi"


@app.route("/hook", methods=['POST'])
def webhook():
    json_string = request.get_data()
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_messages([update.message])
    return "OK"


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Hello, ' + message.from_user.first_name + " " +
                     message.from_user.last_name + config.WELCOME_HELP)
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    itembtna = telebot.types.KeyboardButton('/%s' % config.FROM_Z)
    itembtnb = telebot.types.KeyboardButton('/%s' % config.FROM_O)
    itembtnc = telebot.types.KeyboardButton('/%s' % config.SCHEDULE_Z)
    itembtnd = telebot.types.KeyboardButton('/%s' % config.SCHEDULE_O)
    markup.row(itembtna, itembtnb)
    markup.row(itembtnc, itembtnd)
    bot.send_message(message.chat.id, 'Choose what you wanna do next from the following options: ', reply_markup=markup)


@bot.message_handler(commands=[('%s' % config.FROM_Z)])
def from_village(message):
    bot.send_message(message.chat.id, 'Your closest bus from Zaria is @:\n' + functions.find_nerest(config.bus_time_Z))


@bot.message_handler(commands=['%s' % config.FROM_O])
def from_city(message):
    bot.send_message(message.chat.id,
                     'Your closest bus from Ostrovskogo is @:\n' + functions.find_nerest(config.bus_time_O))


@bot.message_handler(commands=['%s' % config.SCHEDULE_O])
def schedule_from_city(message):
    bot.send_message(message.chat.id, parse_mode="HTML", text='Schedule from <b>Ostrovskogo</b>:\n' + '<b>' +
                                                              str(functions.schedule(config.bus_time_O)) + '</b>')


@bot.message_handler(commands=['%s' % config.SCHEDULE_Z])
def schedule_from_village(message):
    bot.send_message(message.chat.id, 'Schedule from Zaria:\n' + str(functions.schedule(config.bus_time_Z)))


@bot.message_handler(content_types=["text"])
def repeat_all_messages(message):
    bot.reply_to(message, config.USE_START_COMMAND)

