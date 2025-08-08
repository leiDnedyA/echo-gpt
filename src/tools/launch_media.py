from requests.api import options
from selenium import webdriver
import time
import os
import requests
import urllib

from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
chrome_options.add_argument("--disable-blink-features=AutomationControlled")

def _close_junk_windows(driver):
    try:
        # https://stackoverflow.com/questions/65987801/closing-popup-windows-in-selenium-using-python
        parent = driver.current_window_handle
        uselessWindows = driver.window_handles
        for winId in uselessWindows:
            if winId != parent: 
                driver.switch_to.window(winId)
                driver.close()
        driver.switch_to.window(parent)
    except:
            pass


def _open_page(url: str):
    service = Service(executable_path='/usr/bin/google-chrome')
    driver = webdriver.Chrome(options=chrome_options)
    try:
        driver.get(url)
        time.sleep(5)

        mute_toggle = driver.find_element(By.CSS_SELECTOR, ".mui-dhecnw")
        actions = ActionChains(driver)
        actions.click(mute_toggle).perform()
        driver.execute_script("document.querySelector('.mui-dhecnw').click();")

        _close_junk_windows(driver)

        body = driver.find_element(By.TAG_NAME, 'body')
        body.send_keys('f')
    finally:
        # driver.quit()
        pass

def launch_show(name: str):
    query = urllib.parse.quote_plus(name)
    api_url = f'https://api.themoviedb.org/3/search/tv?api_key=68e094699525b18a70bab2f86b1fa706&include_adult=false&query={query}'
    response = requests.get(api_url)
    show_id = str(response.json()['results'][1]['id'])
    _open_page(f'https://vidfast.pro/tv/{show_id}/1/1?autoPlay=true&autoNext=true')
    # _open_page('https://bingeflix.tv/tv/' + show_id)

if __name__ == '__main__':
    launch_show('shark tank')
