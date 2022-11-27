import mylib
import os
import re
import time
from datetime import datetime
from mylib import driver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

folder_name = "Инвентаризации 11 20"
a = ['https://drive.google.com/drive/u/0/folders/1eLIxNdUhNaUVi2rlNNF5ekhZGHlRP6rb',
     'https://drive.google.com/drive/u/0/folders/1n6R50IOR3eTFcIDVbZ-jBBs-HXLYC2yt',
     'https://online.sbis.ru/page/purchases']


link_to_file = f'C:\\Инвентаризации\\{folder_name}'
files = os.listdir(link_to_file)
print(files)
driver.get('https://online.sbis.ru/page/internal-docs')
time.sleep(3)


def load_invent(driver, file_name, folder_name, invent_date):
    now = datetime.now()
    for_xpath_date = now.strftime("%d.%m.%y")
    paths = [
        "//i[@class='controls-Button__icon controls-BaseButton__icon icon-DownloadNew controls-icon_size-m controls-icon_style-secondary controls-icon icon-DownloadNew']",
        "//div[text()='С компьютера']",
        "//div[text()=' Локальный диск (C:) ']",
        "//div[text()=' Инвентаризации ']",
        f"//div[text()=\' {folder_name} \']",
        f"//div[text()=\'{file_name}\']",
        f"//div[text()=\'{for_xpath_date}\']"
    ]
    paths2 = [
        "//span[text()='1']",
        "//span[text()='Разобрать']",
        "//div[text()='Шаблон инвентаризации']",
        "//span[text()='Переключиться']",
        "//div[@class='edo3-DocumentName__overlay']"
    ]

    for patch in paths:
        mylib.find_click(patch, driver)

    while True:
        try:
            data_input = driver.find_element(by=By.XPATH, value="//div[text()='00.00.00']/preceding-sibling::input")
            data_input.send_keys(invent_date)
            time.sleep(1)
            data_input.send_keys(Keys.ENTER)
            break
        except Exception as ex:
            time.sleep(0.5)

    time.sleep(2)
    j = {
        "Козлочков Алексей Владимирович, ИП": ["Кудринка", "Серебрянка"],
        "Козлочкова Наталья Ивановна, ИП": ["Палатка", "СЭМЗ"],
        "Козлочков Иван Алексеевич, ИП": ["Просвещения", "Ветеран", "ООО"],
        "Романова Екатерина Алексеевна, ИП": ["Московский 2", "Легостаева", "Московский"],
        "Романов Алексей Сергеевич, ИП": ["Татьяна", "Озеро", "Новая палатка"],
        "Чернова Олеся Анатольевна, ИП": ["Заветы", "Агро", "Победа"]
    }
    tochka = re.sub(r'.[a-z][^\w\s]+|[\d]+', r'', file_name).strip().replace(' ', '').replace('.xlsx', '')
    ex = 'Новаяпалатка'
    if tochka == ex:
        tochka = "Новая палатка"
    else:
        pass
    print(f'Название точки из файла: {tochka}')
    for key in j:
        a = key
        values = j.get(a)
        for value in values:
            if value == tochka:
                mylib.find_click("//div[@class='whd-document__organisationSelector-wrapper ws-ellipsis']", driver)
                forxpath44 = f"//div[@class='entityChoice-Stack__column--name ws-flex-shrink-1 ws-ellipsis   ']/span[text()='{a}']"
                mylib.find_click(forxpath44, driver)
                mylib.find_click("//span[@class='controls-Lookup__link__text ']", driver)
                try:
                    mylib.find_click("//span[@class='controls-FilterView__iconReset icon-CloseNew']", driver)
                except:
                    pass
                forxpath666 = f"//div[contains (@class, 'wnc-warehouse-selector__item  wnc-warehouse-selector__itemCaption') and text()='{tochka_clear}']"
                mylib.find_click(forxpath666, driver)
                for patch in paths2:
                    mylib.find_click(patch, driver)
                mylib.find_click("//span[text()='Сохранить']", driver)
                print(f'Загружено:{tochka}')



for file in files:
    load_invent(driver, file, 'Инвентаризации 11 20', '20.11.22')
print('ВСЁ!')
