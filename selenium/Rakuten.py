from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import configparser
import time
import datetime

config = configparser.ConfigParser()  # 注意大小寫
config.read("./sc.ini")  # 配置檔案的路徑

DRIVER_PATH = config['main']['DRIVER_PATH']
URL = config['main']['URL']
ACC = config['main']['ACC']
PWD = config['main']['PWD']

options = webdriver.ChromeOptions()
# options.add_argument('--no-sandbox')
# options.add_argument("--disable-notifications")
# options.add_argument('--disable-gpu')
# options.add_argument('blink-settings=imagesEnabled=false')
# options.add_argument('--disable-javascript')
# options.add_argument('--disable-plugins')
options.add_argument('--user-data-dir=C:\\Users\\User\\AppData\\Local\\Google\\Chrome\\User Data')
driver = webdriver.Chrome(executable_path=DRIVER_PATH, chrome_options=options)
driver.delete_all_cookies()
driver.maximize_window()
driver.get(URL)
driver.set_page_load_timeout(30)
target = '10:59:55'
now_time = datetime.datetime.now()
target_time = datetime.datetime.strptime(
    str(now_time.date().year) + "-" + str(now_time.date().month) + "-" + str(
        now_time.date().day) + ' ' + target, "%Y-%m-%d %H:%M:%S")
if now_time > target_time:
    while True:
        try:
            WebDriverWait(driver, 5).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "cart-button-container")))
            driver.find_elements_by_class_name("cart-button-container")[1].click()
            # WebDriverWait(driver, 5).until(EC.presence_of_element_located(
            #     (By.CLASS_NAME, 'big-red-button.large-button.purchaseButton.ratTrackingEvent')))
            driver.find_elements_by_class_name("big-red-button large-button purchaseButton ratTrackingEvent").click()
            break
        except:
            time.sleep(1)
            pass
else:
    time.sleep(1)
"""==================================================================================="""
# WebDriverWait(driver, 5).until(expected_conditions.presence_of_element_located(
#     (By.NAME, 'u'))).send_keys(ACC)
# WebDriverWait(driver, 5).until(expected_conditions.presence_of_element_located(
#     (By.NAME, 'p'))).send_keys(PWD)
# WebDriverWait(driver, 5).until(expected_conditions.presence_of_element_located((By.NAME, 'login_submit'))).click()
"""==================================================================================="""
# driver.find_element_by_class_name("big-red-button.large-button.ratTrackingEvent").click()
driver.quit()
