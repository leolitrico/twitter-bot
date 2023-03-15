# Description: This script will filter through a accounts followers' followers and output users that meet certain criteria. This script is meant to be used with the populate script.
# Arguments:
# botUsername: username of the bot account
# botPassword: password of the bot account
# followers: file containing the users that follow target's followers
# n: number of users to output
# Options:
# --profile: use a chrome profile for the bot (--profile path profileName)
# --follower-limit: max number of followers an eligible user can have to follow them
# --ratio-limit: limit the ratio of followers to following an eligible user can have to follow them
# --file: file to store the users in


import sys
from time import sleep
import pathlib
sys.path.append(str(pathlib.Path(__file__).parent.absolute()) + "/../")

from libs.twitter import login, get_follow_count
from libs.browser import get_browser

##############################################################################################
# constants
##############################################################################################
PROFILE_OPT = "--profile"

FOLLOWER_LIMIT_OPT = "--follower-limit"
FOLLOWER_LIMIT = 100

RATIO_LIMIT_OPT = "--ratio-limit"
RATIO_LIMIT = 8

N = 10

FILE_OPT = "--file"

NUMBER_TRIES = 5

##############################################################################################
# functions
##############################################################################################
#load followers
def load_followers(filename):
    followedUsers = []
    try:
        with open(filename, "r") as f:
            for line in f:
                followedUsers.append(line.strip())
    except:
        print("Error: unable to load followed users from file " + filename)
        return None
    return followedUsers

def store_users_to_follow(filename, usersToFollow):
    try:
        with open(filename, 'w') as file:
            for user in usersToFollow:
                file.write(user + '\n')
    except:
        print("unable to store users to follow")

def main():
    ##############################################################################################
    # parse arguments
    ##############################################################################################
    botUsername = None
    botPassword = None
    profile_path = None
    botProfile = None
    followersFilename = None
    filename = None
    n = N
    followerLimit = FOLLOWER_LIMIT
    ratioLimit = RATIO_LIMIT
    try:
        argv = sys.argv[1:]

        botUsername = argv[0]
        botPassword = argv[1]

        followersFilename = argv[2]
        n = int(argv[3])

        if PROFILE_OPT in argv:
            i = argv.index(PROFILE_OPT)
            profile_path = argv[i + 1]
            botProfile = argv[i + 2]

        if FOLLOWER_LIMIT_OPT in argv:
            i = argv.index(FOLLOWER_LIMIT_OPT)
            followerLimit = int(argv[i + 1])

        if RATIO_LIMIT_OPT in argv:
            i = argv.index(RATIO_LIMIT_OPT)
            ratioLimit = int(argv[i + 1])
        
        if FILE_OPT in argv:
            i = argv.index(FILE_OPT)
            filename = argv[i + 1]

    except:
        print("Error: invalid arguments")
        return

    ##############################################################################################
    # main
    ##############################################################################################
    followers = load_followers(followersFilename)
    if followers == None:
        return
    
     #file to store all the users to follow
    file = None
    if filename == None:
        file = sys.stdout
    else:
        try: 
            file = open(filename, "a")
        except:
            print("Error: unable to write to file " + filename)
            return

    botBrowser = get_browser(profile_path, botProfile)

    #login to bot account
    login(botBrowser, botUsername, botPassword)

    print("filtering users...")
    i = -1
    try: 
        for follower in followers:
            i += 1
            try:
                following_count, follow_count = get_follow_count(botBrowser, follower, numberOfTries=NUMBER_TRIES)
            except:
                sleep(100)
                botBrowser = get_browser(profile_path, botProfile)
                login(botBrowser, botUsername, botPassword)
                
            ratio = 100
            if follow_count != 0:
                ratio = following_count / follow_count

            if following_count < followerLimit or ratio > ratioLimit:
                file.write(follower + "\n")
                print(follower)
                n -= 1
                if n == 0:
                    break
        print("Successfully filtered " + str(i + 1) + " users")
    except:
        print("Error: only able to filter " + str(i + 1) + " users")
    finally: 
        if i + 1 < len(followers) and i >= 0:
            store_users_to_follow(followersFilename, followers[i + 1:])
        elif i != -1:
            store_users_to_follow(followersFilename, [])
        file.close()

if __name__ == "__main__":
    print("##############################################")
    main()
    print("##############################################")

