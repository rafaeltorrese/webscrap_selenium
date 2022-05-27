# %%
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager


# %%
url = 'https://www.latamairlines.com/mx/es'

# %%
options = Options()
options.add_experimental_option('detach', True)
options.add_argument('start-maximized')
options.add_argument('--incognito')
# %%
# download ChromeDriver from https://chromedriver.chromium.org/downloads
driver = webdriver.Chrome(executable_path=r'..\chromedriver.exe')  # for windows
# %%
# driver = webdriver.Chrome(chrome_options=options,
                        #   service=Service(ChromeDriverManager().install()))  # for linux
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
itinerary_modal = flight.find_element(By.XPATH, './/a[@id="itinerary-modal-0-dialog-open"]')
print(itinerary_modal)
# %%
itinerary_modal.click()
# %%
legs = flight.find_elements(By.XPATH, '//section[@data-test="section-info-leg"]')
print(f'Number of legs: {len(legs)}')
# %%
num_stops = len(legs) - 1
print(f'Number of stops: {num_stops}')
# %% [markdown]
# ## Stops and fares
# %%
leg = legs[0]
# %%

# Departure City Leg
print(leg.find_element(By.XPATH, '//span[@class="pathInfo-origin incoming-outcoming-title"]/following-sibling::div[@class="iataCode"]/span[1]').text)

# Departure Time Leg
print(leg.find_element(By.XPATH, '//span[@class="pathInfo-origin incoming-outcoming-title"]/following-sibling::div[@class="iataCode"]/span[2]').text)

# Duration flight
print(leg.find_element(By.XPATH, './/div[@class="sc-cdQEHs jryrRi"]//span[@class="time"]').text)

# airplane model
print(leg.find_element(By.XPATH, './/div[@class="sc-bNpCPZ fOmMxC"]/span[@class="airplane-code"]').text)

# flight number
print(leg.find_element(By.XPATH, '//div[@class="incoming-outcoming-title"]/div').text)
# %%
# Arrival City Leg
print(leg.find_element(By.XPATH, '//span[@class="pathInfo-destination incoming-outcoming-title"]/following-sibling::div[@class="iataCode"]/span[1]').text)

# Arrival Time Leg
print(leg.find_element(By.XPATH, '//span[@class="pathInfo-destination incoming-outcoming-title"]/following-sibling::div[@class="iataCode"]/span[2]').text.replace('. ', '.'))
# %%
connections = leg.find_elements(By.XPATH, '//section[@data-test="section-info-connection"]')
print(f'Number of connections: {len(connections)}')

# Delay Connections
print(connections[0].find_element(By.XPATH, '//div[@class="sc-kGsDXJ dZJGGL"]/span[@class="time"]').text)
# %% [markdown]
# ## Close Modal
# %%
button_close = leg.find_element(By.XPATH, '//button[@class="MuiButtonBase-root MuiIconButton-root sc-jbKcbu eQFcRm"]')

button_close.click()
# %%
# open fares in a flight
# flight.find_element(By.XPATH, './/div[@role="button"]').click()
flight.click()
# %%
fares = flight.find_elements(By.XPATH, './/li[contains(@id, "WrapperBundleCardbundle-detail")]')
# %%


# fare amount
for fare in fares: print(fare.find_element(By.XPATH, './/span[@class="sc-iipuKH ibJrcp displayAmount"]').text)
# %%
# fare type
for fare in fares: print(fare.find_element(By.XPATH, './/span[@class="sc-eQPCt kXXugL"]').text)
# %%
fares_info = {fare.find_element(By.XPATH, './/span[@class="sc-eQPCt kXXugL"]').text: fare.find_element(By.XPATH, './/span[@class="sc-iipuKH ibJrcp displayAmount"]').text for fare in fares}

print(fares_info)
#%%
# close modal
flight.find_element(By.XPATH, './/button[contains(@class,"MuiButtonBase-root")]').click()
# %%
def get_prices(flight):
    fares = flight.find_elements(By.XPATH, './/li[contains(@id, "WrapperBundleCardbundle-detail")]')
    return {fare.find_element(By.XPATH, './/span[@class="sc-eQPCt kXXugL"]').text: fare.find_element(By.XPATH, './/span[@class="sc-iipuKH ibJrcp displayAmount"]').text for fare in fares}
#%%
def get_info_leg(flight):
    'Function that returns information about a leg flight'
    info_leg = []
    legs = flight.find_elements(By.XPATH, '//section[@data-test="section-info-leg"]')
    for leg in legs:
        # Departure City Leg
        leg.find_element(By.XPATH, '//span[@class="pathInfo-origin incoming-outcoming-title"]/following-sibling::div[@class="iataCode"]/span[1]').text

        # Departure Time Leg
        leg.find_element(By.XPATH, '//span[@class="pathInfo-origin incoming-outcoming-title"]/following-sibling::div[@class="iataCode"]/span[2]').text

        # Duration flight
        leg.find_element(By.XPATH, './/div[@class="sc-cdQEHs jryrRi"]//span[@class="time"]').text

        # airplane model
        leg.find_element(By.XPATH, './/div[@class="sc-bNpCPZ fOmMxC"]/span[@class="airplane-code"]').text

        # flight number
        leg.find_element(By.XPATH, '//div[@class="incoming-outcoming-title"]/div').text
        # %%
        # Arrival City Leg
        print(leg.find_element(By.XPATH, '//span[@class="pathInfo-destination incoming-outcoming-title"]/following-sibling::div[@class="iataCode"]/span[1]').text)

        # Arrival Time Leg
        print(leg.find_element(By.XPATH, '//span[@class="pathInfo-destination incoming-outcoming-title"]/following-sibling::div[@class="iataCode"]/span[2]').text.replace('. ', '.'))

    return info_leg