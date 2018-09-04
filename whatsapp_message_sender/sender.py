from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
 
# Replace below path with the absolute path
# to chromedriver in your computer
chrome = 'D:\Git\python-projects\whatsapp_message_sender\chromedriver.exe'
driver = webdriver.Chrome(chrome)
 
driver.get("https://web.whatsapp.com/")
wait = WebDriverWait(driver, 600)
 
# Replace 'Friend's Name' with the name of your friend 
# or the name of a group 
target = '"Madhav"'
print('here')
 
# Replace the below string with your own message
string = "Message sent using Python!!!"
 
x_arg = '//span[contains(@title,' + target + ')]'
group_title = wait.until(EC.presence_of_element_located((
    By.XPATH, x_arg)))
print(target + ' located')
group_title.click()
time.sleep(5)
print('searching for text box')
inp_xpath = '_2S1VP copyable-text selectable-text'
input_box = wait.until(EC.presence_of_element_located((
    By.CLASS_NAME, inp_xpath)))
print('box located')

input_box.send_keys(string + Keys.ENTER)
time.sleep(1)
