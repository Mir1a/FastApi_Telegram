import requests
import telebot
import webbrowser
from config import BOT

from telebot import types


def send_message(bottoken: str, chatid: str, message: str) -> str:
    url = f"https://api.telegram.org/bot{bottoken}/sendMessage"
    payload = {"chat_id": chatid, "text": message}
    response = requests.post(url, data=payload)
    return response.text


bot = telebot.TeleBot(BOT)

user_initialized = {}


@bot.message_handler(content_types=['text', 'photo'])
def start(message):
    user_id = message.from_user.id
    if user_id not in user_initialized:
        user_initialized[user_id] = True
        markup = types.ReplyKeyboardMarkup()
        btn1 = types.KeyboardButton("ссылки🔗")
        btn2 = types.KeyboardButton("/start👋")
        btn3 = types.KeyboardButton("фотка📷")
        btn4 = types.KeyboardButton('🆔')
        btn5 = types.KeyboardButton("/help🆘")
        btn6 = types.KeyboardButton("/infoℹ️")
        markup.row(btn1, btn2)
        markup.row(btn3, btn4)
        markup.row(btn5, btn6)
        bot.send_message(message.chat.id, "Hi", reply_markup=markup)
    else:
        info(message)


def info(message):
    if message.content_type == 'photo':
        bot.send_message(message.chat.id, "это фото")
    elif message.content_type == 'text':
        text = message.text.lower()
        if "привет" in text:
            bot.send_message(message.chat.id, "И тебе привет")
        elif "Предскажи будущее" in text:
            bot.send_message(message.chat.id, "У тебя всё будет отлично")
        elif text == "🆔":
            bot.reply_to(message, f'id: {message.from_user.id}')
        elif text == "/help🆘":
            bot.send_message(message.chat.id, "Ты сейчас общаешься ботом, созданным Miria для тестирования и обучения "
                                              "библиотеке telebot")
        elif text == "/infoℹ️":
            bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name}, ниже будет собрана вся '
                                              f'информация, которую бот получает после того как ты напишешь ему хотя '
                                              f'бы одно сообщение: {message}')
        elif text == "/start👋":
            bot.send_message(message.chat.id, "Привет")
        elif text == "/site":
            bot.send_message(message.chat.id, "https://github.com/Mir1a")
        elif text == "фотка📷":
            file = open('./sondjinvoo_potok.png', 'rb')
            bot.send_photo(message.chat.id, file)
        elif "ссылки" in text:
            markup = types.InlineKeyboardMarkup()
            btn1 = types.InlineKeyboardButton("github", url="https://github.com/Mir1a")
            btn2 = types.InlineKeyboardButton("linkidin", url="https://www.linkedin.com/in/matvey-bliznyuk-a735ab303/")
            btn3 = types.InlineKeyboardButton('Удалить', callback_data='delete')
            btn4 = types.InlineKeyboardButton("Изменить", callback_data='edit')
            markup.row(btn1, btn2)
            markup.row(btn3, btn4)
            bot.reply_to(message, "Твои ссылки", reply_markup=markup)


@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):
    if callback.data == "delete":
        bot.delete_message(callback.message.chat.id, callback.message.message_id)
    elif callback.data == 'edit':
        bot.edit_message_text('edit text', callback.message.chat.id, callback.message.message_id)


def start_bot():
    bot.polling(non_stop=True)
