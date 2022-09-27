from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service

options = Options()
#  Will launch browser without UI(headless)
options.headless = True
# options.add_argument("--no-sandbox")
# FIREFOX_PATH = 'd:\\Python\\geckodriver-v0-31-0-win64\\geckodriver.exe'
FIREFOX_PATH = '../../../../usr/bin/geckodriver'
service = Service(FIREFOX_PATH)
driver = webdriver.Firefox(service=service, options=options)

driver.get("https://google.com/")
print(driver.title)
driver.quit()
