import pandas as pd
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
import time

CHROMEPATH = 'YOUR_CHROMEDRIVER_PATH'

contacts = None
saved_len = None
unsaved_len = None
message = None


def read_contacts(file_name):
    global contacts, saved_len, unsaved_len
    csv = file_name + '.csv'
    contacts = pd.read_csv(csv)
    saved_len = len(contacts['Saved Contacts'])
    unsaved_len = len(contacts['Unsaved Contacts'])


def input_message():
    global message
    print('Enter your message and press ` to exit:\n\n')
    message = []
    text = ""
    check = False
    while not check:
        text = input()
        if len(text) != 0 and text[-1] == '`':
            check = True
            message.append(text[:-1])
        else:
            message.append(text)
    message = "\n".join(message)


def saved_message():
    global message
    for contact in contacts['Saved Contacts']:
        target = str(contact)
        target = '"' + target + '"'
        x_arg = '//span[contains(@title,' + target + ')]'
        group_title = waiter.until(EC.presence_of_element_located((By.XPATH, x_arg)))
        group_title.click()
        browser.implicitly_wait(2)
        try:
            message_box = browser.find_element_by_xpath('//*[@id="main"]/footer/div[1]/div[2]/div/div[2]')
            for ch in message:
                if ch == "\n":
                    ActionChains(browser).key_down(Keys.SHIFT).key_down(Keys.ENTER).key_up(Keys.ENTER).key_up(
                        Keys.SHIFT).key_up(Keys.BACKSPACE).perform()
                else:
                    message_box.send_keys(ch)
            message_box.send_keys(Keys.ENTER)
        except NoSuchElementException:
            print(f'Contact not found - {target}')
            return
    time.sleep(10)


def unsaved_message():
    global message
    for number in contacts['Unsaved Contacts']:
        target = str(number)
        link = f"https://web.whatsapp.com/send?phone={target}&text&source&data&app_absent"
        browser.get(link)
        time.sleep(10)
        try:
            message_box = browser.find_element_by_xpath('//*[@id="main"]/footer/div[1]/div[2]/div/div[2]')
            for ch in message:
                if ch == "\n":
                    ActionChains(browser).key_down(Keys.SHIFT).key_down(Keys.ENTER).key_up(Keys.ENTER).key_up(
                        Keys.SHIFT).key_up(Keys.BACKSPACE).perform()
                else:
                    message_box.send_keys(ch)
            message_box.send_keys(Keys.ENTER)
        except NoSuchElementException:
            print(f'Number not available - {target}')
            return
    time.sleep(10)


if __name__ == "__main__":
    file = input('Enter name of contacts file (csv): ')
    read_contacts(file)

    input_message()

    browser = webdriver.Chrome(CHROMEPATH)
    browser.get('https://web.whatsapp.com')
    waiter = WebDriverWait(browser, 120)

    if saved_len > 0:
        saved_message()
    if unsaved_len > 0:
        unsaved_message()
    browser.close()
    print('Messaging completed')
