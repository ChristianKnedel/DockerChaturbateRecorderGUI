# docker ChaturbateRecorder
Download Chaturbate video stream with  DockerChaturbateRecorderGUI! Try it out..

## Features
* watchlist/wishlist
  * automatically record Chaturbate live streams
* streams and folder size limis 
* stream/channel priority
* stream finder 
  * automatically search for streams


![alt text](https://github.com/terrorist-squad/DockerChaturbateRecorderGUI/blob/master/screens/3.png "record")



## Initial Setup
Find or make a directory you want your videos saved to then run: 
```
$ mkdir videos
$ chmod 755 -R videos
```
Save the full directory from above for later

## Install
After that I go to the docker-registry directory and download the "DockerChaturbateRecorderGUI"

It is suggested that you go and make a temp directory somewhere else before you start.
```
$ wget https://github.com/terrorist-squad/DockerChaturbateRecorderGUI/archive/refs/heads/master.zip
$ unzip master.zip 
$ cd DockerChaturbateRecorderGUI-master
```

for synology disk stations:
```
$ wget https://github.com/terrorist-squad/DockerChaturbateRecorderGUI/archive/refs/heads/master.zip
$ /bin/7z x master.zip
$ cd DockerChaturbateRecorderGUI-master
```

### 1.) build recorder
```
$ docker build -t chatrubate-recorder ./recorder/
```
If you prefer to use only the command line, then this call will help you:
``docker run -it -v /Users/CharlieScene/docker/chatrubate/input:/output chatrubate-recorder /code/recorder.sh -u https://chaturbate.com/triple_crystal/``


### 2.) build web app
```
$ docker-compose -f dev.yml build
```

### 3.) directory path
Change the 'ABSOLUTE_HOST_MEDIA'-path in dev.yml with the directory you got set at the start.

### 4.) start the container
```
$ docker-compose -f dev.yml up -d
```
After that I can call my recoder server with the IP of the server / diskstation and the assigned port 8002. Great! 
![alt text](https://github.com/terrorist-squad/DockerChaturbateRecorderGUI/blob/master/screens/3.png "record")

## Howto
### 1.) Copy the channnel url
To download video from chaturbate, no special tech knowledge is required. The process starts with chaturbate page link. Copy that link or channel name from the browser's address bar, then paste it into the white box above. And hit "Submit".
![alt text](https://github.com/terrorist-squad/DockerChaturbateRecorderGUI/blob/master/screens/1.png "Copy the channnel url")

### 2.) add the channel
Click on '+' and add the channel name as title
![alt text](https://github.com/terrorist-squad/DockerChaturbateRecorderGUI/blob/master/screens/2.png "add the channel")

### 3.) record
![alt text](https://github.com/terrorist-squad/DockerChaturbateRecorderGUI/blob/master/screens/3.png "record")

## Contributing
We welcome your contributions! Please refer to our contributing policies prior to submitting pull requests.
