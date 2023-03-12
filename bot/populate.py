# Description: This script will find all the followers of a user's followers
# Arguments:
# botUsername: username of the bot account
# botPassword: password of the bot account
# targetUsername: username of the target account
# wereFollowed: file containing the users that were followed at any time
# Options:
# --profile: use a chrome profile for the bot (--profile path profileName)
# --follower-limit: max number of followers an eligible user can have to follow them
# --ratio-limit: limit the ratio of followers to following an eligible user can have to follow them
# --file: file to store the users in
# --max: max number of users to follow (default 100) 


import sys
import pathlib
sys.path.append(str(pathlib.Path(__file__).parent.absolute()) + "/../")

from libs.twitter import login, get_followers, get_following
from libs.browser import get_browser

##############################################################################################
# constants
##############################################################################################
PROFILE_OPT = "--profile"

FOLLOWER_LIMIT_OPT = "--follower-limit"
FOLLOWER_LIMIT = 100

RATIO_LIMIT_OPT = "--ratio-limit"
RATIO_LIMIT = 2

FILE_OPT = "--file"

MAX_OPT = "--max"
MAX = 10000

NUMBER_TRIES = 5

##############################################################################################
# functions
##############################################################################################
#load the users that were followed at any point in time
def load_were_followed_users(filename):
    followedUsers = []
    try:
        with open(filename, "r") as f:
            for line in f:
                followedUsers.append(line.strip())
    except:
        print("Error: unable to load followed users from file " + filename)
        return None
    return followedUsers

def main():
    ##############################################################################################
    # parse arguments
    ##############################################################################################
    botUsername = None
    botPassword = None
    targetUsername = None
    wereFollowed = None
    profile_path = None
    botProfile = None
    filename = None
    followerLimit = FOLLOWER_LIMIT
    ratioLimit = RATIO_LIMIT
    max = MAX
    try:
        argv = sys.argv[1:]

        botUsername = argv[0]
        botPassword = argv[1]

        targetUsername = argv[2]
        wereFollowed = argv[3]

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

        if MAX_OPT in argv:
            i = argv.index(MAX_OPT)
            max = int(argv[i + 1])
    except:
        print("Error: invalid arguments")
        return

    ##############################################################################################
    # main
    ##############################################################################################
    #load the users that were followed at any point in time
    wereFollowedUsers = load_were_followed_users(wereFollowed)
    if wereFollowedUsers == None:
        return
    
    botBrowser = get_browser(profile_path, botProfile)

    #login to bot account
    login(botBrowser, botUsername, botPassword)

    #get all my followers
    targetFollowers = get_followers(botBrowser, targetUsername, numberOfTries=NUMBER_TRIES)
    targetFollowing = get_following(botBrowser, targetUsername, numberOfTries=NUMBER_TRIES)

    #init list of new people to follow
    usersToFollow = []

    #file to store all the users to follow
    file = None
    if filename == None:
        file = sys.stdout
    else:
        try: 
            file = open(filename, "w")
        except:
            print("Error: unable to write to file " + filename)
            return

    
    #for each of target's followers, get their followers
    print("Getting followers of followers of " + targetUsername + "...")
    try:
        for follower in targetFollowers:
            try:
                theirFollowers = get_followers(botBrowser, follower, limit=2000, numberOfTries=NUMBER_TRIES)
            except:
                botBrowser = get_browser(profile_path, botProfile)
                login(botBrowser, botUsername, botPassword)
            print("got " + str(len(theirFollowers)) + " followers of " + follower)
            for f in theirFollowers:
                #if: they are me, or they are the bot, or they are already in my list, or they are already in my followers, skip
                if not f in targetFollowing and f != targetUsername and f != botUsername and f not in usersToFollow and f not in targetFollowers and f not in wereFollowedUsers:
                    file.write(f + "\n")
                    usersToFollow.append(f)
        print("successfully got " + str(len(usersToFollow)) + " users")
    except Exception as e:
        print(e)
        print("Error: only able to get " + str(len(usersToFollow)) + " users")
    finally:
        file.close()





if __name__ == "__main__":
    print("##############################################")
    main()
    print("##############################################")
