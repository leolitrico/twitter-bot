import sys
import pathlib
sys.path.append(str(pathlib.Path(__file__).parent.absolute()) + "/../")

import datetime
from libs.twitter import login, get_followers, get_follow_count, follow, unfollow
from bot.data import store_data, contains, remove_before, load_data
from libs.browser import get_browser

##############################################################################################
# constants
##############################################################################################
PROFILE_OPT = "--profile"

FOLLOWER_LIMIT_OPT = "--follower-limit"
FOLLOWER_LIMIT = 30

RATIO_LIMIT_OPT = "--ratio-limit"
RATIO_LIMIT = 3

FOLLOW_AMOUNT_OPT = "--follow-amount"
FOLLOW_AMOUNT = 10

##############################################################################################
# parse arguments
##############################################################################################

argv = sys.argv[1:]

botUsername = argv[0]
botPassword = argv[1]

targetUsername = argv[2]
targetPassword = argv[3]

profile_path = None
botProfile = None
targetProfile = None
if PROFILE_OPT in argv:
    i = argv.index(PROFILE_OPT)
    profile_path = argv[i + 1]
    botProfile = argv[i + 2]
    targetProfile = argv[i + 3]

followerLimit = FOLLOWER_LIMIT
if FOLLOWER_LIMIT_OPT in argv:
    i = argv.index(FOLLOWER_LIMIT_OPT)
    followerLimit = int(argv[i + 1])

ratioLimit = RATIO_LIMIT
if RATIO_LIMIT_OPT in argv:
    i = argv.index(RATIO_LIMIT_OPT)
    ratioLimit = int(argv[i + 1])

followAmount = FOLLOW_AMOUNT
if FOLLOW_AMOUNT_OPT in argv:
    i = argv.index(FOLLOW_AMOUNT_OPT)
    followAmount = int(argv[i + 1])


##############################################################################################
# functions
##############################################################################################
def users_to_follow(browser, data):
    #get all my followers
    myFollowers = get_followers(browser, targetUsername, 1000)

    #init list of new people to follow
    usersToFollow = []

    #for each of my followers, get their followers
    for follower in myFollowers:
        theirFollowers = get_followers(browser, follower, 1000)
        for f in theirFollowers:
            #if they are not already in my followers, and they have a small amount of followers, add to list
            if not contains(data, f):
                following, followers = get_follow_count(browser, f)
                if following / followers > ratioLimit and followers < followerLimit:
                    usersToFollow.append(f)
                    data.append((f, datetime.datetime.now()))
                    if len(usersToFollow) > followAmount:
                        return usersToFollow
    return usersToFollow

##############################################################################################
# retrieve data
##############################################################################################
botBrowser = get_browser(profile_path, botProfile)

#login to bot account
login(botBrowser, botUsername, botPassword)

#list of pairs (username, time when followed)
data = load_data()

#remove all users that were followed more than 1 week ago
usersToUnFollow = remove_before(data, datetime.datetime.now() - datetime.timedelta(days=7))

#get the list of users to follow
usersToFollow = users_to_follow(botBrowser, data)

#close the bot browser
botBrowser.close()

#store the data
store_data(data)


##############################################################################################
# follow/unfollow
##############################################################################################
targetBrowser = get_browser(profile_path, targetProfile)

#follow each user
for user in usersToFollow:
    follow(targetBrowser, user)

#unfollow each user
for user in usersToUnFollow:
    unfollow(targetBrowser, user)

#close the target browser
targetBrowser.close()


