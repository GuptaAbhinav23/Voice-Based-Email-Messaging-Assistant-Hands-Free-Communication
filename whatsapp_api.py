
import os
import time
import pickle
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

SESSION_FILE = 'whatsapp_session.pkl'

class WhatsAppAPI:
    def __init__(self):
        self.driver = None

    def start_whatsapp(self, show_qr=True):
        chrome_options = Options()
        chrome_options.add_argument('--user-data-dir=./chrome_data')
        chrome_options.add_argument('--profile-directory=Default')
        chrome_options.add_argument('--disable-notifications')
        chrome_options.add_argument('--window-size=900,900')
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.get('https://web.whatsapp.com/')
        # Load session if exists
        if os.path.exists(SESSION_FILE):
            with open(SESSION_FILE, 'rb') as f:
                cookies = pickle.load(f)
            for cookie in cookies:
                self.driver.add_cookie(cookie)
            self.driver.refresh()
            time.sleep(5)
        # Wait for QR or main page
        if show_qr:
            self.wait_for_login()
            # Save session after login
            with open(SESSION_FILE, 'wb') as f:
                pickle.dump(self.driver.get_cookies(), f)

    def wait_for_login(self, timeout=60):
        for _ in range(timeout):
            try:
                self.driver.find_element(By.CSS_SELECTOR, 'canvas[aria-label="Scan me!"]')
                time.sleep(1)
            except NoSuchElementException:
                # QR gone, probably logged in
                return True
        return False

    def get_recent_chats(self):
        chats = []
        chat_elements = self.driver.find_elements(By.CSS_SELECTOR, 'div[role="row"]')
        for chat in chat_elements[:20]:
            try:
                name = chat.find_element(By.CSS_SELECTOR, 'span[title]').get_attribute('title')
                last_msg = chat.find_element(By.CSS_SELECTOR, 'div[dir="ltr"]').text
                chats.append({'name': name, 'last_message': last_msg})
            except Exception:
                continue
        return chats

    def open_chat(self, contact_name):
        search_box = self.driver.find_element(By.XPATH, '//div[@title="Search input textbox"]')
        search_box.clear()
        search_box.send_keys(contact_name)
        time.sleep(2)
        try:
            chat = self.driver.find_element(By.XPATH, f'//span[@title="{contact_name}"]')
            chat.click()
            time.sleep(2)
            return True
        except NoSuchElementException:
            return False

    def get_messages(self, contact_name):
        if not self.open_chat(contact_name):
            return []
        messages = []
        msg_bubbles = self.driver.find_elements(By.CSS_SELECTOR, 'div.message-in, div.message-out')
        for msg in msg_bubbles:
            try:
                text = msg.find_element(By.CSS_SELECTOR, 'span.selectable-text').text
                sent = 'message-out' in msg.get_attribute('class')
                messages.append({'text': text, 'sent': sent})
            except Exception:
                continue
        return messages

    def send_message(self, contact_name, message):
        if not self.open_chat(contact_name):
            return False
        input_box = self.driver.find_element(By.XPATH, '//div[@title="Type a message"]')
        input_box.click()
        input_box.send_keys(message + Keys.ENTER)
        time.sleep(1)
        return True

    def forward_message(self, to_contact, message):
        return self.send_message(to_contact, message)

# Singleton instance
whatsapp_api = WhatsAppAPI()
