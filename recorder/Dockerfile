FROM ubuntu:latest

ENV TZ 'Europe/Berlin'
RUN echo $TZ > /etc/timezone && \
apt-get update && apt-get install -y tzdata && \
rm /etc/localtime && \
ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && \
dpkg-reconfigure -f noninteractive tzdata

# Copy the rest of the applicaion's code
ADD . /code
WORKDIR /code

RUN useradd -ms /bin/bash recorder

#install packages
RUN apt-get update && apt-get install -y \
ffmpeg \
curl

RUN apt-get clean
RUN mkdir /output/
RUN chown -R recorder:recorder /output/
USER recorder


WORKDIR /code

# Run the app
CMD ["/code/bash/recorder.sh"]
