# Use the official lightweight Python image.
# https://hub.docker.com/_/python
FROM python:3.10

# Allow statements and log messages to immediately appear in the Knative logs
ENV PYTHONUNBUFFERED True

# Copy local code to the container image.
ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./

# Install production dependencies.
# RUN pip install --no-cache-dir -r requirements.txt
# RUN pip install selenium==4.4.3
# RUN pip install webdriver-manager
# RUN pip install cloudscraper
# RUN pip install google-cloud-storage

RUN pip install gunicorn
RUN pip install google-cloud-bigquery
RUN pip install Flask-RESTful
RUN pip install pandas
RUN pip install pandas-gbq
RUN pip install fake-useragent
RUN pip install requests-html
RUN pip install requests
RUN pip install pendulum
RUN pip install gspread
RUN pip install oauth2client
RUN pip install bs4
RUN pip install --no-cache-dir --upgrade pip

# Install manually all the missing libraries
RUN apt-get update
RUN apt-get install wget

# Install Chrome
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN dpkg -i google-chrome-stable_current_amd64.deb; apt-get -fy install

RUN apt-get update && apt-get install -y gconf-service libasound2 libatk1.0-0 libc6 libcairo2 libcups2 \
libdbus-1-3 libexpat1 libfontconfig1 libgcc1 libgconf-2-4 libgdk-pixbuf2.0-0 libglib2.0-0 libgtk-3-0 \
libnspr4 libpango-1.0-0 libpangocairo-1.0-0 libstdc++6 libx11-6 libx11-xcb1 libxcb1 libxcomposite1 \
libxcursor1 libxdamage1 libxext6 libxfixes3 libxi6 libxrandr2 libxrender1 libxss1 libxtst6 ca-certificates \
fonts-liberation libnss3 lsb-release xdg-utils 

# libappindicator1
# Run the web service on container startup. Here we use the gunicorn
# webserver, with one worker process and 8 threads.
# For environments with multiple CPU cores, increase the number of workers
# to be equal to the cores available.
# Timeout is set to 0 to disable the timeouts of the workers to allow Cloud Run to handle instance scaling.

CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 app:app