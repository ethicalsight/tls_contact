import sys
import time

from selenium import webdriver
from selenium.webdriver.common.by import By

from include import WEB_URL, countries

if __name__ == '__main__':
    options = webdriver.ChromeOptions()
    options.add_argument("--window-size=1920,1080")
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(60)

    for country in countries:
        if country['code'] == sys.argv[1]:
            for center in country['centers']:
                driver.get(WEB_URL + '/{}/{}/register.php'.format(country['code'], center['code']))
                driver.find_element(By.ID, 'u_email').send_keys(sys.argv[2])
                driver.find_element(By.ID, 'u_email_confirm').send_keys(sys.argv[2])
                driver.find_element(By.ID, 'u_password').send_keys('Pa$$w0rd')
                driver.find_element(By.ID, 'u_password_confirm').send_keys('Pa$$w0rd')
                driver.find_element(By.ID, 'create_user').click()

                time.sleep(2)

                for radio in driver.find_elements(By.XPATH, '//input[@type="radio"]'):
                    radio.click()
                driver.find_element(By.ID, 'consent_button').click()
                time.sleep(2)
                driver.delete_all_cookies()
                                                   
                time.sleep(15)
    driver.close()
    driver.quit()
            