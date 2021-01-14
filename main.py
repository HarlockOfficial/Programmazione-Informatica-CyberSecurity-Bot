#!/usr/bin/env python

import bot_token

from telegram.ext import Updater, CommandHandler, CallbackContext
from telegram import Update, bot

from time import time


users = dict()
otp = "0000"

def is_banned(user: str) -> bool:
    with open("ban.log", "r") as f:
        if user in f.readlines():
            return True
    return False


def start(update: Update, context: CallbackContext):
    if is_banned(str(update.message.chat.username)+","+str(update.message.chat.id)):
        return
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
    if is_banned(str(update.message.chat.username)+","+str(update.message.chat.id)):
        return
    if update.message.chat.username in users.keys() and time() - users[update.message.chat.username] <= 30:
        update.message.reply_text("Errore, puoi fare una domanda ogni 30 secondi")
        return
    users[update.message.chat.username] = time()
    # Domande durante i webinar limite antispam 1 domanda/min
    update.message.reply_text("hai chiesto una cosa, presto riceverai una risposta")
    pass


def info(update: Update, context: CallbackContext):
    # gruppo informatica, contatti e link (cartella/materiale/...)
    update.message.reply_text("info e link magici")
    pass


def beer(update: Update, context: CallbackContext):
    # paypal link
    update.message.reply_text("Se ti dovessero piacere i webinar, sentiti libero di offrirci una birra!\n")
    pass


def today(update: Update, context: CallbackContext):
    update.message.reply_text("ferb, so cosa faremo oggi")
    pass


def login(update: Update, context: CallbackContext):
    # TODO implement add otp and login admin
    pass


def ban(update: Update, context: CallbackContext):
    # TODO add user to ban.log by username (search in users.log)
    pass


def main():
    updater = Updater(bot_token.TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", bot_help))
    dp.add_handler(CommandHandler("ask", ask))
    dp.add_handler(CommandHandler("info", info))
    dp.add_handler(CommandHandler("beer", beer))
    dp.add_handler(CommandHandler("today", today))

    # admin functions
    dp.add_handler(CommandHandler("login", login))
    dp.add_handler(CommandHandler("ban", ban))

    # Invia Notifica a tutti i loggati (chiunque ha fatto start)
    with open("users.log", "r") as f:
        user_list = f.readlines()
        for user in user_list:
            user_id = user.split(",")[1]
            bot.Bot(bot_token.TOKEN).send_message(chat_id=user_id, text="Il meet inizierà a breve")

    print("Bot Started")
    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
