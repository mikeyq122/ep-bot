from selenium.webdriver.chrome.options import Options
from selenium import webdriver
import random
import time
from pynput.keyboard import Controller, Key
import suspend
from pathlib import Path
#only used if auto login is enabled on line 113: 'login(b)'
#if you are using auto-login you will need to make it (defferent per school)
email='ENTER HERE'
password='ENTER HERE'

sleeptime=3

kb = Controller()


def wait_for_trigger():
    suspend.wait_for_key('Key.ctrl_l')

def ran_sleep(multi):
    # random from 1 - 3 (has decimals) multiplied by the input variable
    delay=random.randrange(10,30)/10
    duration=delay*multi
    print("sleeping for " + str(duration))
    time.sleep(duration)

def make_browser():
    opts = Options()
    opts.add_argument("user-agent=user")
    browser = webdriver.Firefox(executable_path='./geckodriver.exe')
    browser.delete_all_cookies()
    browser.get("https://www.educationperfect.com/controlpanel/#/login")
    return browser

def login(browser):
    a=0 #placeholder
    # make login



def read_page(browser):
    on_screen_element = browser.find_element_by_id('question-text')
    return on_screen_element.text

def make_def(browser, onscreen):
    file='./defs/' + str(onscreen)
    print('Creating a definition for ' + str(file))
    f=open(file, "a")

    textbox = browser.find_element_by_css_selector('#answer-text-container > input:nth-child(1)')
    textbox.send_keys('?')

    time.sleep(sleeptime)

    submit_button = browser.find_element_by_id('submit-button')
    submit_button.click()

    time.sleep(sleeptime)

    read = browser.find_element_by_id('correct-answer-field')
    answer = read.text

    f.write(answer)
    answer_field = browser.find_element_by_id('answer-text')
    answer_field.send_keys(answer)

def answer_question(browser, fn):
    f=open(fn, "r")
    text = f.read()
    print('Found def, ' + str(text))

    textbox = browser.find_element_by_css_selector('#answer-text-container > input:nth-child(1)')
    textbox.send_keys(text)

    time.sleep(sleeptime)

    submit_button = browser.find_element_by_id('submit-button')
    submit_button.click()

def check_if_done(browser):
    try:
        exit_button = browser.find_element_by_id('end-test')
        exit_button.click()
    except:
        a=0
    else:
        print('Finished list! Giving control back')
        wait_for_trigger()

def auto_answer(br):
    text_onscreen = str(read_page(br))
    text_onscreen = text_onscreen.replace(' ', '_')
    text_onscreen = text_onscreen.replace('"', '')
    text_onscreen = text_onscreen.replace('(', '')
    text_onscreen = text_onscreen.replace(')', '')
    text_onscreen = text_onscreen.replace('/', '.')

    check_if_done(br)

    filename = Path('./defs/' + str(text_onscreen))
    if filename.is_file():
        answer_question(br, filename)
    else:
        make_def(br, text_onscreen)
    time.sleep(sleeptime)

b = make_browser()
time.sleep(5)

print(1)

login(b)

wait_for_trigger()

while True:
    try:
        auto_answer(b)
    except:
        print("something went fucky wucky")
        wait_for_trigger()

print(0)
