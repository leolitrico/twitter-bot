import sys
sys.path.append("../")

import datetime
from libs.twitter import login, get_followers, get_follow_count, follow, unfollow
from bot.data import store_data, contains, remove_before, load_data
from libs.browser import get_browser

BOT_USERNAME = ""
BOT_PASSWORD = ""

TARGET_USERNAME = ""
TARGET_PASSWORD = ""

BROWSER_PROFILE_PATH = "/home/leo/.config/google-chrome"

BROWSER_PROFILE_NAME_BOT = "Profile 1"
BROWSER_PROFILE_NAME_MY = ""

FOLLOWING_LIMIT = 30
FOLLOW_RATIO_LOWER_BOUND = 3
FOLLOW_AT_A_TIME = 10


##############################################################################################
# functions
##############################################################################################

def users_to_follow(browser, data):
    #get all my followers
    myFollowers = get_followers(browser, TARGET_USERNAME, 1000)

    #init list of new people to follow
    usersToFollow = []

    #for each of my followers, get their followers
    for follower in myFollowers:
        theirFollowers = get_followers(browser, follower, 1000)
        for f in theirFollowers:
            #if they are not already in my followers, and they have a small amount of followers, add to list
            if not contains(data, f):
                following, followers = get_follow_count(browser, f)
                if following / followers > FOLLOW_RATIO_LOWER_BOUND and followers < FOLLOWING_LIMIT:
                    usersToFollow.append(f)
                    data.append((f, datetime.datetime.now()))
                    if len(usersToFollow) > FOLLOW_AT_A_TIME:
                        return usersToFollow
    return usersToFollow

##############################################################################################
# main
##############################################################################################
bot_browser = get_browser(BROWSER_PROFILE_PATH, BROWSER_PROFILE_NAME_BOT)
my_browser = get_browser(BROWSER_PROFILE_PATH, BROWSER_PROFILE_NAME_MY)

#login to bot account
bot_browser.login(BOT_USERNAME, BOT_PASSWORD)

#list of pairs (username, time when followed)
data = load_data()

#remove all users that were followed more than 1 week ago
usersToUnFollow = remove_before(data, datetime.datetime.now() - datetime.timedelta(days=7))

#get the list of users to follow
usersToFollow = users_to_follow(bot_browser, data)

#follow each user
for user in usersToFollow:
    follow(my_browser, user)

for user in usersToUnFollow:
    unfollow(my_browser, user)

store_data(data)


