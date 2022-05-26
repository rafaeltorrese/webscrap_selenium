# %%
import requests
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager


# %%
url = 'https://www.latamairlines.com/mx/es'

# r = requests.get(url)
# print(r.status_code)
#
# s = BeautifulSoup(r.text, 'lxml')
# print(s.prettify())
# %%
options = Options()
options.add_experimental_option('detach', True)
options.add_argument('start-maximized')
options.add_argument('--incognito')
# %%
# download ChromeDriver from https://chromedriver.chromium.org/downloads
# driver = webdriver.Chrome(executable_path=r'..\chromedriver.exe')  # for windows
# %%
driver = webdriver.Chrome(chrome_options=options,
                          service=Service(ChromeDriverManager().install()))  # for linux
driver.get(url)

# %%
flights = driver.find_elements(By.XPATH, '//li[@class="sc-dCVVYJ CEVgB"]')
print(flights)
# %%
flight = flights[0]
print(flight)

# %%
departure = flight.find_element(
    By.XPATH, './/div[@class="sc-kBMPsl hKrdMC flight-information"][1]/span').text
arrival = flight.find_element(
    By.XPATH, './/div[@class="sc-kBMPsl hKrdMC flight-information"][2]/span').text

duration = flight.find_element(
    By.XPATH, './/div[@class="sc-kBMPsl hKrdMC flight-duration"]/span[2]').text

print(departure)
print(arrival)
print(duration)
# %%
