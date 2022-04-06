FROM ubuntu:latest

ENV MAXIMUM_FOLDER_KB=1048576
ENV TZ 'Europe/Berlin'
ENV UID 0
ENV GID 0

RUN echo $TZ > /etc/timezone && \
apt-get update && apt-get install -y tzdata && \
rm /etc/localtime && \
ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && \
dpkg-reconfigure -f noninteractive tzdata

# Copy the rest of the applicaion's code
ADD code /code
WORKDIR /code

RUN useradd -ms /bin/bash recorder

#install packages
RUN apt-get update && apt-get install -y \
ffmpeg \
curl \
cron

RUN mkdir /output/
RUN chmod 755 /code/recorder.sh
RUN chmod 755 /code/cron.sh

WORKDIR /code

#cleanup
RUN apt-get clean


#install cronjobs
# Copy cron file to the cron.d directory
COPY cron-root /etc/cron.d/cron

# Give execution rights on the cron job
RUN chmod 0644 /etc/cron.d/cron &&\
 crontab -u root /etc/cron.d/cron &&\
 touch /var/log/cron.log

CMD /code/recorder.sh
