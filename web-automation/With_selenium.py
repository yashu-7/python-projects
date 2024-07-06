from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import pyautogui as pg
from time import sleep
from bs4 import BeautifulSoup

from_place = 'bangalore'
to_place = 'hyderabad'
driver = webdriver.Chrome(ChromeDriverManager().install())
url = 'https://www.makemytrip.com/bus-tickets/'
driver.get(url)
driver.maximize_window()

from_tab = driver.find_element(By.XPATH, '//*[@id="fromCity"]')
from_tab.click()

sleep(2)
xin, yin = 191, 876
xout, yout = 900, 986

pg.click(x=xin, y=yin)
sleep(2)
pg.click(x=xout, y=yout)

date = driver.find_element(By.XPATH, '//*[@id="top-banner"]/div[2]/div/div/div[2]/div/div[3]/div[1]/div/div/div/div[2]/div/div[2]/div[1]/div[3]/div[2]/div[4]')
date.click()

search_button = driver.find_element(By.ID, 'search_button')
search_button.click()

sleep(5)  # wait for the results to load

page_source = driver.page_source
driver.quit()

soup = BeautifulSoup(page_source, 'html.parser')
buses = soup.find_all('div', class_='busCard false')

# Open the file in write mode
with open('bus_details.txt', 'w') as file:
    for bus in buses:
        name_element = bus.find('p', class_='latoBold')
        departure_time_element = bus.find('span', class_='font18 latoBlack blackText')
        arrival_time_elements = bus.find_all('span', class_='font18 blackText appendRight4 latoRegular')
        price_element = bus.find('span', id='price')

        name = name_element.text if name_element else 'N/A'
        departure_time = departure_time_element.text if departure_time_element else 'N/A'
        arrival_time = arrival_time_elements[-1].text if arrival_time_elements else 'N/A'
        price = price_element.text.strip() if price_element else 'N/A'

        # Write the details to the file
        file.write(f"Bus Name: {name}\n")
        file.write(f"Departure Time: {departure_time}\n")
        file.write(f"Arrival Time: {arrival_time}\n")
        file.write(f"Price: {price}\n")
        file.write("-" * 40 + "\n")

print("Bus details have been saved to bus_details.txt")