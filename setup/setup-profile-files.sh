#!/bin/bash
# This script will create necessary files and directories for the setup
# Arguments: 
# - $1 = username

mkdir ~/twitter-server/$1
touch ~/twitter-server/$1/follow-all.txt
touch ~/twitter-server/$1/follow-filtered.txt
touch ~/twitter-server/$1/following.txt
touch ~/twitter-server/$1/were-followed.txt