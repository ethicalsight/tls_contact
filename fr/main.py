import ctypes
import logging
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters, ConversationHandler
from include import TOKEN, WEB_URL, countries
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import requests
import json
import random
import string
import time

logger = logging.getLogger(__name__)

selected_center = ''


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("Pass code:")
    return auth

async def auth(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if update.message.text == 'q':
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
    
    driver = webdriver.Chrome()
    driver.get(WEB_URL + '/MA/AGA/login.php')

    time.sleep(5)
    driver.save_screenshot('test.png')

    driver.close() 
                                           

                

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
            country: [MessageHandler(filters.TEXT, country)]
        },
        fallbacks=[CommandHandler('stop', stop)],
    )

    application.add_handler(conversation_handler)

    # Other handlers
    unknown_handler = MessageHandler(filters.COMMAND, unknown)
    application.add_handler(unknown_handler)
    
    application.run_polling()
    