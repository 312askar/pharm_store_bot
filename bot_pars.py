from config import TOKEN
import telebot
from telebot import types
import requests
import shutil
from lib_sql.sql_config import db

# bot init
bot = telebot.TeleBot(TOKEN)

# echo
@bot.message_handler(commands=['start'])
def send_welcome_message(message):
    text = "Welcome to our PharmStore, please input correct url for parsing:"
    bot.send_message(message.from_user.id, f"{message.from_user.first_name}, {text}")

# get picture
def get_file(url):
    response = requests.get(url, stream=True)
    return response

def save_data(name, file_data):
    file = open(name, 'bw') #Бинарный режим, изображение передається байтами
    for chunk in file_data.iter_content(4096): # Записываем в файл по блочно данные
        file.write(chunk)
    shutil.move(name, 'images') # move picture to directory

def get_name(url):
    name = url.split('/')[-1]
    return name

@bot.message_handler()
def get_image_url(message: types.Message):
    url = message.text
    print(get_file(url))
    save_data(get_name(url), get_file(url))
    bot.send_message(message.from_user.id, f"{get_name(url)} have been downloaded to directory 'images'")


bot.infinity_polling()
