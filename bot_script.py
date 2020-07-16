
import time
import pyqrcode  # pip install pyqrcode
import telebot  # pip install pyTelegramBotApi
from telebot import types
# Also, for qr generation you have to install pypng via pip (pip install pypng)

TOKEN = 'your_token'
bot = telebot.TeleBot(TOKEN)

print(f"Bot started at {time.ctime()}")

# emoji and other non-suitable symbols remover :) Actually, it works with latin only (ascii)

def removeEmoji(input_str):
    return input_str.encode('ascii', 'ignore').decode('ascii')


# print info about incoming message
def terminal_output(message):
    print(f"User: \n{message.from_user}\n"
          f"Message: {message.text}\n\n")


@bot.message_handler(commands=['start'])
def intro(message):
    terminal_output(message)
    intro_message = "Hi! \n" \
                    "Look what I can do:  \n" \
                    "/tlgrm_id - shows your Telegram ID\n" \
                    "/qr - generate QR code with your link\n"

    in_chat_markup = types.InlineKeyboardMarkup()
    link_btn = types.InlineKeyboardButton(text='MyGit', url='https://github.com/Dimaryst')
    in_chat_markup.add(link_btn)

    bot.send_message(message.chat.id, intro_message, reply_markup=in_chat_markup)


@bot.message_handler(commands=['qr'])
def txt2qr(message):
    terminal_output(message)
    bot.send_message(message.chat.id, "Send me the text to generate QR code. \n"
                                      "Make sure that your message does not contain any emoji. "
                                      "Unfortunately, I can't create QR with emoji 😔 ")
    bot.register_next_step_handler(message, txt2qr2)


def txt2qr2(message):
    terminal_output(message)
    if message.content_type == 'text':
        qr = pyqrcode.create(removeEmoji(message.text))
        qr.png('last.png', scale=5)
        qr_pic = open('last.png', 'rb')
        bot.send_message(message.chat.id, "Done! Your QR Code: ")
        bot.send_photo(message.chat.id, qr_pic)
    else:
        bot.send_message(message.chat.id, "Error. Try again.")


@bot.message_handler(commands=['tlgrm_id'])
def tlgrm_id(message):
    terminal_output(message)
    bot.send_message(message.chat.id, f"Your Telegram ID: {message.chat.id}")


bot.polling(none_stop=True)
