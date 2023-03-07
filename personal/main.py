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
sys.path.append(str(pathlib.Path(__file__).parent.absolute()) + "/../")

from libs.twitter import login, get_following, follow, unfollow
from libs.browser import get_browser

##############################################################################################
# constants
##############################################################################################
NUMBER_TRIES = 5
DATE_FORMAT = "%Y-%m-%d"

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
            return usersToUnfollow
    except:
        print("unable to get users to unfollow")
        return []
    
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

    ##############################################################################################
    # main
    ##############################################################################################

    # login
    browser = get_browser()
    login(browser, username, password)

    # get following
    following = get_following(browser, username)

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

    # follow users
    i = 0
    for user in usersToFollow:
        if i >= followNumber:
            break

        if user not in following:
            follow(browser, user, numberTries=NUMBER_TRIES)
            wereFollowed.write(user + '\n')
            usersFollowed.append((user, datetime.datetime.now().strftime(DATE_FORMAT)))
            i += 1
            
    wereFollowed.close()

    # store users to follow
    store_users_to_follow(followFilename, usersToFollow[i:])
    store_users_followed(followedFilename, usersFollowed)

    # unfollow users
    for user in usersToUnfollow:
        if user not in following:
            unfollow(browser, user[0], numberTries=NUMBER_TRIES)

if __name__ == "__main__":
    main()
