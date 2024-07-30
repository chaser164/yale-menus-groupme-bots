from django.core.management.base import BaseCommand
from prefs.models import Pref
import re
import time as t
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
from datetime import datetime
import json
import requests

LOAD_TIME = 0.15

menus = {
    ' BK':1,
    ' BR & SB':2,
    ' DP':3,
    ' ES & MO':4,
    ' BF & PM':5,
    ' GH':6,
    ' JE':7,
    ' PS':8,
    ' SM':9,
    ' TD':10,
    ' TB':11,
}

colleges = ['BK', 'BR', 'SB', 'DP', 'ES', 'MO', 'BF', 'PM', 'GH', 'JE', 'PS', 'SM', 'TD', 'TB']

class Command(BaseCommand):
    help = 'run scraper and send all groupme messages'

    def scrape(self):
        print("initiating update...")
        firefox_options = webdriver.FirefoxOptions()
        firefox_options.add_argument("--headless")
        driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()), options=firefox_options)
        print("gecko driver installed!")


        prefs = Pref.objects.all().values()

        # Set empty mealtime fields
        for pref in prefs:
            pref['breakfast'] = ''
            pref['brunch_lunch'] = ''
            pref['dinner'] = ''

        for menu in menus:
            driver.get(f'https://usa.jamix.cloud/menu/app?anro=97939&k={menus[menu]}')
            # Attempt to access menu and configure buttons
            try:
                # Find and click the agreement-to-terms button
                driver.implicitly_wait(10)
                view_button = driver.find_element(By.CSS_SELECTOR, '[class="v-button v-widget multiline v-button-multiline selection v-button-selection icon-align-right v-button-icon-align-right v-has-width"]')
                view_button.click()
                # Allow time for the menu loading animation
                driver.implicitly_wait(10)
                meals = driver.find_elements(By.CLASS_NAME, "v-tabsheet-tabitemcell")
                # Create scrollers if need be
                prev_scroller = None
                next_scroller = None
                try:
                    driver.implicitly_wait(5)
                    prev_scroller = driver.find_element(By.CLASS_NAME, 'v-tabsheet-scrollerPrev')
                    next_scroller = driver.find_element(By.CLASS_NAME, 'v-tabsheet-scrollerNext-disabled')
                except:
                    pass
            except:
                print(f'timeout while entering{menu} menu')
                driver.quit()
                return
            page_source_dict_lst = [{'id': '<title>Breakfast', 'visited' : False, 'src': ''},
                                    {'id': '<title>Brunch and Lunch', 'visited' : False, 'src': ''},
                                    {'id': '<title>Dinner', 'visited' : False, 'src': ''}]
            for meal in meals:
                # Scroll until found; click
                clicked = False
                scroll_count = 0
                while(not clicked):
                    try:
                        meal.click()
                        clicked = True
                    except:
                        if(prev_scroller == None or next_scroller == None):
                            print('ERROR: no scrollers found, yet item not visible')
                            return
                        prev_scroller.click()
                        scroll_count += 1
                # reset scroll
                for _ in range(scroll_count):
                    next_scroller.click()
                total = 0
                while True:
                    # Sleep a bit
                    t.sleep(LOAD_TIME)
                    # Populate dict with page src
                    found = False
                    for item in page_source_dict_lst:
                        if item['id'] in driver.page_source and not item['visited']:
                            item['src'] = driver.page_source
                            item['visited'] = True
                            found = True
                            break
                    total += LOAD_TIME
                    # Continue after timeout or menu populated
                    if total > 7 or found:
                        break

            # Add all prefs
            for pref in prefs:
                # Add breakfast data
                if re.search(rf'>[^<]*{pref['pref_string']}[^>]*<', page_source_dict_lst[0]['src'], re.IGNORECASE):
                    pref['breakfast'] += menu
                # Add brunch/lunch data
                if re.search(rf'>[^<]*{pref['pref_string']}[^>]*<', page_source_dict_lst[1]['src'], re.IGNORECASE):
                    pref['brunch_lunch'] += menu
                # Add dinner data
                if re.search(rf'>[^<]*{pref['pref_string']}[^>]*<', page_source_dict_lst[2]['src'], re.IGNORECASE):
                    pref['dinner'] += menu
            print(f'{menu[1:]} data added...')

        driver.quit()
        print('fields update complete!')
        return prefs


    def build_message_string(self, pref):
        header = f'-------------------------------\n{datetime.now().month}/{datetime.now().day} results for "{pref['pref_string']}"\n\n'
        footer = '\n-------------------------------'

        results_if_matches = ''

        any_hits = False

        # BREAKFAST
        count = 0
        included_colleges = ''
        # Accumulate colleges
        for col in colleges:
            if col in pref['breakfast']:
                count += 1
                included_colleges += col + ', '
        # Append
        if count > 0:
            any_hits = True
            results_if_matches += 'breakfast:\n'
            if count == 14:
                results_if_matches += 'all colleges\n\n'
            else:
                results_if_matches += included_colleges[:-2] + '\n\n'

        # BRUNCH / LUNCH
        count = 0
        included_colleges = ''
        # Accumulate colleges
        for col in colleges:
            if col in pref['brunch_lunch']:
                count += 1
                included_colleges += col + ', '
        # Append
        if count > 0:
            any_hits = True
            results_if_matches += 'brunch / lunch:\n'
            if count == 14:
                results_if_matches += 'all colleges\n\n'
            else:
                results_if_matches += included_colleges[:-2] + '\n\n'

        # DINNER
        count = 0
        included_colleges = ''
        # Accumulate colleges
        for col in colleges:
            if col in pref['dinner']:
                count += 1
                included_colleges += col + ', '
        # Append
        if count > 0:
            any_hits = True
            results_if_matches += 'dinner:\n'
            if count == 14:
                results_if_matches += 'all colleges'
            else:
                results_if_matches += included_colleges[:-2]

        if any_hits:
            return header + results_if_matches + footer
        else:
            return 'NO_HITS'
        

    def post_to_groupme(self, bot_dict):
        # Endpoint URL
        url = "https://api.groupme.com/v3/bots/post"

        message = self.build_message_string(bot_dict)
        # Don't send if there are no hits
        if message == 'NO_HITS':
            print(f"no hits for {bot_dict['pref_string']}")
            return
        
        # Data payload
        data = {
            "text": message,
            "bot_id": bot_dict['bot_id']
        }
        
        # Convert data to JSON format
        json_data = json.dumps(data)
        
        try:
            # Send POST request
            response = requests.post(url, data=json_data)
            
            # Check if request was successful (status code 200)
            if response.status_code == 202:
                print(f"{bot_dict['pref_string']} bot delivered the message!")
            else:
                print(f"Failed to post message. Status code: {response.status_code}")
        
        except requests.exceptions.RequestException as e:
            print(f"Error posting message: {e}")


    def handle(self, *args, **options):
        bot_dicts = self.scrape()
        # Send groupme messages
        for bot_dict in bot_dicts:
            self.post_to_groupme(bot_dict)


        