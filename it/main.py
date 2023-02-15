
import logging
import random
import string
import sys
import time
from datetime import date, timedelta

import requests
import schedule
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

from include import CHAT_ID, TOKEN, WEB_URL, accounts

logger = logging.getLogger(__name__)
options = webdriver.ChromeOptions()
options.add_argument('---start-maximized')  
driver = webdriver.Chrome(options=options)
driver.implicitly_wait(30)


def login():
    driver.find_element(By.ID, 'email').clear()
    driver.find_element(By.ID, 'email').send_keys(random.choice(accounts))
    driver.find_element(By.ID, 'pwd').clear()
    driver.find_element(By.ID, 'pwd').send_keys('Pa$$w0rd')
    driver.find_element(By.CSS_SELECTOR, 'input.submit').click()
            

def create_application():
    driver.find_element(By.XPATH, '//input[contains(@onclick, "ajaxUpdater")]').click()
    time.sleep(5)

    # Purpose of Travel
    driver.execute_script('set_visa_purpose(`short_stay|tourism`);')
    time.sleep(1)

    time.sleep(5)
    # Personal Information
    driver.find_element(By.ID, 'f_pers_surnames').send_keys(''.join(random.choice(string.ascii_uppercase) for i in range(6)))
    time.sleep(1)

    driver.find_element(By.ID, 'f_pers_givennames').send_keys(''.join(random.choice(string.ascii_uppercase) for i in range(6)))
    time.sleep(1)

    driver.find_element(By.ID, 'f_pers_sex-M').click()
    time.sleep(1)
    
    birth_date = date.today() - timedelta(days=random.randint(21, 65)*365)
    driver.find_element(By.ID, 'f_pers_birth_date').send_keys(birth_date.strftime("%Y-%m-%d"))
    driver.find_element(By.ID, 'f_pers_birth_date').send_keys(Keys.ENTER)
    time.sleep(2)

    if len(driver.find_elements(By.ID, 'f_birth_place')) == 1:
        driver.find_element(By.ID, 'f_birth_place').send_keys(''.join(random.choice(string.ascii_uppercase) for i in range(6)))
        time.sleep(2)
    
    driver.find_element(By.ID, 'f_pass_num').send_keys(''.join(random.choice(string.ascii_uppercase) for i in range(2)))
    driver.find_element(By.ID, 'f_pass_num').send_keys(''.join(random.choice(string.digits) for i in range(6)))
    time.sleep(1)
    
    passport_issue_date = date.today() - timedelta(days=random.randint(1, 12)*30)
    driver.find_element(By.ID, 'fi_passport_issue_date').send_keys(passport_issue_date.strftime("%Y-%m-%d"))
    time.sleep(1)
    
    passport_expiry_date = passport_issue_date + timedelta(days=3650)
    driver.find_element(By.ID, 'fi_passport_expiry_date').send_keys(passport_expiry_date.strftime("%Y-%m-%d"))
    time.sleep(1)
    
    select = Select(driver.find_element(By.ID, 'f_pers_occupation'))
    select.select_by_index(2)
    time.sleep(3)

    select = Select(driver.find_element(By.ID, 'f_fami_marital_status'))
    select.select_by_index(random.randint(1, 5))
    time.sleep(3)

    driver.find_element(By.ID, 'f_pers_mobile_phone').send_keys(''.join(random.choice(string.digits) for i in range(10)))
    time.sleep(1)

    if len(driver.find_elements(By.ID, 'fi_trav_main_dest')) == 1:
        select = Select(driver.find_element(By.ID, 'fi_trav_main_dest'))
        select.select_by_index(1)
        time.sleep(1)

    trav_departure_date = date.today() + timedelta(days=random.randint(30, 60))
    driver.find_element(By.ID, 'f_trav_departure_date').send_keys(trav_departure_date.strftime("%Y-%m-%d"))
    driver.find_element(By.ID, 'f_trav_departure_date').send_keys(Keys.ENTER)
    time.sleep(3)

    trav_arrival_date = trav_departure_date + timedelta(days=random.randint(7, 21))
    driver.find_element(By.ID, 'f_trav_arrival_date').send_keys(trav_arrival_date.strftime("%Y-%m-%d"))
    driver.find_element(By.ID, 'f_trav_arrival_date').send_keys(Keys.ENTER)
    time.sleep(3)

    if len(driver.find_elements(By.ID, 'fi_need_legalisation-f')) == 1:
        driver.find_element(By.ID, 'fi_need_legalisation-f').click()
        time.sleep(2)

    driver.find_element(By.ID, "save_button").click()
    time.sleep(10)

    driver.switch_to.alert.accept()


def confirm_application():
    driver.find_element(By.XPATH, '//input[contains(@onclick, "confirm")]').click()
    time.sleep(3)
    driver.find_element(By.ID, 'ajaxConfirmCall_submit').click()


def find_appointment():
    if len(driver.find_elements(By.CSS_SELECTOR, 'a.dispo')) > 0:
        requests.get(url='https://api.telegram.org/bot{}/sendMessage'.format(TOKEN), params={'chat_id': CHAT_ID, 'text':sys.argv[1] + '-' + sys.argv[2] + '|' + str(len(driver.find_elements(By.CSS_SELECTOR, 'a.dispo')))})


def main():
    try:
        driver.get(WEB_URL + '/{}/{}/login.php'.format(sys.argv[1], sys.argv[2]))
        while driver.current_url.endswith('login.php'):
            login()
            time.sleep(5)
        if len(driver.find_elements(By.XPATH, '//input[contains(@onclick, "ajaxUpdater")]')) == 1:
            create_application()
            time.sleep(5)
            confirm_application()

        elif len(driver.find_elements(By.XPATH, '//input[contains(@onclick, "confirm")]')) == 1:
            confirm_application()

        else:
            find_appointment()
    except Exception as e:
        print(e)


if __name__ == '__main__':
    schedule.every(1).minutes.do(main)
    while True:
        schedule.run_pending()
        time.sleep(1)


    