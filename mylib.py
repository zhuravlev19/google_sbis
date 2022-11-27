import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

s = Service('C:/Users/Admin/PycharmProjects/pythonProject1/chromedriver/chromedriver.exe')
user_data = "C:/Users/Admin/AppData/Local/Google/Chrome/User Data"
options = webdriver.ChromeOptions()
options.add_argument(f"--user-data-dir={user_data}")
driver = webdriver.Chrome(service=s, options=options)


# Функция поиска элемента на странице, нажатия на него и задержки после
def find_click(XPvalue, driver):
    a = 0
    while True:
        try:
            if a == 10:
                pass
            else:
                driver.find_element(by=By.XPATH, value=XPvalue).click()
            break
        except Exception:
            a += 1
            time.sleep(0.8)


# Функция поиска элемента на странице, нажатия на него и задержки после
def find(XPvalue, driver):
    a = 0
    while True:
        try:
            if a == 10:
                pass
            else:
                element = driver.find_element(by=By.XPATH, value=XPvalue)
            break
        except Exception:
            a += 1
            time.sleep(0.8)
    return element