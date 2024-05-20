from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from tkinter import messagebox
import selenium.common.exceptions as exc
import os
import time


RUNTIME = 660
TRANSITION = 3
INITIAL_TRANSITIONS = 5

def transition():
    time.sleep(TRANSITION)
def wait_five_sec():
    time.sleep(INITIAL_TRANSITIONS)

def initial_transition(driver):
    driver.implicitly_wait(5)


def open_browser():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(options=chrome_options)

    return driver

def tinder_login(driver):
    email = os.environ.get("USERNAME")
    pw = os.environ.get("PW")
    login = driver.find_element(By.LINK_TEXT, value="Log in")
    login.click()
    initial_transition(driver)
    facebook_button = driver.find_element(
        By.CSS_SELECTOR,
        value='.Typs\(button-1\)')
    facebook_button.click()
    initial_transition(driver)
    main_window = driver.window_handles[0]
    wait_five_sec()
    fb_login = driver.window_handles[1]
    driver.switch_to.window(fb_login)
    email_input = driver.find_element(By.ID, value="email")
    email_input.send_keys(email)
    pw_input = driver.find_element(By.ID, value="pass")
    pw_input.send_keys(pw)
    fb_login_button = driver.find_element(By.ID, value="loginbutton")
    fb_login_button.click()
    wait_five_sec()
    driver.switch_to.window(main_window)


def accept_settings(driver):
    accept = driver.find_element(By.CSS_SELECTOR, value=".c9iqosj")
    accept.click()
    enable = driver.find_element(By.CSS_SELECTOR, value=".c9iqosj")
    enable.click()
    driver.implicitly_wait(10)


def check_for_interests(driver):
    my_passions = ["music", "movies", "tattoos","coffee", "travel",
                         "horror movies", "concerts", "working out", "reading",
                         "wine", "heavy metal", "hip hop", "live music", "sushi", "anime", "gym",
                   "xbox", "ice cream", "pro-choice"]

    interests_match = False
    action = ActionChains(driver)
    action.key_down(Keys.UP).key_up(Keys.UP)
    action.perform()
    transition()
    elements = driver.find_elements(By.CSS_SELECTOR, value=".Typs\(body-2-regular\)")
    keywords = [element.text.lower() for element in elements]
    for keyword in keywords:
        if keyword in my_passions:
            interests_match = True
            break

    return interests_match

def swipe(driver, counter):
    action = ActionChains(driver)
    match = check_for_interests(driver)
    if match:

        action.key_down(Keys.RIGHT).key_up(Keys.RIGHT)
        action.perform()
    else:
        action.key_down(Keys.LEFT).key_up(Keys.LEFT)
        action.perform()
    transition()
    if counter == 5:
        dismiss_installation(driver, counter)

def sequence(driver):
    counter = 0
    start = int(time.time())
    end = int(time.time() + RUNTIME)

    while start < end:
        swipe(driver, counter)
        counter += 1
        increment = int(time.time())
        difference = increment - start

        if difference >= 1:
            start += difference

        if start >= end:
            messagebox.showinfo(title="Finished", message="Automated swiping process complete.")


def dismiss_installation(my_driver, counter):
        not_interested = my_driver.find_elements(By.CSS_SELECTOR,value='.c9iqosj')[1]
        not_interested.click()


chrome_driver = open_browser()

try:
    chrome_driver.get("https://www.tinder.com")
    chrome_driver.implicitly_wait(30)
    tinder_login(chrome_driver)
    accept_settings(chrome_driver)
    time.sleep(10)
    sequence(chrome_driver)
except exc.NoSuchElementException as exc:
    print(exc.msg)
    chrome_driver.quit()
except exc.StaleElementReferenceException as exc:
    print(exc.msg)
    chrome_driver.quit()
