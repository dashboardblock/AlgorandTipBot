import os
import logging
import models
import algo_handler

from telegram import Update
from telegram.ext import (
    Updater,
    CommandHandler,
    CallbackContext,
)


logging.basicConfig(filename='algorandtipbot.log',
                            filemode='a',
                            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                            datefmt='%H:%M:%S',
                            level=logging.DEBUG)

logger = logging.getLogger(__name__)


def balance_handler(update: Update, context: CallbackContext)-> None:
    username = update.effective_user.username.lower()
    chat = update.effective_chat
    if chat.type == 'private':
        if username is None:
            update.message.reply_text("Please set a telegram username in your profile settings!")
        else:
            algo_handler.check_account(username)
            context.bot.send_message(chat_id=chat.id, text=("Your balance: {} ALGO".format(algo_handler.get_balance(username))))
    else:
        update.message.reply_text("Run this command in @algorandtipbot private chat!")

def deposit_handler(update: Update, context: CallbackContext)-> None:
    username = update.effective_user.username.lower()
    chat = update.effective_chat
    if chat.type == 'private':
        if username is None:
            update.message.reply_text("Please set a telegram username in your profile settings!")
        else:
            algo_handler.check_account(username)
            context.bot.send_message(chat_id=chat.id, text="Your Algorand address for deposit:")
            context.bot.send_message(chat_id=chat.id, text=(models.fetch_user(username)[0][1]))
    else:
        update.message.reply_text("Run this command in @algorandtipbot private chat!")

def withdraw_handler(update: Update, context: CallbackContext)-> None:
    username = update.effective_user.username.lower()
    chat = update.effective_chat
    if chat.type == 'private':
        if username is None:
            update.message.reply_text("Please set a telegram username in your profile settings!")
        else:
            algo_handler.check_account(username)
            context.bot.send_message(chat_id=chat.id, text="Your passphrase:")
            context.bot.send_message(chat_id=chat.id, text=(models.fetch_user(username)[0][3]))
    else:
        update.message.reply_text("Run this command in @algorandtipbot private chat!")


def on_start(update: Update, context: CallbackContext)-> None:
    chat = update.effective_chat
    username = update.effective_user.username.lower()
    algo_handler.check_account(username)
    if chat.type == 'private':
        if username is None:
            update.message.reply_text("Please set a telegram username in your profile settings!")
        else:
            context.bot.send_message(chat_id=chat.id, text='''
            Hello {}! Your AlgorandTipBot wallet is 
            {}\n\nYou can deposit ALGO and start tipping community members!
            |- /start : Starting again
            |- /balance : Check wallet balance
            |- /deposit : View your deposit address
            |- /withdraw : View your passphrase
            |- /tip : Tip someone on Telegram
            |- /help : Learn how to tip someone on Telegram\n\nYou can support further development by tipping to @AlgorandTipBot
            '''.format(username, models.fetch_user(username)[0][1]))
    else:
        update.message.reply_text("Run this command in @algorandtipbot private chat!")


def help_message(update: Update, context: CallbackContext)-> None:
    chat = update.effective_chat
    context.bot.send_message(chat_id=chat.id, text='''
You can tip ALGO on Telegram:\n
Make sure you and the recipient have a @username configured in the telegram settings.\n
Reply to a user with the command `/tip @username [AMOUNT]` to tip that user in a channel with @AlgorandTipBot\n
The following commands are also at your disposal: /start , /help , /tip, /balance , /deposit, /withdraw\n\nYou can support further development by tipping to @AlgorandTipBot\n
You can write on @MaksimF for any issues you encounter with the bot.
    ''')

def tip_handler(update: Update, context: CallbackContext):
    chat = update.effective_chat
    username = update.effective_user.username.lower()
    text = update.message.text[5:]
    try:
        target =  text.split(" ")[0]
        amount =  float(text.split(" ")[1])
        if username is None:
            update.message.reply_text("Please set a telegram username in your profile settings!")
        else:
            if ((target[0] != '@') or (amount <= 0)):
                context.bot.send_message(chat_id=chat.id, text="Please use correct command: /tip @username amount")
            else:
                target = target[1:].lower()
                status = algo_handler.send_tip(username,target,amount)
                context.bot.send_message(chat_id=update.message.chat_id, text=status)
    except IndexError:
        context.bot.send_message(chat_id=chat.id, text="Please use correct command: /tip @username amount")
    except ValueError:
        context.bot.send_message(chat_id=chat.id, text="Please use correct command: /tip @username amount")
        raise

  
def main():
    """Start the bot"""
    updater = Updater(token=os.getenv('BOT_API', 'Token Not found'), use_context=True)
  
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('balance', balance_handler))
    dispatcher.add_handler(CommandHandler('deposit', deposit_handler))
    dispatcher.add_handler(CommandHandler('tip', tip_handler))
    dispatcher.add_handler(CommandHandler('withdraw', withdraw_handler))
    dispatcher.add_handler(CommandHandler('help', help_message))
    dispatcher.add_handler(CommandHandler("start", on_start))
  
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()