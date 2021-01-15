#!/usr/bin/env python

import bot_token

from telegram.ext import Updater, CommandHandler, CallbackContext
from telegram import Update, bot

from time import time

# used to block spam
users = dict()


def is_banned(user: str) -> bool:
    with open("ban.log", "r") as f:
        if user in f.readlines():
            return True
    return False


def is_admin(user: str) -> bool:
    with open("admin.log", "r") as f:
        if user in f.readlines():
            return True
    return False


def start(update: Update, unused: CallbackContext):
    if is_banned(str(update.message.chat.username)+","+str(update.message.chat.id)):
        return
    with open("users.log", "r+") as users_log:
        content = users_log.readlines()
        if not str(update.message.chat.username)+","+str(update.message.chat.id) in content:
            users_log.write(str(update.message.chat.username)+","+str(update.message.chat.id))
            users_log.flush()
    update.message.reply_text("Benvenuto al Webinar di Sicurezza Informatica.\n" +
                              "Il bot sarà attivo solo durante i webinar.\n" +
                              "Per scoprire tutte le funzionalità, digita il comando /help")


def bot_help(update: Update, unused: CallbackContext):
    update.message.reply_text("hai chiesto aiuto")


def ask(update: Update, unused: CallbackContext):
    if is_banned(str(update.message.chat.username)+","+str(update.message.chat.id)):
        return
    if update.message.chat.username in users.keys() and time() - users[update.message.chat.username] <= 30:
        update.message.reply_text("Errore, puoi fare una domanda ogni 30 secondi")
        return
    users[update.message.chat.username] = time()
    update.message.reply_text("La tua domanda è stata notificata, presto riceverai una risposta")
    print(update.message.chat.username, "ha chiesto:", update.message.text)
    with open("admin.log", "r") as admin_log:
        for user in admin_log.readlines():
            user_id = user.split(",")[1]
            bot.Bot(bot_token.TOKEN).send_message(chat_id=user_id,
                                                  text="Se devi bannare l'utente " + update.message.chat.username +
                                                  "puoi usare /ban " + update.message.chat.username)


def info(update: Update, unused: CallbackContext):
    # gruppo informatica, contatti e link (cartella/materiale/...)
    update.message.reply_text("info e link magici")
    pass


def beer(update: Update, unused: CallbackContext):
    # paypal link
    update.message.reply_text("Se ti dovessero piacere i webinar, sentiti libero di offrirci una birra!\n")
    pass


def today(update: Update, unused: CallbackContext):
    update.message.reply_text("ferb, so cosa faremo oggi")
    pass


def ban(update: Update, unused: CallbackContext):
    if not is_admin(str(update.message.chat.username)+","+str(update.message.chat.id)):
        return
    user_to_ban = update.message.text
    with open("users.log", "r") as users_log:
        users_list = users_log.readlines()
        for i in range(len(users_list)):
            if user_to_ban == users_list[i].split(",")[0]:
                with open("ban.log", "a") as ban_log:
                    ban_log.write(users_list[i])
                    ban_log.flush()
                break


def main():
    updater = Updater(bot_token.TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", bot_help))
    dp.add_handler(CommandHandler("ask", ask))
    dp.add_handler(CommandHandler("info", info))
    dp.add_handler(CommandHandler("beer", beer))
    dp.add_handler(CommandHandler("today", today))

    # admin function
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
