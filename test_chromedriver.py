from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

options = Options()
options.headless = True
options.add_argument("--no-sandbox")
CHROME_PATH = '../../../../usr/bin/chromedriver'
service = Service(CHROME_PATH)
driver = webdriver.Chrome(service=service, options=options)


driver.get("https://google.com/")
print(driver.title)
driver.quit()