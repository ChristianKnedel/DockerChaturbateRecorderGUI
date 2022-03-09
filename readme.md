# docker ChaturbateRecorder
ChaturbateRecorder records any video stream from Chaturbate
![alt text](https://github.com/terrorist-squad/DockerChaturbateRecorderGUI/blob/master/screens/3.png "record")


## Install
### 1.) build recoder
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
Change the 'HOST_MEDIA'-path in dev.yml

### 4.) start the container
```
$ docker-compose -f dev.yml up
```

## Howto
### 1.) Copy the channnel url
copy the channel name / slug
![alt text](https://github.com/terrorist-squad/DockerChaturbateRecorderGUI/blob/master/screens/1.png "Copy the channnel url")

### 2.) add the channel
Click on '+' and add the channel name as title
![alt text](https://github.com/terrorist-squad/DockerChaturbateRecorderGUI/blob/master/screens/2.png "add the channel")

### 3.) record
![alt text](https://github.com/terrorist-squad/DockerChaturbateRecorderGUI/blob/master/screens/3.png "record")

## Contributing
We welcome your contributions! Please refer to our contributing policies prior to submitting pull requests.
