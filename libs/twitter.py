from time import sleep
import random
import locale

from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

RANGE = 5

def random_sleep(min):
    sleep(random.randint(min, min + RANGE))


def login(browser, username, password, verifier=None, numberOfTries=1):
    for i in range(numberOfTries):
        try:
            browser.get("https://twitter.com/home")
            sleep(3)

            if browser.current_url == "https://twitter.com/home":
                return
            
            browser.get("http://twitter.com/i/flow/login/")
            sleep(3)
            #Enter Your Username Here
            browser.find_element(By.XPATH,"//input[@name='text']").send_keys(username)
            browser.find_element(By.XPATH,"/html/body/div[1]/div/div/div[1]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[6]").click()
            sleep(3)
            #Enter Your Password here
            browser.find_element(By.XPATH,"//input[@name='password']").send_keys(password)
            browser.find_element(By.XPATH,"/html/body/div/div/div/div[1]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div[1]/div/div/div").click()
            sleep(3)
            #Enter Verification
            if verifier != None and browser.current_url != "https://twitter.com/home":
                browser.find_element(By.XPATH,"//input[@name='text']").send_keys(verifier)
                browser.find_element(By.XPATH,"//div[@role='button' and @test-id='ofcEnterTextNextButton']").click()
                sleep(3)
        except NoSuchElementException:
            continue

def get_followers(browser, name, limit=None, numberOfTries=1):
    for i in range(numberOfTries):
        try:
            follower_list = []
            browser.get("https://twitter.com/" + name + "/followers")
            sleep(3)
            # Code to goto End of the Page
            last_height = browser.execute_script("return document.body.scrollHeight")
            counter = 0
            while True:
                #get usernames element
                usernames = browser.find_elements(By.XPATH, "//div[@data-testid='cellInnerDiv']//a[@role='link']//span")
                for username in usernames:
                    if limit != None and counter >= limit:
                        return follower_list
                    
                    username = username.text
                    if len(username) > 0 and username[0] == '@': 
                        username = str(username[1:])
                        if username not in follower_list:
                            follower_list.append(username)
                            counter += 1
                # Scroll down to bottom
                browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                # Wait to load page
                sleep(3)
                # Calculate new scroll height and compare with last scroll height
                new_height = browser.execute_script("return document.body.scrollHeight")
                if new_height == last_height:
                    break
                last_height = new_height
            return True, follower_list
        except NoSuchElementException: 
            continue
        except:
            return False, follower_list
    return True, []

def get_following(browser, name, limit=None, numberOfTries=1):
    for i in range(numberOfTries):
        try:
            follower_list = []
            browser.get("https://twitter.com/" + name + "/following")
            sleep(3)
            # Code to goto End of the Page
            last_height = browser.execute_script("return document.body.scrollHeight")
            counter = 0
            while True:
                #get usernames element
                usernames = browser.find_elements(By.XPATH, "//div[@data-testid='cellInnerDiv']//a[@role='link']//span")
                for username in usernames:
                    if limit != None and counter >= limit:
                        return follower_list
                    
                    username = username.text
                    if len(username) > 0 and username[0] == '@': 
                        username = str(username[1:])
                        if username not in follower_list:
                            follower_list.append(username)
                            counter += 1
                # Scroll down to bottom
                browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                sleep(3)
                # Calculate new scroll height and compare with last scroll height
                new_height = browser.execute_script("return document.body.scrollHeight")
                if new_height == last_height:
                    break
                last_height = new_height
            return True, follower_list
        except NoSuchElementException: 
            continue
        except:
            return False, follower_list
    return True, []

#returns (following, followers)
def get_follow_count(browser, name, numberOfTries=1):
    for i in range(numberOfTries):
        try:
            browser.get("https://twitter.com/" + name)
            sleep(3)
            #get follower count element
            follower_count = browser.find_element(By.XPATH, "/html/body/div[1]/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div/div/div/div[5]/div[2]/a/span[1]/span")
            #get following count element
            following_count = browser.find_element(By.XPATH, "/html/body/div[1]/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div/div/div/div[5]/div[1]/a/span[1]/span")

            locale.setlocale( locale.LC_ALL, 'en_US.UTF-8' ) 
            try:
                return locale.atoi(following_count.text), locale.atoi(follower_count.text)
            except locale.Error:
                return 100, 10000
        except NoSuchElementException:
            continue
    return 100, 10000

def follow(browser, name, numberOfTries=1):
    for i in range(numberOfTries):
        try:
            browser.get("https://twitter.com/" + name)
            random_sleep(4)
            #get follow button element
            follow_button = None
            try: 
                follow_button = browser.find_element(By.XPATH, "/html/body/div[1]/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div/div/div/div[1]/div[2]/div[2]/div[1]/div")
            except:
                follow_button = browser.find_element(By.XPATH, "/html/body/div[1]/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div/div/div/div[1]/div[2]/div[3]/div[1]/div")

            follow_button.click()
            sleep(1)
            return True
        except NoSuchElementException:
            continue
    return False

def unfollow(browser, name, numberOfTries=1):
    for i in range(numberOfTries):
        try:
            browser.get("https://twitter.com/" + name)
            random_sleep(4)
            #get follow button element
            follow_button = None
            try:
                follow_button = browser.find_element(By.XPATH, "/html/body/div[1]/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div/div/div[1]/div[1]/div[2]/div[4]/div[1]/div")
            except:
                follow_button = browser.find_element(By.XPATH, "/html/body/div[1]/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div/div/div[1]/div[1]/div[2]/div[4]/div[1]/div")
            follow_button.click()
            sleep(1)
            return True
        except NoSuchElementException:
            continue
    return False
