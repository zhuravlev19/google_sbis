import time
import os
import zipfile
import fnmatch
import re
import mylib

from datetime import date, datetime, timedelta
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from mylib import driver


# Функция запуска драйвера браузера
def driver_start(chromedriver, userdata):
    """запускает хром драйвер, позволяющий рабоать с браузером. в аргументы передвется путь к хромдрайверу и user data"""
    s = Service(chromedriver)
    options = webdriver.ChromeOptions()
    options.add_argument(f"--user-data-dir={userdata}")
    # options.add_argument('--headless')
    mydriver = webdriver.Chrome(service=s, options=options)
    return mydriver

# Функиця открытия вкладок
def tab_open_list(urls, mydriver):
    """открывает список ссылок в новых вкладках, принимает список и объект драйвер"""
    urls_long = len(urls)   #определяем длину списка
    i = 0
    while i < urls_long:
        new_tab = f"window.open('{urls[i]}')"
        if i == 0:
            driver.get(urls[i])
            i += 1
            time.sleep(0.5)
        else:
            mydriver.execute_script(new_tab)
            i += 1
            time.sleep(0.5)
    time.sleep(10)

# Старая функция скачивания таблиц
def file_download(file_name: str = None, key_down: int = 0):
    # driver.switch_to.window(driver.window_handles[2])
    actionchains = ActionChains(driver)
    file = driver.find_element(by=By.XPATH, value=f"//div[text()='{file_name}']")
    time.sleep(1)
    actionchains.context_click(file).perform()
    time.sleep(1)
    i = 0
    while i < key_down:
        actionchains.send_keys(Keys.DOWN).perform()
        time.sleep(0.5)
        i += 1
    actionchains.send_keys(Keys.ENTER).perform()

# Найти по списку и распокавать архивы (Старая)
def found_unzip(directory, filename, finaldirectory):
    for file in os.listdir(directory):
        if fnmatch.fnmatch(file, '*.zip'):
            fstring = file
            # print(fstring)
            ssrting = filename
            # print(ssrting)
            if ssrting in fstring:
                print(f'Файл найден! "{file}"')
                arc = zipfile.ZipFile(f'{directory}/{file}', 'r')
                archlist = arc.namelist()
                list_len = len(archlist)
                i = 0
                while i < list_len:
                    arc.extract(archlist[i], finaldirectory)
                    i += 1
                else:
                    print('Распаковано')
        else:
            pass


# Функция получения даты последнего прихода
def get_lastdate():
    driver.switch_to.window(driver.window_handles[1])
    print(driver.current_url)
    time.sleep(1)
    try:
        driver.find_element(by=By.XPATH, value="//span[@title='Сбросить']").click()
        time.sleep(1)
    except Exception as ex:
        pass
    finally:
        last_purchases_date = driver.find_element(by=By.XPATH,
                                                  value="//div[@class='edo3-Browser-DateNumber  ']/div").text
        start = datetime.strptime(last_purchases_date, "%d.%m.%y")
        now = datetime.now()
        formated = now.strftime("%d-%m-%Y")
        end = datetime.strptime(formated, "%d-%m-%Y")
        date_generated = [start + timedelta(days=x) for x in range(1, (end - start).days)]
        print(last_purchases_date)
    return date_generated

# Функиция скачивания папки с приходами
def download_folder(a):
    for date in a:
        driver.switch_to.window(driver.window_handles[2])
        print(driver.current_url)
        time.sleep(2)
        folder_name = date.strftime("Приходы  %m %d")
        file_download(folder_name, 9)



def find_document(listdt, driver):
    files_list = []
    for date in listdt:
        driver.switch_to.window(driver.window_handles[0])
        document_name = date.strftime("разблюдовка %m %d")
        folder_name = date.strftime("Приходы %m %d ")
        files_list.append(folder_name)
        forxpath = f"//div[text()='{document_name}']"
        actionchains = ActionChains(driver)
        find_doc = driver.find_element(by=By.XPATH, value=forxpath)
        time.sleep(2)
        actionchains.double_click(find_doc).perform()
        time.sleep(3)
        driver.switch_to.window(driver.window_handles[3])
        time.sleep(10)
        print(driver.current_url)
        driver.find_element(by=By.XPATH, value="//div[text()='Форматирование']").click()
        time.sleep(1)
        driver.find_element(by=By.XPATH, value="//div[text()='Сформировать приходы для СБИС']").click()
        time.sleep(1)
        driver.close()

    return files_list

# Функция цикла кликов. Получает список xpatch-ей
def cycle_of_click(list, driver):
    # Цикл нажатия на каждый элемент их списка
    for path in list:
        mylib.find_click(path, driver)
        time.sleep(0.5)


def load_file(driver, folder_name, last_date):
    link_to_file = f'C:\\Приходы\\{folder_name}'
    files = os.listdir(link_to_file)
    start = datetime.strptime(last_date, "%d.%m.%y")
    now = datetime.now()
    formated = now.strftime("%d-%m-%Y")
    end = datetime.strptime(formated, "%d-%m-%Y")
    date_generated = [start + timedelta(days=x) for x in range(1, (end - start).days)]
    datagen_len = len(date_generated)
    print(datagen_len)
    print(date_generated)
    for date in date_generated:
        for file in files:
            now = datetime.now()
            for_xpath_date = now.strftime("%d.%m.%y")
            paths = [
                "//i[@class='controls-Button__icon controls-BaseButton__icon icon-DownloadNew controls-icon_size-m controls-icon_style-secondary controls-icon icon-DownloadNew']",
                "//div[text()='С компьютера']",
                "//div[text()=' Локальный диск (C:) ']",
                "//div[text()=' Приходы ']",
                f"//div[text()=\' {folder_name} \']",
                f"//div[text()=\'{file}\']",
                        ]
            cycle_of_click(paths, driver)
            time.sleep(5)
            mylib.find_click(f"//div[text()='{for_xpath_date}']", driver)
            for_input = date.strftime("%d.%m.%y")
            data_input = mylib.find("//div[text()='00.00.00']/preceding-sibling::input", driver)

            print(folder_name)
            print(for_input)
            data_input.send_keys(for_input)
            time.sleep(0.5)

            paths = [
                "//span[text()='Поставщик']",
                "//span[text()='Козлочков Алексей Владимирович, ИП']",
            ]
            cycle_of_click(paths, driver)

            time.sleep(0.5)
            paths = [
                "//span[text()='Поставщик']",
                "//span[text()='Козлочков Алексей Владимирович, ИП']",
            ]
            cycle_of_click(paths, driver)
            paths = [
                "//span[text()='Разобрать']",
                "//div[text()='Приход']",
            ]
            cycle_of_click(paths, driver)
            j = {
                "Козлочков Алексей Владимирович, ИП": ["Кудринка", "Серебрянка"],
                "Козлочкова Наталья Ивановна, ИП": ["Палатка", "СЭМЗ"],
                "Козлочков Иван Алексеевич, ИП": ["Просвещения", "Ветеран", "ООО"],
                "Романова Екатерина Алексеевна, ИП": ["Московский 2", "Легостаева", "Московский"],
                "Романов Алексей Сергеевич, ИП": ["Татьяна", "Озеро", "Новая палатка"],
                "Чернова Олеся Анатольевна, ИП": ["Заветы", "Агро", "Победа"]
            }
            tochka = re.sub(r'.[a-z][^\w\s]+|[\d]+', r'', file).strip()
            tochka_clear = tochka.replace('.xlsx', '')
            print(tochka)
            print(tochka_clear)
            for key in j:
                a = key
                values = j.get(a)
                for value in values:
                    if value == tochka_clear:
                        paths2 = [
                            "//div[@class='whd-document__organisationSelector-wrapper ws-ellipsis']",
                            f"//div[@class='entityChoice-Stack__column--name ws-flex-shrink-1 ws-ellipsis   ']/span[text()='{a}']",
                            "//span[@class='wnccore-lookup-selector-item-default controls-SelectedCollection__item__caption-default']",
                            ]
                        paths3 = [
                            f"//div[text()='{tochka_clear}']",
                            "//span[text()='Сохранить']",
                        ]
                        cycle_of_click(paths2, driver)
                        try:
                            driver.find_element(by=By.XPATH,
                                                value="//span[@class='controls-FilterView__iconReset icon-CloseNew']").click()
                        except:
                            pass
                        cycle_of_click(paths3, driver)

        else:
            print('готово')


def my_pass():
    pass


def element_action(driver, XPvalue, attempts=5, click='no', exeption_action=my_pass()):
    a = 0
    try:
        while True:
            try:
                if a == attempts:
                    pass
                else:
                    if click == 'no':
                        element = driver.find_element(by=By.XPATH, value=XPvalue)
                        return element
                    else:
                        driver.find_element(by=By.XPATH, value=XPvalue).click
                break
            except Exception:
                a += 1
                print(f'Попытка: {a}')
                time.sleep(0.3)
    except:
        exeption_action



def main():
    driver.get('https://online.sbis.ru/page/purchases')
    load_file(driver, 'Приходы  11 13', '12.11.22')


if __name__ == '__main__':
    main()

