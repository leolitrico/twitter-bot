# Description: follow users from a file, and unfollow users based on how long ago you followed them
# Arguments:
    # username: twitter username
    # password: twitter password
    # followNumber: number of users to follow
    # followFilename: file to read users from
    # followedFilename: file to store users that were followed by this script and date followed (user, date) format
    # wereFollowedFilename: file to store users that were followed at any point in time

# Options:
    # --profile: use a chrome profile (--profile path profileName)

import sys
import pathlib
import datetime
from time import sleep
sys.path.append(str(pathlib.Path(__file__).parent.absolute()) + "/../")

from libs.twitter import login, get_following, follow, unfollow
from libs.browser import get_browser

##############################################################################################
# constants
##############################################################################################
NUMBER_TRIES = 5
DATE_FORMAT = "%Y-%m-%d"
PROFILE_OPT = "--profile"
VERIFY_OPT = "--verify"

##############################################################################################
# functions
##############################################################################################
def get_users_to_follow(filename):
    try:
        with open(filename, 'r') as file:
            usersToFollow = []
            for line in file:
                usersToFollow.append(line.strip())
            return usersToFollow
    except:
        print("unable to get users to follow")
        return []

def store_users_to_follow(filename, usersToFollow):
    try:
        with open(filename, 'w') as file:
            for user in usersToFollow:
                file.write(user + '\n')
    except:
        print("unable to store users to follow")

def get_users_to_unfollow(filename):
    try:
        with open(filename, 'r') as file:
            usersToUnfollow = []
            usersToKeep = []
            for line in file:
                line = line.strip()
                line = line.split(',')
                #if user was followed more than a week ago
                if datetime.datetime.now() - datetime.datetime.strptime(line[1], DATE_FORMAT) > datetime.timedelta(days=7):
                    usersToUnfollow.append(line[0])
                else:
                    usersToKeep.append((line[0], line[1]))
            return usersToUnfollow, usersToKeep
    except:
        print("unable to get users to unfollow")
        return [], []
    
def store_users_followed(filename, usersToUnfollow):
    try:
        with open(filename, 'w') as file:
            for user in usersToUnfollow:
                file.write(user[0] + ',' + user[1] + '\n')
    except:
        print("unable to store users to unfollow")

def main():
    ##############################################################################################
    # parse arguments
    ##############################################################################################
    argv = sys.argv[1:]

    username = argv[0]
    password = argv[1]
    followNumber = int(argv[2])
    followFilename = argv[3]
    followedFilename = argv[4]
    wereFollowedFilename = argv[5]
    profile_path = None
    profile = None
    verifier = None

    if PROFILE_OPT in argv:
        i = argv.index(PROFILE_OPT)
        profile_path = argv[i + 1]
        profile = argv[i + 2]

    if VERIFY_OPT in argv:
        i = argv.index(VERIFY_OPT)
        verifier = argv[i + 1]


    ##############################################################################################
    # main
    ##############################################################################################

    # login
    browser = get_browser(profile_path, profile, verifier=verifier)
    login(browser, username, password)

    # get following
    success, following = get_following(browser, username)

    #get users to follow
    usersToFollow = get_users_to_follow(followFilename)

    # get users to unfollow, and users that were followed by this script
    usersToUnfollow, usersFollowed = get_users_to_unfollow(followedFilename)

    #open were followed file in append only mode
    wereFollowed = None
    try:
        wereFollowed = open(wereFollowedFilename, 'a')
    except:
        print("error opening were followed file")
        return
    
    print("following users...")
    i = 0
    try: 
        # follow users
        for user in enumerate(usersToFollow):
            if i >= followNumber:
                break

            if user not in following:
                try:
                    if(follow(browser, user, numberOfTries=NUMBER_TRIES)):
                        wereFollowed.write(user + '\n')
                        usersFollowed.append((user, datetime.datetime.now().strftime(DATE_FORMAT)))
                        i += 1
                except:
                    browser = get_browser(profile_path, profile, verifier=verifier)
                    login(browser, username, password)
    except:
        print("error following users")
    finally:
        wereFollowed.close()

    # store users to follow
    if i < len(usersToFollow):
        store_users_to_follow(followFilename, usersToFollow[i:])
    else:
        store_users_to_follow(followFilename, [])
        
    store_users_followed(followedFilename, usersFollowed)

    # unfollow users
    print("unfollowing users...")
    try:
        for user in usersToUnfollow:
            if user not in following:
                try:
                    unfollow(browser, user[0], numberOfTries=NUMBER_TRIES)
                except:
                    sleep(100)
                    browser = get_browser(profile_path, profile, verifier=verifier)
                    login(browser, username, password)
    except:
        print("error unfollowing users")

if __name__ == "__main__":
    print("##############################################")
    main()
    print("##############################################")

