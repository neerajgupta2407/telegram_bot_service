#!/usr/bin/env python
# pylint: disable=C0116
# This program is dedicated to the public domain under the CC0 license.

"""
Simple Bot to reply to Telegram messages.

First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import logging

from telegram import Update, ForceReply, ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

from app.models import State, District
# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context.
def start(update: Update, _: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Hi {user.mention_markdown_v2()}\!',
        reply_markup=ForceReply(selective=True),
    )


def help_command(update: Update, _: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def echo(update: Update, _: CallbackContext) -> None:
    """Echo the user message."""
    text = update.message.text
    reply_text = ""
    reply_keyboard = [
        ["start"],
        ["States"],
        ["Welcome"]
    ]
    state_pretext = "State: "
    district_pretext = "District: "
    if text == '/start':
        reply_text = "Hi. Welcome to the bot"
    elif text in ["/help", 'help']:
        reply_text = "How can i help you."
    elif text == "States":
        states = State.objects.all().order_by('state_name')
        reply_text = "Listing States\n"
        reply_keyboard = [
            [state_pretext + state.state_name] for state in states]

    elif text.startswith(state_pretext):
        state_name = text.replace(state_pretext,'')
        reply_text = f"Below are the Districts is {state_name}"
        districts = District.objects.filter(state__state_name=state_name)
        reply_keyboard = [
            [district_pretext + d.district_name]
            for d in districts
        ]
    elif text.startswith(district_pretext):
        district_name = text.replace(district_pretext,"")
        reply_text = f"Selected District is {district_name}"

    else:
        reply_text = f"OOps...We didn't recognise the command: {text}"
    update.message.reply_text(reply_text, reply_markup=ReplyKeyboardMarkup(reply_keyboard,))


def main() -> None:
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    token = '1870682730:AAE7kRRCTmc_6HZ6P9DHVZC2kVRazvU82_M'
    updater = Updater(token)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    # dispatcher.add_handler(CommandHandler("start", start))
    # dispatcher.add_handler(CommandHandler("help", help_command))

    # on non command i.e message - echo the message on Telegram
    dispatcher.add_handler(MessageHandler(Filters.text, echo))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()