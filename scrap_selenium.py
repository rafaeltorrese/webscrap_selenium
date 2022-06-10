# %%
import time
#%%
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
flights = driver.find_element(By.XPATH, '//ol[@aria-label="Vuelos disponibles."]').find_elements(By.TAG_NAME, 'li')
print(flights)
# %%
flight = flights[-1]
print(flight)

# %%
departure = flight.find_element(
    By.XPATH, './/div[contains(@class, "flight-information")][1]/span').text

arrival = flight.find_element(
    By.XPATH, './/div[contains(@class, "flight-information")][2]/span').text.split('\n')[0]

days_difference = flight.find_element(By.XPATH, './/span[@class="days-difference"]').text

duration = flight.find_element(
    By.XPATH, './/div[contains(@class, "flight-duration")]/span[2]').text

print(departure)
print(arrival)
print(duration)
print(f'Days difference: {days_difference}')
# %%
itinerary_modal = flight.find_element(By.XPATH, './/a[starts-with(@id, "itinerary-modal")]')
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
leg = legs[1]
# %% [markdown]
# ## Legs Information
# %%
# Departure City Leg
print(leg.find_element(By.XPATH, './/span[@class="pathInfo-origin incoming-outcoming-title"]/following-sibling::div[@class="iataCode"]/span[1]').text)

#%%
# Departure Time Leg
print(leg.find_element(By.XPATH, './/span[@class="pathInfo-origin incoming-outcoming-title"]/following-sibling::div[@class="iataCode"]/span[2]').text)
#%%
# Duration flight
print('Flight Duration')
print(leg.find_element(By.XPATH, './/span[@class="pathInfo-duration"]/following-sibling::span[@class="time"]').text)

#%%
# airplane model
print('Airplane Code:')
print(leg.find_element(By.XPATH, './/span[@class="airplane-code"]').text)
# %%
# flight number
print('Flight Number:')
print(leg.find_element(By.XPATH, './/div[@class="incoming-outcoming-title"]/div').text)
# %%
# Arrival City Leg
print('Arrival City Leg')
print(leg.find_element(By.XPATH, './/span[@class="pathInfo-destination incoming-outcoming-title"]/following-sibling::div[@class="iataCode"]/span[1]').text)
#%%
# Arrival Time Leg
print('Arrival Time for the Leg')
print(leg.find_element(By.XPATH, './/span[@class="pathInfo-destination incoming-outcoming-title"]/following-sibling::div[@class="iataCode"]/span[2]').text.replace('. ', '.'))
# %%
connections = leg.find_elements(By.XPATH, '//section[@data-test="section-info-connection"]')
print(f'Number of connections: {len(connections)}')
#%%
# Delay Connections
print('Delay of the connection:')
print(connections[0].find_element(By.XPATH, './/section//span[@class="time"]').text)
# %% [markdown]
# ## Close Modal
# %%
button_close = driver.find_element(By.XPATH, '//button[contains(@id, "itinerary-modal")]')

button_close.click()
# %%
# open fares in a flight
# flight.find_element(By.XPATH, './/div[@role="button"]').click()
flight.click()
# %%
fares = flight.find_elements(By.XPATH, './/li[contains(@id, "WrapperBundleCardbundle-detail")]')
# %%

# fare amount
fare_amounts = [fare.find_element(By.XPATH, './/span[contains(@class, "displayAmount")]').text for fare in fares]
print(fare_amounts)
# %%
# fare type
print('Fare Types:')
fare_types = [fare.find_element(By.XPATH, './div/div/div/div/span[@title]').text for fare in fares[:-1]]
if len(fares) > 3:
    premium_fare = fares[-1].find_element(By.XPATH, './div/div/div/div/span/span[3]').text
    fare_types += [premium_fare]
print(fare_types)
# %%
print('Fares Info:')

fares_info = dict(zip(fare_types, fare_amounts))
print(fares_info)

#%%
# close modal
flight.find_element(By.XPATH, './/button[contains(@class,"MuiButtonBase-root")]').click()
# %%
def get_prices(flight):    
    fares = flight.find_elements(By.XPATH, './/li[contains(@id, "WrapperBundleCardbundle-detail")]')
    fare_types = [fare.find_element(By.XPATH, './div/div/div/div/span[@title]').text for fare in fares[:-1]]
    if len(fares) > 3:
        premium_fare = fares[-1].find_element(By.XPATH, './div/div/div/div/span/span[3]').text
        fare_types += [premium_fare]

    fare_amounts = [fare.find_element(By.XPATH, './/span[contains(@class, "displayAmount")]').text for fare in fares]
    return dict(zip(fare_types, fare_amounts))
#%%
def get_info_legs(flight):
    'Function that returns information about a leg flight'

    info_legs = []    

    legs = flight.find_elements(By.XPATH, '//section[@data-test="section-info-leg"]')
    
    for leg in legs:
        try:            
            connection_length = leg.find_element(By.XPATH, './/following-sibling::section[@data-test="section-info-connection"]//span[@class="time"]').text
            connection_place = leg.find_element(By.XPATH, './/following-sibling::section[@data-test="section-info-connection"]//span[@class="connection-text"]').text            
        except:
            connection_length = ''
            connection_place = ''

        info = {
            # Source Leg
            'source': leg.find_element(By.XPATH, './/span[@class="pathInfo-origin incoming-outcoming-title"]/following-sibling::div[@class="iataCode"]/span[1]').text,
            # Source Time Leg
            'departure': leg.find_element(By.XPATH, './/span[@class="pathInfo-origin incoming-outcoming-title"]/following-sibling::div[@class="iataCode"]/span[2]').text,
            # Duration flight
            'duration': leg.find_element(By.XPATH, './/span[@class="pathInfo-duration"]/following-sibling::span[@class="time"]').text,
            # Sink Leg
            'sink': leg.find_element(By.XPATH, './/span[@class="pathInfo-destination incoming-outcoming-title"]/following-sibling::div[@class="iataCode"]/span[1]').text,
            # Sink Time Leg        
            'arrival': leg.find_element(By.XPATH, './/span[@class="pathInfo-destination incoming-outcoming-title"]/following-sibling::div[@class="iataCode"]/span[2]').text.replace('. ', '.'),
            # airplane model
            'airplane': leg.find_element(By.XPATH, './/span[@class="airplane-code"]').text,        
            #  flight number
            'fligth': leg.find_element(By.XPATH, './/div[@class="incoming-outcoming-title"]/div').text,

            # connection length            
            'connection': connection_length,
            # connection place
            'connection_place': connection_place,
        }
  

        info_legs.append(info)              

    # button_close = flight.find_element(By.XPATH, '//button[@id="itinerary-modal-0-dialog-close"]')    
    # button_close.click()

    return info_legs
# %%
print(flight)

# %%
infolegs = get_info_legs(flight)
print(infolegs)
# %%
def get_info_flight(flight):
    return {
        'departure': flight.find_element( By.XPATH, './/div[contains(@class, "flight-information")][1]/span').text,
        'arrival': flight.find_element(By.XPATH, './/div[contains(@class, "flight-information")][2]/span').text.split('\n')[0],
        'days': flight.find_element(By.XPATH, './/div[contains(@class, "flight-information")][2]/span/span').text,
        'duration': flight.find_element(By.XPATH, './/div[contains(@class, "flight-duration")]/span[2]').text,    
    }
    
# %%
    
print(get_info_flight(flight))

# %%
def get_info(driver):
    flights = driver.find_element(By.XPATH, '//ol[@aria-label="Vuelos disponibles."]').find_elements(By.TAG_NAME, 'li')
    print(f'Number of flights: {len(flights)}\nStart scraping')
    
    information = []
    
    for i,flight in enumerate(flights, 1):
        print(f'Flight Number: {i}')
        time.sleep(1)
        info_flight = get_info_flight(flight)
        
        # open itenerary button
        flight.find_element(By.XPATH, './/a[starts-with(@id, "itinerary-modal")]').click()
        
        time.sleep(1)
        info_stops = get_info_legs(flight)
        
        time.sleep(0.5)
        # close button
        flight.find_element(By.XPATH, '//button[contains(@id, "itinerary-modal")]').click()

        # driver.find_element(By.XPATH, '//button[@id="itinerary-modal-0-dialog-close"]').click()
        
        # open fares, click on the flight
        flight.click()

        prices = get_prices(flight)

        # close modal
        driver.find_element(By.XPATH, './/button[contains(@class,"MuiButtonBase-root")]').click()

        information.append(
            {'prices': prices, 
            'flight': info_flight, 
            'stops':info_stops}
            )
    return information

# %%
url = 'https://www.latamairlines.com/mx/es'
options = Options()
options.add_experimental_option('detach', True)
options.add_argument('start-maximized')
options.add_argument('--incognito')

# download ChromeDriver from https://chromedriver.chromium.org/downloads
driver = webdriver.Chrome(executable_path=r'..\chromedriver.exe')  # for windows

# driver = webdriver.Chrome(chrome_options=options,
                        #   service=Service(ChromeDriverManager().install()))  # for linux
#%%
driver.get(url)
#%%
get_info(driver)
#%%
driver.close()
# %%
