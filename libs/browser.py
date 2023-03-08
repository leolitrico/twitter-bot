from time import sleep
from selenium import webdriver

DRIVER_PATH = '/usr/bin/chromedriver'
BINARY_PATH = '/usr/bin/google-chrome'

def get_browser(profile_path=None, profile_name=None):
    options = webdriver.ChromeOptions()
    options.binary_location = BINARY_PATH
    options.add_argument('--headless=new')
    options.add_argument('--disable-dev-shm-usage') 

    #add chrome profile to persist cookies
    if profile_path is not None and profile_name is not None:
        options.add_argument('--user-data-dir=' + profile_path)
        options.add_argument('--profile-directory=' + profile_name)

    browser = webdriver.Chrome(options = options, executable_path = DRIVER_PATH)
    sleep(3)
    return browser