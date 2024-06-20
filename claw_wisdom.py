# -*- coding: utf-8 -*-
"""
Created on Mon Nov 14 01:14:54 2022

@author: user

要先安裝套件

pip install pandas
pip install selenium
pip install webdriver-manager
pip install 

"""
import pandas as pd
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time
import random

options = webdriver.ChromeOptions()
#不自動關閉瀏覽器
options.add_experimental_option('detach', True)
#無痕模式
options.add_argument('--incognito')
#解決DevToolsActivePort檔案不存在的報錯
options.add_argument("--no-sandbox")
#瀏覽器不提供可視化頁面
options.add_argument('--headless')
#停用GPU
options.add_argument('--disable-gpu')
#停用WebGL
options.add_argument('--disable-software-rasterizer')
#停用dev-shm-usage
options.add_argument('-enable-webgl --no-sandbox --disable-dev-shm-usage')
#關閉INFO:CONSOLE提示
options.add_argument('log-level=3')
#不載入圖片，提升運行速度
options.add_argument('blink-settings=imagesEnabled=false')
#停用外掛
options.add_argument('--disable-plugins')
options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.add_experimental_option("excludeSwitches", ['enable-automation'])
# prefs = {'profile.default_content_setting_values' :{'notifications' : 2}}
# option.add_experimental_option('prefs', prefs)

#自動更新
driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options = options)
# driver = webdriver.Chrome("C:\Users\user\.wdm\drivers\chromedriver\win32\107.0.5304\chromedriver.exe", chrome_options = option)

#爬蟲取得網址
driver.get('https://act.twse.com.tw/wisdom/account/index')
time.sleep(3)

#下面填入你們隊的帳號和密碼

#登入
def login():
    element_account = driver.find_element(By.ID, 'account')
    element_password = driver.find_element(By.ID, 'password')
    element_account.send_keys('你們隊的帳號')
    element_password.send_keys('你們隊的密碼')
    driver.find_element(By.NAME, 'send').click()
    alert = driver.switch_to.alert
    alert.accept()

login()
time.sleep(1)

#如果是第一次使用，要建立一個空白題庫all.csv
'''
blank = pd.DataFrame()
blank.to_csv('all.csv')
'''

#用all題庫為基底，抓第n大題m次

def crawl_all(n, m):
    for times in range(m):
        i = 0
        j = 0
        k = 0
        l = 0
        repeat = 0
        adding = 0
        before_all_len = 0
        after_all_len = 0
        data_len = 0
        data_all = pd.read_csv('all.csv', index_col=0, header=0)
        driver.get('https://act.twse.com.tw/wisdom/exam/videoList')
        x = random.randint(2, 3)
        time.sleep(x)
        window_before = driver.window_handles[0]
        video_path = '/html/body/section/div[2]/table/tbody/tr[' + str(n) + ']/td[2]/a'
        driver.find_element(By.XPATH, video_path).click()
        time.sleep(1)
        window_after = driver.window_handles[1]
        driver.switch_to.window(window_after)
        driver.close()
        driver.switch_to.window(window_before)
        x = random.randint(3, 4)
        time.sleep(x)
        driver.find_element(By.XPATH, "//button[@type='submit']").click()
        html_text = driver.page_source
        df = pd.read_html(html_text, encoding='utf-8')
        data = pd.DataFrame(df[0])
        data.drop(0, axis=1, inplace=True)
        data.drop([0, 1], inplace=True)
        data = data.reset_index(drop=True)
        data['2'] = ''
        data['3'] = ''
        data['4'] = ''
        data['5'] = ''
        data.columns = ['0', '1', '2', '3', '4', '5']
        for i in range(len(data)):
            string = data.iloc[i, 1]
            data.iloc[i, 0] = string[-1]
            string = string[:-8]
            string = string.replace('(1)(2)(3)', '1 2 3')
            string = string.replace('(1)', '!!')
            string = string.replace('(2)', '!!')
            string = string.replace('(3)', '!!')
            string = string.replace('(4)', '!!')
            arr = string.split('!!')
            while '!!' in arr:
                arr.remove('!!')
            while '' in arr:
                arr.remove('')
            for j in range(len(arr)):
                arr[j].strip()
            for k in range(len(arr)):
                data.iloc[i, k+1] = arr[k]
            if data.iloc[i, 0] == '1':
                data.iloc[i, 0] = data.iloc[i, 2]
            elif data.iloc[i, 0] == '2':
                data.iloc[i, 0] = data.iloc[i, 3]
            elif data.iloc[i, 0] == '3':
                data.iloc[i, 0] = data.iloc[i, 4]
            elif data.iloc[i, 0] == '4':
                data.iloc[i, 0] = data.iloc[i, 5]
        data = data.reset_index(drop=True)
        data_len = len(data)
        before_all_len = len(data_all)
        data_all = pd.concat([data_all, data], axis=0, ignore_index=True)
        repeat = data_all[data_all.duplicated(subset=['0', '1'])]['1'].value_counts().sum()
        data_all.drop_duplicates(subset=['0', '1'], keep='first', inplace=True)
        data_all = data_all.reset_index(drop=True)
        data_all.to_csv('all.csv', encoding='utf_8_sig')
        after_all_len = len(data_all)
        adding = after_all_len - before_all_len
        print('第', n, '大題', '第', times+1, '次', data_len, 'repeat =', repeat, 'add =', adding)
        x = random.randint(6, 7)
        time.sleep(x)

#抓o次全大題，重複p次，每完成一輪印出分隔線
for p in range(30):
    for o in range(1, 11):
        y = random.randint(3, 6)
        crawl_all(o, 2)
        print('---------------第', o, '大題---------------')
    print('--------------------------------------')
    print('--------------------------------------')
    print('--------------------------------------')

#檢查各大題題庫重複情形
'''
d2 = pd.read_csv('all_2.csv', index_col=0, header=0)
d3 = pd.read_csv('all_3.csv', index_col=0, header=0)

length = 63
if len(d2) > len(d3):
    length = len(d2)
else:
    length = len(d3)

repeat = 0
for i in range(len(d2)):
    for j in range(len(d3)):
        if (d2.iloc[i, 1] == d3.iloc[j, 1]) & (d2.iloc[i, 0] == d3.iloc[j, 0]):
            repeat = repeat + 1
print('數字', repeat)
'''

#刪除重複的題目
'''
df = pd.read_csv('all.csv', index_col=0, header=0)
df.drop_duplicates(subset=['0', '1'], keep='first', inplace=True)
df = df.reset_index(drop=True)
df.to_csv('all.csv', encoding='utf_8_sig')
'''

#關閉爬蟲
driver.quit()




