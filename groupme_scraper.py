# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.support import expected_conditions as EC
# from build_message import build_message_string
# import time as t
# from datetime import datetime



# def send_messages(bot_dicts):
#     chrome_options = webdriver.ChromeOptions()
#     # Add your Chrome options here as needed
#     chrome_options.add_argument("--no-sandbox")
#     chrome_options.add_argument("--headless")
#     chrome_options.add_argument("--disable-gpu")
#     chrome_options.add_argument(f"--user-data-dir=/Users/chasereynders/Library/Application Support/Google/Chrome")
#     chrome_options.add_argument('--profile-directory=Profile 8')

#     driver = webdriver.Chrome(options=chrome_options)
#     driver.get('https://web.groupme.com/chats/')
#     for bot_dict in bot_dicts:
#         driver.get(bot_dict['url'])


#         # Wait for the modal to appear
#         modal = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, 'modal-content')))
        
#         # Now find the "View" button within the modal
#         driver.implicitly_wait(5)
#         view_button = modal.find_element(By.XPATH, '//span[contains(text(), "View")]')
        
#         # Click the button once it's clickable
#         view_button.click()

#         # Copy to clipboard and paste into message box
#         msg = build_message_string(bot_dict)
#         # Locate the element by partial ID match
#         message_composer = driver.find_element(By.CSS_SELECTOR, '[id*="message-composer"]')
#         # Inject message into JS
#         message_composer.click()    
#         driver.execute_script("arguments[0].textContent = arguments[1];", message_composer, msg)

#         # Send the message
#         message_composer.send_keys(Keys.RETURN)
#         # Wait until message is shown to be sent
#         t.sleep(0.1)
        
