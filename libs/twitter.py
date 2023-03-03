

from libs.random_sleep import random_sleep
from selenium.webdriver.common.by import By


def login(browser, username, password):
    random_sleep(3)
    browser.get("https://twitter.com/home")
    random_sleep(3)

    if browser.current_url == "https://twitter.com/home":
        return
    
    browser.get("http://twitter.com/i/flow/login/")
    random_sleep(3)
    #Enter Your Username Here
    browser.find_element(By.XPATH,"//input[@name='text']").send_keys(username)
    random_sleep(2)
    browser.find_element(By.XPATH,"/html/body/div[1]/div/div/div[1]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[6]").click()
    random_sleep(3)
    #Enter Your Password here
    browser.find_element(By.XPATH,"//input[@name='password']").send_keys(password)
    random_sleep(3)
    browser.find_element(By.XPATH,"/html/body/div/div/div/div[1]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div[1]/div/div/div").click()

def get_followers(browser, name, limit):
    follower_list = []
    random_sleep(3)
    browser.get("https://twitter.com/" + name + "/followers")
    random_sleep(3)
    # Code to goto End of the Page
    last_height = browser.execute_script("return document.body.scrollHeight")
    counter = 0
    while True:
        # Scroll down to bottom
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # Wait to load page
        random_sleep(2)
        # Calculate new scroll height and compare with last scroll height
        new_height = browser.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

        #get usernames element
        usernames = browser.find_elements(By.XPATH, "//div[@data-testid='cellInnerDiv']//a[@role='link']//span")
        for username in usernames:
            if counter >= limit:
                return follower_list
            
            username = username.text
            if username not in follower_list and len(username) > 0 and username[0] == '@':
                follower_list.append(username[1:])
                counter += 1
    return follower_list

#returns (following, followers)
def get_follow_count(browser, name):
    random_sleep(3)
    browser.get("https://twitter.com/" + name)
    random_sleep(3)
    #get follower count element
    follower_count = browser.find_element(By.XPATH, "/html/body/div[1]/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div/div/div/div[5]/div[2]/a/span[1]/span")
    #get following count element
    following_count = browser.find_element(By.XPATH, "/html/body/div[1]/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div/div/div/div[5]/div[1]/a/span[1]/span")

    return int(following_count), int(follower_count.text)

def follow(browser, name):
    random_sleep(3)
    browser.get("https://twitter.com/" + name)
    random_sleep(3)
    #get follow button element
    follow_button = browser.find_element(By.XPATH, "/html/body/div[1]/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div/div/div/div[1]/div[2]/div[3]/div[1]/div")
    follow_button.click()

def unfollow(browser, name):
    random_sleep(3)
    browser.get("https://twitter.com/" + name)
    random_sleep(3)
    #get follow button element
    follow_button = browser.find_element(By.XPATH, "/html/body/div[1]/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div/div/div[1]/div[1]/div[2]/div[4]/div[1]/div")
    follow_button.click()
