from selenium import webdriver
import json
import time
import requests
import urllib
import sys
import os

try:
    # This works when the script is imported as a module.
    from ..ai import get_openai_response
except ImportError:
    # This allows the script to be run directly.
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
    from src.ai import get_openai_response

from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
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
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    time.sleep(5)

    mute_toggle = driver.find_element(By.CSS_SELECTOR, ".mui-dhecnw")
    actions = ActionChains(driver)
    actions.click(mute_toggle).perform()
    driver.execute_script("document.querySelector('.mui-dhecnw').click();")

    _close_junk_windows(driver)

    body = driver.find_element(By.TAG_NAME, 'body')
    body.send_keys('f')

def ai_pick_result_id(options):
    system_prompt = """You are an expert search result classifier.
    Your task is to review a user's query and a list of search results.
    Your goal is to identify the single best-matching search result from the list.
    The search results are provided as a JSON list.
    Return the ID of the most relevant search result in a JSON object."""
    prompt = f"""User query: {json.dumps(options)}. Respond only with the ID of the most popular media entity,
    with no punctuation / quotation marks."""
    id = int(get_openai_response(prompt, system_prompt=system_prompt))
    return id


def launch_show_by_name(name: str):
    query = urllib.parse.quote_plus(name)
    api_url = f'https://api.themoviedb.org/3/search/tv?api_key=68e094699525b18a70bab2f86b1fa706&include_adult=false&query={query}'
    response = requests.get(api_url)
    results = response.json()['results']
    show_id = ai_pick_result_id(results)
    _open_page(f'https://vidfast.pro/tv/{show_id}/1/1?autoPlay=true&autoNext=true')

if __name__ == '__main__':
    # launch_show('shark tank')
    launch_show_by_name('gumball')
