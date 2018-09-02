import selenium 

magiclink = 'https://api.whatsapp.com/send?phone='
geckodriver = '/home/manthan/Git/python-projects/whatsapp_message_sender/geckodriver'
driver = selenium.webdriver.Firefox(geckodriver)
driver.get(magiclink + '917042255746')
