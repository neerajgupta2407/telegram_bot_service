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
from apis.apisetu.apisetu import ApiSetu
apisetu = ApiSetu()

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context.

class Constants:
    welcome_text = "Hi. Welcome to the bot"
    help_text = "How can i help you."
    list_states_txt = "Listing States\n"
    show_district = "Below are the Districts is {state_name}"
    selected_district = "Selected District is {district_name}"
    unknown_command = "OOps...We didn't recognise the command: {text}"


class Commands:
    start = 'start'
    help = 'help'
    states = "States"
    more_options = "More Options"
    state_pretext = 'State: '
    district_pretext = "District: "


    reply_keyboards = {
        'default': [
            [states],
            [help, more_options]
        ]
    }

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

def build_state_name(state_name):
    return Commands.state_pretext + state_name
def build_district_name(district_name):
    return Commands.district_pretext + district_name
def create_reply_keyboard(options: list)-> list :
    return [[l] for l in options]


def echo(update: Update, _: CallbackContext) -> None:
    """Echo the user message."""
    text = update.message.text
    reply_text = ""
    reply_keyboard = Commands.reply_keyboards.get('default')
    if text == Commands.start:
        reply_text = Constants.welcome_text
    elif text == Commands.help:
        reply_text = Constants.help_text
    elif text == Commands.states:
        states = State.objects.all().order_by('state_name')
        reply_text = Constants.list_states_txt
        reply_keyboard = create_reply_keyboard([build_state_name(state.state_name) for state in states])

    elif text.startswith(Commands.state_pretext):
        state_name = text.replace(Commands.state_pretext,'')
        reply_text =  Constants.show_district.format(state_name=state_name)
        districts = District.objects.filter(state__state_name=state_name)
        reply_keyboard = create_reply_keyboard([build_district_name(d.district_name) for d in districts])
    elif text.startswith(Commands.district_pretext):
        district_name = text.replace(Commands.district_pretext,"")
        # reply_text = Constants.selected_district.format(district_name=district_name)
        district = District.objects.get(district_name=district_name)
        centers = apisetu.get_appointments_by_district(district.district_id)
        reply_text = "\n".join([str(obj) for obj in centers])
        # Ask for agre. If user is lookig for slot for 18 or 45.


    else:
        reply_text = Constants.unknown_command.format(text=text)
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