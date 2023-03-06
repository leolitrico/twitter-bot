#!/bin/bash

#install chrome
curl -sS -o - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add
bash -c "echo 'deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main' >> /etc/apt/sources.list.d/google-chrome.list"
apt -y update 
apt -y install google-chrome-stable
	
wget https://chromedriver.storage.googleapis.com/${google-chrome --version | grep -iE "[0-9.]{10,20}"}/chromedriver_linux64.zip 
unzip chromedriver_linux64.zip 
mv chromedriver /usr/bin/chromedriver 
chown root:root /usr/bin/chromedriver 
chmod +x /usr/bin/chromedriver
	
#install pip
apt install -y python3-pip

#install selenium
pip3 install selenium