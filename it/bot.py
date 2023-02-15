import ctypes
import logging
from optparse import Values
from select import select
from telegram import *
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters, ConversationHandler
from include import TOKEN, WEB_URL, CHAT_ID, countries
import os
import psutil


logger = logging.getLogger(__name__)



logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("Pass code:")
    return auth

async def auth(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if update.message.text == '1':
        reply_keyboard = []
        for country_object in countries:
            reply_keyboard.append([country_object['name']])

        await update.message.reply_text(
            "Country:",
            reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, input_field_placeholder="Country code."
            ),
        )
        return country
    else:
        await update.message.reply_text("Wrong pass code!")
        return ConversationHandler.END

async def country(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    for country_object in countries:
        if update.message.text == country_object['name']:
            for center_object in country_object['centers']:
                os.system('python3 main.py {} {}'.format(country_object['code'], center_object['code']))

async def appointment(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    for country_object in countries:
        if update.message.text == country_object['name']:
            for center_object in country_object['centers']:
                os.system('python3 main.py {} {}'.format(country_object['code'], center_object['code']))

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    #await update.message.reply_text('chrome' in (p.name() for p in psutil.process_iter()))
    for p in psutil.process_iter:
        print ()

async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")      

async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(
        "Bye! I hope we can talk again.", reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END
    

if __name__ == '__main__':
    application = ApplicationBuilder().token(TOKEN).build()

    # Add conversation handler with the states country, center, and mail
    conversation_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            auth: [MessageHandler(filters.TEXT, auth)],
            country: [MessageHandler(filters.TEXT, country)],
            appointment: [MessageHandler(filters.COMMAND, appointment)],
            status: [CommandHandler('status', status)]
        },
        fallbacks=[CommandHandler('stop', stop)],
    )

    application.add_handler(conversation_handler)

    # Status
    status_handler = CommandHandler('status', status)
    application.add_handler(status_handler)

    # Other handlers
    unknown_handler = MessageHandler(filters.COMMAND, unknown)
    application.add_handler(unknown_handler)
    
    application.run_polling()
    