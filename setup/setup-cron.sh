#!/bin/bash
# This script setups the cron jobs
# Arguments: 
# - $1 = username
# - $2 = password
# - $3 = botUsername
# - $4 = botPassword
# - $5 = chrome profile path
# - $6 = cron base time
# - $7 = populate date

POPULATE_TIME = ($6 + 13)%24
FOLLOW_MORNING_TIME = $6 + 1
FOLLOW_AFTERNOON_TIME = ($6 + 13)%24
FILTER_TIME = $6

0 $POPULATE_TIME $7 * * python3 ~/twitter-bot/bot/populate.py $3 $4 $1 ~/twitter-server/$1/were-followed.txt --profile $5 $3 --file ~/twitter-server/$1/follow-all.txt
0 $FILTER_TIME * * * python3 ~/twitter-bot/bot/filter.py $3 $4 ~/twitter-server/$1/follow-all.txt 40 --file ~/twitter-server/$1/follow-filtered.txt --profile $5 $3
0 $FOLLOW_MORNING_TIME * * * python3 ~/twitter-bot/personal/main.py $1 $2 10 ~/twitter-server/$1/follow-filtered.txt ~/twitter-server/$1/following.txt ~/twitter-server/$1/were-followed.txt --profile $5 $1
0 $FOLLOW_AFTERNOON_TIME * * * python3 ~/twitter-bot/personal/main.py $1 $2 10 ~/twitter-server/$1/follow-filtered.txt ~/twitter-server/$1/following.txt ~/twitter-server/$1/were-followed.txt --profile $5 $1