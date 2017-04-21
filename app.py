import os
import telebot
import imdb
from flask import Flask, request
import config

bot = telebot.TeleBot(config.token)
app = Flask(__name__)
ia = imdb.IMDb() # by default access the web

@bot.message_handler(commands=["start"])
def test(message):
    user_markup = telebot.types.ReplyKeyboardMarkup(True, True)
    user_markup.row("Actor", "Title")
    user_markup.row("Character")
    bot.send_message(message.from_user.id, 'Choose menu:', reply_markup=user_markup)

@bot.message_handler(func=lambda mess: "Actor" == mess.text or "Title" == mess.text or "Character" == mess.text, content_types=['text'])
def search(message):
    if (message.text == "Actor"):
        bot.send_message(message.chat.id, "Write name:")
        bot.register_next_step_handler(message, searchartist)
    elif (message.text == "Title"):
        bot.send_message(message.chat.id, "Write title:")
        bot.register_next_step_handler(message, searchfilm)
    elif (message.text == "Character"):
        bot.send_message(message.chat.id, "Write character name:")
        bot.register_next_step_handler(message, charactersearch)

def searchartist(msg):
    S = "Nothing found"
    S1 = ""
    s_result = ia.search_person(msg.text)
    if " " in msg.text:
        the_unt = s_result[0]
        ia.update(the_unt)
        try:
            if len(the_unt.data['actor'])<5:
                bot.send_message(msg.chat.id, the_unt['bio'])
            else:
                S = "Filmlist to long. View last 10 films:\n"
                for i in range(0,10):
                    S = S + str(the_unt.data['actor'][i]) + "\n"
            S1 = str(the_unt['name']) + " http://www.imdb.com/name/nm"+str(the_unt.personID) + "\n"
        except LookupError:
            if len(the_unt.data['actress'])<5:
                bot.send_message(msg.chat.id, the_unt['bio'])
            else:
                S = "Filmlist to long. View last 10 films:\n"
                for i in range(0,10):
                    S = S + str(the_unt.data['actress'][i]) + "\n"
            S1 = str(the_unt['name']) + " http://www.imdb.com/name/nm"+str(the_unt.personID) + "\n"
    else:
        S = "Try to input full name"
        for item in s_result:
            S = S + item['name'].encode('utf-8') + " http://www.imdb.com/name/nm"+str(item.personID) + "\n"
    if len(S1) != 0:
        bot.send_message(msg.chat.id, S1)
        bot.send_message(msg.chat.id, S)

def searchfilm(msg):
    s_result = ia.search_movie(msg.text)
    S = "Nothing found"
    for item in s_result:
        S = S + item['long imdb canonical title'].encode('utf-8') + " http://www.imdb.com/title/tt" + str(item.movieID) + "\n"
    bot.send_message(msg.chat.id, S)

def charactersearch(msg):
    s_result = ia.search_character(msg.text)
    S = "Nothing found"
    for item in s_result:
        S = S + item['long imdb canonical title'].encode('utf-8') + " http://www.imdb.com/title/tt" + str(item.movieID) + "\n"
    bot.send_message(msg.chat.id, S)

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
