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
            file = open(filename, "w")
        except:
            print("Error: unable to write to file " + filename)
            return

    botBrowser = get_browser(profile_path, botProfile)

    #login to bot account
    login(botBrowser, botUsername, botPassword)

    for follower in followers:
        following_count, follow_count = get_following(botBrowser, follower, numberOfTries=NUMBER_TRIES)
        ratio = 100
        if follow_count != 0:
            ratio = following_count / follow_count
        if following_count < followerLimit and ratio < ratioLimit:

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
    for follower in targetFollowers:
        theirFollowers = get_followers(botBrowser, follower, limit=1000, numberOfTries=NUMBER_TRIES)
        for f in theirFollowers:
            #if: they are me, or they are the bot, or they are already in my list, or they are already in my followers, skip
            if not f in targetFollowing and f != targetUsername and f != botUsername and f not in usersToFollow and not f in targetFollowers:
                file.write(f + "\n")
    file.close()

if __name__ == "__main__":
    main()
