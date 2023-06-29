from selenium import webdriver
from PIL import Image, ImageFilter
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import time
import sqlite3
from anticaptchaofficial.imagecaptcha import *
from database import Database
from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QIcon
from out_table import Ui_Form
import sys



def main(numbers):
    print("[+]------------------Начало работы программы-----------------[+]\n")
    def get_captcha():
        print("[+]--------------Получаем капчу--------------[+]")
        ele_captcha = driver.find_element(By.XPATH, '//*[@id="imgCaptcha"]')
        src = ele_captcha.get_attribute('src')
        time.sleep(1)
        img_captcha = ele_captcha.screenshot_as_png
        with open('captcha.jpg', 'wb') as f:
            f.write(img_captcha)
                
    # SOLVE CAPTCHA
    def solve_captcha():
        with open("key.txt", "r", encoding="utf-8") as f:
            key = f.read().strip()
            key = "".join(key).split()
        try:
            print(f"[+]--------------API ключ: {key[0]}--------------[+]")
            print("[+]--------------Отправка капчи в обработку--------------[+]")
            solver = imagecaptcha()
            solver.set_verbose(1)
            solver.set_key(f"{key[0]}")
            solver.set_soft_id(0)
            captcha_text = solver.solve_and_return_solution("captcha.jpg")
            if captcha_text != 0:
                return captcha_text.strip()
        except Exception as e:
            print("[+]--------------Произошла ошибка, перезапустите программу!--------------[+]")
            driver.close()

        
    o = Options()
    # o.add_experimental_option("detach", True)
    o.add_argument("--headless")

    driver = webdriver.Chrome("chrome", chrome_options=o)
    driver.get("https://checkvehicle.sfri.ru/AppCheckVehicle/app/main")
    db = Database()

    def insert_data(num):
        if num != "":
            driver.find_element(By.XPATH, '//*[@id="fldNum"]').send_keys(num)
            try:
                get_captcha()
            except Exception as e:
               print("[+]--------------Проблемы с подключением, пожалуйста перезапустите программу!--------------[+]")
               driver.close()
            time.sleep(2)
            driver.find_element(By.XPATH, '//*[@id="fldCaptcha"]').send_keys(solve_captcha())
            time.sleep(2)
            driver.find_element(By.XPATH, '//*[@id="btnSend"]').click()
            result = driver.find_element(By.XPATH, '/html/body/div[4]/div[3]').get_attribute('textContent')
            if result.strip() == "ТС эксплуатируется инвалидом или используется для перевозки инвалида":
                print("[+]--------------ТС используется инвалидом--------------[+]")
                return "ТС эксплуатируется инвалидом или используется для перевозки инвалида"
            elif result.strip() == "ТС не эксплуатируется инвалидом и не используется для перевозки инвалида":
                print("[+]--------------ТС не используется инвалидом--------------[+]")
                return "ТС не эксплуатируется инвалидом и не используется для перевозки инвалида"
            elif result.strip() == "Проверочный код введен неверно":
                print("[+]--------------Проверочный код введен неверно, повтор операции--------------[+]")
                return "Проверочный код введен неверно"
        else:
            print("Проблемы с подключением, пожалуйста перезапустите программу!")
            driver.close()

    count = 0
    while True:
        print(f"[+]--------------ОБРАБОТАНО: {count} из {len(numbers)}---------------------[+]\n")
        print(f"[+]--------------Отправка номера {numbers[count]} в обработку--------------[+]\n")
        info = insert_data(numbers[count])
        print(info)
        if  info == "Проверочный код введен неверно":
            driver.find_element(By.XPATH, '//*[@id="btnRetry"]').click()
            time.sleep(1)
        else:
            if db.get_description(number=str(numbers[count]))[0] == info:
                count += 1
                if count == len(numbers):
                    break
                driver.find_element(By.XPATH, '//*[@id="btnRetry"]').click()
            else:
                db.update_description(description=str(info), number=numbers[count])
                count += 1
                if count == len(numbers):
                    break
                driver.find_element(By.XPATH, '//*[@id="btnRetry"]').click()
        
    print(f"[+]--------------Автомобильные номера в количестве {len(numbers)} штук прошли проверку в базе!--------------[+]")
    driver.close()
    


    
    
