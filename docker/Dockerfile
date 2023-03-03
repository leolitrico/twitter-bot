FROM ubuntu:22.04

RUN apt update && apt -y upgrade

#install prerequisites
RUN apt install -y unzip xvfb libxi6 libgconf-2-4

#install chrome
RUN curl -sS -o - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add && \
	bash -c "echo 'deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main' >> /etc/apt/sources.list.d/google-chrome.list" && \
	apt -y update && \ 
	apt -y install google-chrome-stable
	
RUN wget https://chromedriver.storage.googleapis.com/${google-chrome --version | grep -iE "[0-9.]{10,20}"}/chromedriver_linux64.zip && \
	unzip chromedriver_linux64.zip && \
	mv chromedriver /usr/bin/chromedriver && \
	chown root:root /usr/bin/chromedriver && \
	chmod +x /usr/bin/chromedriver
	
#install pip
RUN apt install -y python3-pip

#install requirements
COPY ./requirements.txt /tmp/requirements.txt
RUN pip3 install -r /tmp/requirements.txt
