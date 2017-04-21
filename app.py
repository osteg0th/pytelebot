import os
import telebot
import imdb
import config

from flask import Flask, request

bot = telebot.TeleBot(config.token)
app = Flask(__name__)
ia = imdb.IMDb() # by default access the web

@bot.message_handler(commands = ["start"])
def test(message):
    user_markup = telebot.types.ReplyKeyboardMarkup(True, True)
    user_markup.row("Actor", "Title")
    user_markup.row("Character")
    bot.send_message(message.from_user.id, 'Choose menu:', reply_markup=user_markup)

@bot.message_handler(func=lambda mess: "Actor" == mess.text or "Title" == mess.text or "Keywords" == mess.text, content_types=['text'])
def search(message):
    if (message.text == "Actor"):
        bot.send_message(message.chat.id, "Write name:")
        bot.register_next_step_handler(message, config.searchartist)
    elif (message.text == "Title"):
        bot.send_message(message.chat.id, "Write title:")
        bot.register_next_step_handler(message, config.searchfilm)
    elif (message.text == "Character"):
        bot.send_message(message.chat.id, "Write character name:")
        bot.register_next_step_handler(message, config.searchfilm)

@app.route("/" + config.token, methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "POST", 200

@app.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url="https://pytelebot.herokuapp.com/" + config.token)
    return "CONNECTED", 200

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=os.environ.get('PORT', 5000))
#app.run(host="0.0.0.0", port=os.environ.get('PORT', 5000))