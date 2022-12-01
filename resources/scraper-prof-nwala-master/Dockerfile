FROM python:3.7-stretch

LABEL maintainer="Alexander Nwala <anwala@cs.odu.edu>"

# set display port to avoid crash
ENV DISPLAY=:99

WORKDIR /home/scraper

# install google chrome
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
	&& sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list' \
	&& apt-get -y update && apt-get install -y google-chrome-stable

# install chromedriver
RUN apt-get install -yqq unzip \
	&& wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip \
	&& unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/ \ 
	&& rm /tmp/chromedriver.zip

# upgrade pip & install selenium
COPY requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

COPY . /home/scraper
RUN chmod +x ./scraper/scraper.py && chmod +x /usr/local/bin/chromedriver
ENTRYPOINT ["./scraper/scraper.py"]