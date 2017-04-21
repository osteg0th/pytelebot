import os
import telebot

import config
from flask import request

@config.bot.message_handler(commands = ["start"])
def test(message):
    user_markup = telebot.types.ReplyKeyboardMarkup(True, True)
    user_markup.row("Actor", "Title")
    user_markup.row("Character")
    config.bot.send_message(message.from_user.id, 'Choose menu:', reply_markup=user_markup)

@config.bot.message_handler(func=lambda mess: "Actor" == mess.text or "Title" == mess.text or "Keywords" == mess.text, content_types=['text'])
def search(message):
    if (message.text == "Actor"):
        config.bot.send_message(message.chat.id, "Write name:")
        config.bot.register_next_step_handler(message, config.searchartist)
    elif (message.text == "Title"):
        config.bot.send_message(message.chat.id, "Write title:")
        config.bot.register_next_step_handler(message, config.searchfilm)
    elif (message.text == "Character"):
        config.bot.send_message(message.chat.id, "Write character name:")
        config.bot.register_next_step_handler(message, config.searchfilm)

@config.app.route("/" + config.token, methods=['POST'])
def getMessage():
    config.bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "POST", 200

@config.app.route("/")
def webhook():
    config.bot.remove_webhook()
    config.bot.set_webhook(url="https://pytelebot.herokuapp.com/" + config.token)
    return "CONNECTED", 200

if __name__ == '__main__':
    config.app.run(host="0.0.0.0", port=os.environ.get('PORT', 5000))
#app.run(host="0.0.0.0", port=os.environ.get('PORT', 5000))