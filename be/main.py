import ctypes
import logging
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters, ConversationHandler
from include import TOKEN, WEB_URL, API_URL, countries
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
    for country_object in countries:
        if update.message.text == country_object['name']:
            for center_object in country_object['centers']:
                try:
                    jsessionid = login(WEB_URL + country_object['code'] + '/' + country_object['code'] + center_object['code'] + '2be/home')
                    while(True):
                        print('...')
                        response = requests.get(API_URL + '/formgroup', headers={'Cookie': 'JSESSIONID=' + jsessionid}, data={'client': 'be', 'issuer': country_object['code'] + center_object['code'] + '2be'})
                        if response.status_code == requests.codes.ok:
                            if len(response.json()) > 0:
                                response = requests.get(API_URL + '/appointment', headers={'Cookie': 'JSESSIONID=' + jsessionid}, data={'client': 'be', 'issuer': country_object['code'] + center_object['code'] + '2be', 'formGroupId': response.json()[0]['fg_id'], 'appointmentType': 'Long Stay Application _Appointment'})
                                if response.status_code == requests.codes.ok:
                                    for date_ in response.json().keys():
                                        for time_ in response.json()[date_].keys():
                                            if response.json()[date_][time_] > 0:
                                                if update.message.text != date_:
                                                    await update.message.reply_text(date_)
                        else:
                            jsessionid = login(WEB_URL + country_object['code'] + '/' + country_object['code'] + center_object['code'] + '2be/home')
                        time.sleep(300)                         

                except:
                    return ConversationHandler.END
                finally:
                    return ConversationHandler.END   

async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")      

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(
        "Bye! I hope we can talk again.", reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END
                
def login(url) -> string:
    driver = webdriver.Chrome()
    driver.get(url)
    element = WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable((By.CLASS_NAME, 'tls-button-link'))
    )
    element.click()
    element = WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable((By.ID, 'kc-login'))
    )
    driver.find_element(By.ID, 'username').send_keys('royiki6095@laluxy.com')
    driver.find_element(By.ID, 'password').send_keys('Pa$$w0rd')
    element.click()
    element = WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable((By.XPATH, "//a[contains(@class, 'tls-navbar-slot--myapplication')]"))
    )

    jsessionid = driver.get_cookie('JSESSIONID')['value']
    driver.close() 
    return jsessionid


if __name__ == '__main__':
    application = ApplicationBuilder().token(TOKEN).build()

    # Add conversation handler with the states country, center, and mail
    conversation_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            auth: [MessageHandler(filters.TEXT, auth)],
            country: [MessageHandler(filters.TEXT, country)]
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    application.add_handler(conversation_handler)

    # Other handlers
    unknown_handler = MessageHandler(filters.COMMAND, unknown)
    application.add_handler(unknown_handler)
    
    application.run_polling()