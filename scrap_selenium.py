import requests
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

url = 'https://www.latamairlines.com/mx/es'

# r = requests.get(url)
# print(r.status_code)
# 
# s = BeautifulSoup(r.text, 'lxml')
# print(s.prettify())

options = Options()
options.add_experimental_option('detach', True)
options.add_argument('start-maximized')
options.add_argument('--incognito')

# download ChromeDriver from https://chromedriver.chromium.org/downloads
driver = webdriver.Chrome(executable_path=r'..\chromedriver.exe')  # for windows

# driver = webdriver.Chrome(chrome_options=options,
#                           service=Service(ChromeDriverManager().install()))  # for linux
driver.get(url)

# driver.close()
