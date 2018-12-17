import time
from string import Template
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import urllib
import pandas

def read_message():
    msgfile = open(msg_address, 'r')
    msg = msgfile.read()
    return Template(msg)
def login():
    driver = webdriver.Chrome(chrome_driver)
    driver.get("http://web.whatsapp.com/")
    searchBox = WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH,searchbox)))
    return driver
def sendmsg(name):
    searchBox = driver.find_element_by_xpath(searchbox)
    searchBox.clear()
    searchBox.send_keys(name)
    searchBox.send_keys(Keys.ENTER)
    time.sleep(2)
    try:
        messageBox = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, messagebox)))
        msg = message.substitute(name= name)
        msg = msg.split('\n')
        for text in msg:
            messageBox.send_keys(text)
            messageBox.send_keys(Keys.SHIFT + Keys.ENTER)
        messageBox.send_keys(Keys.ENTER)
    except:
        print('message was not sent to: ' + name)

if __name__== '__main__':
    names_address = 'C:\\Users\\manth\\OneDrive\\Techtronix\\Recruitment.csv'
    msg_address = 'D:\Git\python-projects\whatsapp_message_sender\message.txt'
    chrome_driver = 'D:\Git\python-projects\whatsapp_message_sender\chromedriver.exe'
    searchbox = '//input[@class="jN-F5 copyable-text selectable-text"]'
    messagebox = '//div[@class="_2S1VP copyable-text selectable-text"]'
   
    # df = pandas.read_csv(names_address)
    # names = list(df['Name'])
    names = [
        'Harshita',
        'Harshita 2'
    ]
    driver = login()
    message = read_message()
    for name in names:
        sendmsg(name)
    driver.quit()
