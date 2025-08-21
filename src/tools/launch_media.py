from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

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

    actions = ActionChains(driver)
    actions.move_by_offset(2, 2).click().perform()
    actions.move_by_offset(-2, -2).perform()

    _close_junk_windows(driver)

    driver.execute_script("""
    (function() {
        function playVideo(video) {
            if (video && video.paused) {
                video.play().catch(err => {
                    console.log("Autoplay failed:", err);
                });
            }
        }

        // Play all current videos
        document.querySelectorAll('video').forEach(v => playVideo(v));

        // Watch for new videos
        const observer = new MutationObserver(mutations => {
            for (const mutation of mutations) {
                mutation.addedNodes.forEach(node => {
                    if (node.tagName === 'VIDEO') {
                        playVideo(node);
                    }
                    // If a container has videos inside
                    if (node.querySelectorAll) {
                        node.querySelectorAll('video').forEach(v => playVideo(v));
                    }
                });
            }
        });

        observer.observe(document.body, { childList: true, subtree: true });
    })();
    """)

def ai_pick_result_id(options):
    system_prompt = """You are an expert search result classifier.
    Your task is to review a user's query and a list of search results.
    Your goal is to identify the single best-matching search result from the list.
    The search results are provided as a JSON list.
    Return the ID of the most relevant search result in a JSON object."""
    prompt = f"""User query: {json.dumps(options)}. Respond only with the ID of the most popular media entity,
    with no punctuation / quotation marks. Do not respond with a JSON format, the response must be parseable by the python `int()` function."""
    id = int(get_openai_response(prompt, system_prompt=system_prompt))
    return id

def launch_show_by_name(name: str, season_number=None, episode_number=None):
    query = urllib.parse.quote_plus(name)
    api_url = f'https://api.themoviedb.org/3/search/tv?api_key=68e094699525b18a70bab2f86b1fa706&include_adult=false&query={query}'
    response = requests.get(api_url)
    results = response.json()['results']
    show_id = ai_pick_result_id(results)
    url = f'https://flixer.su/watch/tv/{show_id}'
    if season_number is not None and not episode_number is not None:
        url += f'/{season_number}/1'
    elif episode_number is not None and season_number is None:
        url += f'/1/{episode_number}'
    elif season_number is not None and episode_number is not None:
        url += f'/{season_number}/{episode_number}'
    else:
        url += '/1/1'
    url += '?autoPlay=true&autoNext=true'
    try:
        _open_page(url)
        return True
    except Exception as e:
        print(e)
        return False

tools = [{
    "type": "function",
    "name": "launch_show_by_name",
    "description": "Launch a show based on the given name, and optionally season + episode number.",
    "parameters": {
        "type": "object",
        "properties": {
            "name": {
                "type": "string",
                "description": "The name of the show to be launched, such as 'Adventure Time', or 'Shark Tank'.",
            },
            "season_number": {
                "type": "integer",
                "description": "The season number of the episode to be launched. If not specified, season one will be opened.",
            },
            "episode_number": {
                "type": "integer",
                "description": "The number of the episode to be launched. If not specified, episode one will be opened.",
            },
        },
        "required": ["name"],
    },
}]

tool_functions = {
    "launch_show_by_name": launch_show_by_name
}

if __name__ == '__main__':
    # launch_show('shark tank')
    launch_show_by_name('gumball', 2, 2)
