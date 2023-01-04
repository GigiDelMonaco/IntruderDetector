
#IntruderDetector_Bot
import time
import telebot
from telebot import types
from telebot import apihelper
import urllib.request


bot = telebot.TeleBot('YOUR BOT TOKEN HERE')

apihelper.SESSION_TIME_TO_LIVE = 5 * 60

markup_remove = types.ReplyKeyboardRemove(selective=False)
"""
     COMMANDS
"""
@bot.message_handler(commands=['start'])
def welcome(message):
    bot.reply_to(message, "Alarm detector started!")


@bot.message_handler(commands=['help'])
def help(message):
    bot.reply_to(message, "In case of intruder, i will send you a picture")


@bot.message_handler(commands=['take_picture'])
def sendPhoto(message):
    photo = urllib.request.urlopen('http://YOUR IP ADDRESS/cam-lo.jpg')
    bot.send_photo(message.chat.id, photo)



while True:
    try:
        bot.infinity_polling(skip_pending=True)
    except:
        time.sleep(5)
        continue