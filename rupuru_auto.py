from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.select import Select
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.alert import Alert
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

import time
import requests
import sys
import datetime
import pandas as pd
import random

print("================start===============")

second = 0.5
week_day_dict ={"0":"月", "1":"火", "2":"水", "3":"木", "4":"金", "5":"土", "6":"日"}
url = "https://notify-api.line.me/api/notify"

def rupuru():
    driver.implicitly_wait(60)

    try:
        driver.get("https://www.mychallenge.toyotakenpo.jp/Account/Login?ReturnUrl=%2f")
        driver.set_window_size(1900, 1000)
    except:
        payload = {'message':str(datetime.date.today()) + "==>" + "Error: ChromeDriver" }
        LINE_Error(payload)

    try:    
        driver.find_element(By.ID, "LoginId").click()
        time.sleep(second)
        driver.find_element(By.ID, "LoginId").send_keys(df.at[0,'ID'])
        time.sleep(second)
        driver.find_element(By.ID, "Password").click()
        time.sleep(second)
        driver.find_element(By.ID, "Password").send_keys(df.at[0,'Password'])
        time.sleep(second)
        driver.find_element(By.CSS_SELECTOR, ".btn-primary").click()
    except:
        payload = {'message':str(datetime.date.today()) + "==>" + "Error: Login Phase" }
        LINE_Error(payload)

    try:
        list_date = [1,2,3,4,5,6,7,11,12,13,14,15,16,17,21,22,23,24,25,26,27,31,32,33,34,35,36,37]
        week_num = 0

        for num in list_date:
            if num in [1, 11, 21, 31]:
                path = f'/html/body/form/div/div/div/div/div[4]/div[4]/table/tbody/tr[{num}]/td[2]/span'
                week_num += 1
                count_ex = 1
            else:
                path = f'/html/body/form/div/div/div/div/div[4]/div[4]/table/tbody/tr[{num}]/td[1]/span'
                count_ex += 1

            time.sleep(second)
            if date in str(driver.find_element(By.XPATH, path).text):
                print("date match: " + driver.find_element(By.XPATH, path).text)
                break

    except:
        payload = {'message':str(datetime.date.today()) + "==>" + "Error: date confirmation Phase" }
        LINE_Error(payload)

    try:
        print("List of exercises to register: ")
        for n in range(int(df.at[0,'total_exercise_num'])):
            time.sleep(second)
            n += 1
            dropdown = driver.find_element(By.ID, f"exKey{n}")
            select = Select(dropdown)
            ex_name = df.at[0, f'exercise{n}']
            print(ex_name)
            select.select_by_visible_text(ex_name)
    except:
        payload = {'message':str(datetime.date.today()) + "==>" + "Error: 運動の登録に失敗しました。" }
        LINE_Error(payload)

    try:
        for ex in range(int(df.at[0,'total_exercise_num'])):
            time.sleep(second)
            ex += 1
            elem_id = f"Ex{week_num}_{count_ex}_{ex}"
            driver.find_element(By.ID, elem_id).clear()
            driver.find_element(By.ID, elem_id).send_keys("1")

        d = random.uniform(-0.9, 0.9)
        weight = round(float(df.at[0,'base_weight']) + d, 1)
        print("Weight to register:" + str(weight) + "kg")
        we_id = f"We{week_num}_{count_ex}"
        driver.find_element(By.ID, we_id).clear()
        time.sleep(second)
        driver.find_element(By.ID, we_id).send_keys(str(weight))
    except:
        payload = {'message':str(datetime.date.today()) + "==>" + "Error: METs入力エラー" }
        LINE_Error(payload)

    try:
        if week_num == 4 and count_ex == 7:
            driver.find_element(By.ID, "btnApplicationF").click()
            Alert(driver).accept()
            driver.find_element(By.XPATH, '/html/body/div[2]/div/div/form/div/div/fieldset/div/input[1]').click()
            print("Next Month")
            LINE("Next Month Challenge")
        else:
            driver.find_element(By.ID, "btnSaveH").click()
            time.sleep(second)
            assert driver.switch_to.alert.text == "保存します。よろしいですか？"
            time.sleep(second)
            driver.switch_to.alert.accept()
            time.sleep(10)
    except:
        payload = {'message':str(datetime.date.today()) + "==>" + "Error: Save METs" }
        LINE_Error(payload)

def LINE(status):
    if line_flag == 1:
        payload = {'message': str(datetime.date.today()) + "==>" + status}
        headers = {"Authorization" : "Bearer " + token}
        requests.post(url ,headers=headers ,params=payload)

def LINE_Error(payload):
    if line_flag == 1:
        headers = {"Authorization" : "Bearer " + token}
        requests.post(url ,headers=headers ,params=payload)
    sys.exit()

if __name__ == "__main__":
    df = pd.read_csv("setting_info.csv", encoding='shift_jis')

    line_flag = 1 if df.at[0,'LINE_access_token'] == df.at[0,'LINE_access_token'] else 0
    token = df.at[0,'LINE_access_token'] if line_flag else ""

    required_fields = ['ID', 'Password', 'base_weight', 'total_exercise_num', 'exercise1']
    for field in required_fields:
        if df.at[0, field] != df.at[0, field]:
            LINE_Error({'message': str(datetime.date.today()) + "==>" + f"Error: {field} が空です"})

    ex_num = int(df.at[0, 'total_exercise_num'])
    for i in range(1, ex_num + 1):
        if df.at[0, f'exercise{i}'] != df.at[0, f'exercise{i}']:
            LINE_Error({'message': str(datetime.date.today()) + "==>" + "Error: exercise項目が足りません"})

    # Chrome 起動（ヘッドレス対応可）
    options = webdriver.ChromeOptions()
    if df.at[0,'headless'] == 1:
        options.add_argument('--headless')

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    dt = datetime.datetime.now()
    date = f"{str(dt.month).zfill(2)}月{str(dt.day).zfill(2)}日({week_day_dict[str(dt.weekday())]})"
    print("Date:", date)

    rupuru()
    driver.quit()
    LINE("Normal End")
