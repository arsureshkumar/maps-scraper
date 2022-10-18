from re import T
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.edge.options import Options
from time import sleep
import pandas as pd

place_info = pd.DataFrame(columns=['Firm Name', 'Address', 'Total Reviews', 'Total Rating'])

def grab_text(xpath):
    try:
        wait = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, xpath)))
        return(driver.find_element(By.XPATH, xpath).text)
    except:
        return("")

def get_place_info(links):
    info = pd.DataFrame(columns=['Firm Name', 'Address', 'Total Reviews', 'Total Rating'])
    for i in links:
        driver.get(i)
        current_url = driver.current_url
        xpaths = {
            "Firm Name": '''//*[@id="pane"]/div/div[1]/div/div/div[2]/div[1]/div[1]/div[1]/h1''',
            "Total Rating": '''//*[@id="pane"]/div/div[1]/div/div/div[2]/div[1]/div[1]/div[2]/div/div[1]/div[2]/span/span/span''',
            "Total Reviews": '''//*[@id="pane"]/div/div[1]/div/div/div[2]/div[1]/div[1]/div[2]/div/div[1]/span[1]/span/span[1]/span[2]/span[1]/button''',
            "Address": '''//*[@id="pane"]/div/div[1]/div/div/div[11]/div[1]/button/div[1]/div[2]/div[1]'''
        }
        info = info.append({k:grab_text(v) for (k,v) in xpaths.items()}, ignore_index=True)
    return(info)
    

edgeOptions = Options()
edgeOptions.headless = False

driver = webdriver.Edge(executable_path = ".\msedgedriver.exe", options = edgeOptions)
driver.get("https://maps.google.com/")

driver.switch_to.active_element.send_keys("McDonalds" + Keys.ENTER)


#switch to explicit waits
wait = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, '''//*[@id="pane"]/div/div[1]/div/div/div[2]/div[1]''')))
sleep(1)
driver.switch_to.active_element.send_keys(Keys.TAB + Keys.TAB + Keys.ARROW_DOWN * 100)
sleep(1)
driver.switch_to.active_element.send_keys(Keys.ARROW_DOWN * 100)
sleep(1)
driver.switch_to.active_element.send_keys(Keys.ARROW_DOWN * 100)

pane_element = driver.find_element(By.XPATH, '''//*[@id="pane"]/div/div[1]/div/div/div[2]/div[1]''')
place_links = [i.get_attribute("href") for i in pane_element.find_elements(By.TAG_NAME, "a")]

place_info = pd.concat([place_info, get_place_info(place_links)])
place_info['Total Reviews'] = place_info['Total Reviews'].map(lambda x: x[:-8])

place_info.to_csv('place_info.csv')

sleep(5)

driver.quit()