FROM python:3.10-slim-buster

WORKDIR /app

# Set timezone
ENV TZ=Europe/Berlin
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Install Firefox
RUN apt-get update && \
    apt-get install -y --no-install-recommends firefox-esr && \
    rm -rf /var/lib/apt/lists/*

# Install GeckoDriver
RUN apt-get update && \
    apt-get install -y --no-install-recommends wget unzip && \
    wget https://github.com/mozilla/geckodriver/releases/download/v0.30.0/geckodriver-v0.30.0-linux64.tar.gz && \
    tar -xvzf geckodriver-v0.30.0-linux64.tar.gz && \
    rm geckodriver-v0.30.0-linux64.tar.gz && \
    chmod +x geckodriver && \
    mv geckodriver /usr/local/bin/ && \
    apt-get remove -y wget unzip && \
    rm -rf /var/lib/apt/lists/*

# Install rsyslog
RUN apt-get update && apt-get install -y rsyslog
COPY rsyslog.conf /etc/rsyslog.conf
RUN chmod 644 /etc/rsyslog.conf

# Install cron
RUN apt-get update && apt-get install -y cron

# Install dos2unix
RUN apt-get update && apt-get install -y dos2unix

COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir --no-deps --force-reinstall pydantic==1.10.13

RUN touch /var/log/cron.log
COPY hello-cron /etc/cron.d/hello-cron
RUN dos2unix /etc/cron.d/hello-cron
RUN chmod 0644 /etc/cron.d/hello-cron
RUN crontab /etc/cron.d/hello-cron

CMD printenv | sed 's/^\(.*\)$/export \1/g' > /root/project_env.sh && service rsyslog start && cron && tail -f /var/log/cron.log