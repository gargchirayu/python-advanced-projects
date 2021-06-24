import time
import pause
from datetime import datetime

from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver

CHROMEPATH = 'YOUR_CHROMEDRIVER_PATH'
now = datetime.now()


def meetbot(url, email, password, session_length):
    pause.until(datetime(now.year, now.month, now.day, hours, minutes))
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-infobars")
    options.add_argument("--mute-audio")
    options.add_argument("--mute-video")
    options.add_experimental_option("prefs", {
        "profile.default_content_setting_values.media_stream_mic": 2,  # 1:allow, 2:block
        "profile.default_content_setting_values.media_stream_camera": 2,
        "profile.default_content_setting_values.notifications": 2
    })

    browser = webdriver.Chrome(CHROMEPATH, options=options)
    browser.get(
        'https://accounts.google.com/o/oauth2/auth/identifier?client_id=717762328687-iludtf96g1hinl76e4lc1b9a82g457nn.apps.googleusercontent.com&scope=profile%20email&redirect_uri=https%3A%2F%2Fstackauth.com%2Fauth%2Foauth2%2Fgoogle&state=%7B%22sid%22%3A1%2C%22st%22%3A%2259%3A3%3Abbc%2C16%3A7df599f842c1c0ce%2C10%3A1598275142%2C16%3A711b928803291f44%2Cd0c138b07c19d9d5eb84f1bd1b19ab2404b4db091a4bb6270fb887a665114b3d%22%2C%22cdl%22%3Anull%2C%22cid%22%3A%22717762328687-iludtf96g1hinl76e4lc1b9a82g457nn.apps.googleusercontent.com%22%2C%22k%22%3A%22Google%22%2C%22ses%22%3A%22a0b44e88bafc415789def65b91b12e3e%22%7D&response_type=code&hl=en&flowName=GeneralOAuthFlow')
    browser.implicitly_wait(2)

    email_field = browser.find_element_by_id('identifierId')
    email_field.send_keys(email)
    next_button = browser.find_element_by_id('identifierNext')
    next_button.click()
    browser.implicitly_wait(2)
    pass_field = browser.find_element_by_xpath('//*[@id="password"]/div[1]/div/div[1]/input')
    pass_field.send_keys(password)
    submit_button = browser.find_element_by_id('passwordNext')
    submit_button.click()
    browser.implicitly_wait(2)

    browser.get('https://meet.google.com')
    time.sleep(10)
    try:
        signin = browser.find_element_by_xpath('/html/body/header/div[1]/div/div[3]/div[1]/div/span[1]/a')
        signin.click()
        browser.implicitly_wait(2)
    except NoSuchElementException:
        pass
    browser.get(url)
    dismiss = browser.find_element_by_xpath('//*[@id="yDmH0d"]/div[3]/div/div[2]/div[3]/div')
    dismiss.click()

    try:
        browser.find_element_by_xpath("//span[@class='NPEfkd RveJvd snByac' and contains(text(), 'Join now')]").click()

    except NoSuchElementException:
        browser.find_element_by_xpath(
            "//span[@class='NPEfkd RveJvd snByac' and contains(text(), 'Ask to join')]").click()

    time.sleep(60 * session_length)
    print("closing meeting")
    browser.close()


url = input('Enter meet link: ')
email = input('Institution mail address: ')
password = input('Password: ')
print('Enter Start time: (24 hours format, without preceding zeros)')
hours = int(input('Hour: '))
minutes = int(input('Minutes: '))
session_length = int(input('Session length: (in minutes) '))

meetbot(url, email, password, session_length)
