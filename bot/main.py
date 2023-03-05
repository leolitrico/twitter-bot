# Description: This script will find users that are likely to follow a target user back
# Arguments:
# botUsername: username of the bot account
# botPassword: password of the bot account
# targetUsername: username of the target account
# Options:
# --profile: use a chrome profile for the bot (--profile path profileName)
# --follower-limit: max number of followers an eligible user can have to follow them
# --ratio-limit: limit the ratio of followers to following an eligible user can have to follow them
# --file: file to store the users in


import sys
import pathlib
sys.path.append(str(pathlib.Path(__file__).parent.absolute()) + "/../")

from libs.twitter import login, get_followers, get_follow_count, get_following
from libs.browser import get_browser

##############################################################################################
# constants
##############################################################################################
PROFILE_OPT = "--profile"

FOLLOWER_LIMIT_OPT = "--follower-limit"
FOLLOWER_LIMIT = 30

RATIO_LIMIT_OPT = "--ratio-limit"
RATIO_LIMIT = 3

FILE_OPT = "--file"

NUMBER_TRIES = 100

def main():
    ##############################################################################################
    # parse arguments
    ##############################################################################################
    botUsername = None
    botPassword = None
    targetUsername = None
    profile_path = None
    botProfile = None
    filename = None
    followerLimit = FOLLOWER_LIMIT
    ratioLimit = RATIO_LIMIT
    try:
        argv = sys.argv[1:]

        botUsername = argv[0]
        botPassword = argv[1]

        targetUsername = argv[2]

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
    for follower in targetFollowers:
        theirFollowers = get_followers(botBrowser, follower, limit=1000, numberOfTries=NUMBER_TRIES)
        for f in theirFollowers:
            #if: they are me, or they are the bot, or they are already in my list, or they are already in my followers, skip
            if not f in targetFollowing and f != targetUsername and f != botUsername and f not in usersToFollow and not f in targetFollowers:
                following, followers = get_follow_count(botBrowser, f, numberOfTries=NUMBER_TRIES)
                #check that they have a high probability of following back
                if following / followers > ratioLimit and followers < followerLimit:
                    usersToFollow.append(f)
                    file.write(f + "\n")
    file.close()

if __name__ == "__main__":
    main()
