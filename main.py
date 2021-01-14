#!/usr/bin/env python

import bot_token

from telegram.ext import Updater, CommandHandler, CallbackContext
from telegram import Update, bot


def start(update: Update, context: CallbackContext):
    with open("users.log", "r+") as f:
        content = f.readlines()
        if not str(update.message.chat.username)+","+str(update.message.chat.id) in content:
            f.write(str(update.message.chat.username)+","+str(update.message.chat.id))
    update.message.reply_text("Benvenuto al Webinar di Sicurezza Informatica.\n" +
                              "Il bot sarà attivo solo durante i webinar.\n" +
                              "Per scoprire tutte le funzionalità, digita il comando /help")


def bot_help(update: Update, context: CallbackContext):
    update.message.reply_text("hai chiesto aiuto")


def ask(update: Update, context: CallbackContext):
    # Domande durante i webinar limite antispam 1 domanda/min
    update.message.reply_text("hai chiesto una cosa, presto riceverai una risposta")
    pass


def info(update: Update, context: CallbackContext):
    # gruppo informatica, contatti e link (cartella/materiale/...)
    update.message.reply_text("info e link magici")
    pass


def coffee(update: Update, context: CallbackContext):
    # paypal link
    update.message.reply_text("toss a coin to your witcher")
    pass


def today(update: Update, context: CallbackContext):
    update.message.reply_text("ferb, so cosa faremo oggi")
    pass


def main():
    updater = Updater(bot_token.TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", bot_help))
    dp.add_handler(CommandHandler("ask", ask))
    dp.add_handler(CommandHandler("info", info))
    dp.add_handler(CommandHandler("coffee", coffee))
    dp.add_handler(CommandHandler("today", today))

    # Invia Notifica a tutti i loggati (chiunque ha fatto start)
    with open("users.log", "r") as f:
        user_list = f.readlines()
        for user in user_list:
            username, user_id = user.split(",")
            print("Notification sent to:", username)
            bot.Bot(bot_token.TOKEN).send_message(chat_id=user_id, text="Il meet inizierà a breve")

    print("Bot Started")
    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
