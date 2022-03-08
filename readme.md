

## Install
### 1.) build recoder
```
$ docker build -t chatrubate-recorder ./recorder/
```
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
![alt text](https://github.com/terrorist-squad/DockerChaturbateRecorderGUI/blob/master/screens/1.png "Copy the channnel url")

### 2.) add the channel
![alt text](https://github.com/terrorist-squad/DockerChaturbateRecorderGUI/blob/master/screens/2.png "add the channel")

### 3.) record
![alt text](https://github.com/terrorist-squad/DockerChaturbateRecorderGUI/blob/master/screens/3.png "record")
