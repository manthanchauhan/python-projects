from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from time import sleep

chrome_driver= 'D:\Git\python-projects\\techtronix_whatsapp_messenger\chromedriver.exe'
login=['manthanchauhan913@gmail.com', '*****']
gmail_login_email = '//*[@id="identifierId"]'
gmail_login_password = '//*[@id="password"]/div[1]/div/div[1]/input'
contact_search = '//*[@id="gb"]/div[2]/div[2]/div/form/div/div/div/div/div/div[1]/input[2]'
tab_index = '//*[@id="yDmH0d"]/c-wiz[2]/div[2]/div[1]/div[2]/div/div/div/div[6]/div[3]'
delete_tab = '//*[@id="yDmH0d"]/c-wiz[2]/div[4]/div/div/div[1]/content[4]/content'
delete_final = '//*[@id="yDmH0d"]/div[4]/div/div[2]/div[2]/div[2]/content/span'
login[1]=input('Please enter password for ' + login[0] + ':\n')

driver = webdriver.Chrome(chrome_driver)
driver.get('https://contacts.google.com')
# sleep(2)
# textbox = driver.find_element_by_xpath(gmail_login_email)
textbox = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, gmail_login_email)))
textbox.clear()
textbox.send_keys(login[0] + Keys.ENTER)
#sleep(2)
# textbox = driver.find_element_by_xpath(gmail_login_password)
textbox = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, gmail_login_password)))
textbox.clear()
textbox.send_keys(login[1] + Keys.ENTER)

textbox = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, contact_search)))
textbox.clear()
textbox.send_keys('Abhinav Lal' + Keys.ENTER)
tab = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, tab_index)))
tab.click()
delete= WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, delete_tab)))
delete.click()
delete= WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, delete_tab)))
delete.click()
delete = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, delete_final)))
delete.click()
