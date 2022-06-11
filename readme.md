# docker ChaturbateRecorder
Download Chaturbate video stream with  DockerChaturbateRecorderGUI! Try it out..
Docker-Hub: https://hub.docker.com/repository/docker/chrisknedel/chatrubate-recorder-gui

## Features
* watchlist/wishlist
  * automatically record Chaturbate live streams
* streams and folder size limits 
* stream/channel priority
* stream finder 
  * automatically search for streams
* There are different download adapters:
  * DockerAdapter = Each download runs in its own container
  * ShellAdapter = Everything takes place in a container
  * KubernetesAdapter = Is still under development, branch https://github.com/terrorist-squad/DockerChaturbateRecorderGUI/tree/kubernetes-adapter
* i18n = Is still under development, branch https://github.com/terrorist-squad/DockerChaturbateRecorderGUI/tree/i18n
* stream resolution/Capture Quality 

## run 
```
$ docker run -it --rm -v /Users/christianknedel/videos:/code/database -v /var/run/docker.sock:/var/run/docker.sock -p 8002:8000 -e TZ="Europe/Berlin" -e ABSOLUTE_HOST_MEDIA="/Users/christianknedel/videos/" -e COMMAND_ADAPTER='DockerAdapter' -e CONTAINER_PREFFIX='cr_' -e RECORDER_IMAGE='chrisknedel/chatrubate-recorder:2.0' chrisknedel/chatrubate-recorder-gui:2.0
```
Example stable_adapter_docker.yml for DockerChaturbateRecorderGUI:
```
version: '2'

services:    
  app:
    image: chrisknedel/chatrubate-recorder-gui:2.0
    container_name: recorder_app
    restart: always
    environment:
      TZ: "Europe/Berlin"
      ABSOLUTE_HOST_MEDIA: "/Users/christianknedel/videos/"
      LIMIT_MAXIMUM_FOLDER_GB: 20 #or "0" to disable this limit
      LIMIT_MAXIMUM_DOWNLOADS: 10 #or "0" to disable this limit
      COMMAND_ADAPTER: 'DockerAdapter'
      CONTAINER_PREFFIX: 'cr_'
      RECORDER_IMAGE: 'chrisknedel/chatrubate-recorder:2.0'
      USER_UID: 0
      USER_GID: 0
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
      - /Users/christianknedel/videos:/code/database
    ports:
      - "8002:8000"
```

## build from source
### Initial Setup
Find or make a directory you want your videos saved to then run: 
```
$ mkdir videos
$ chmod 755 -R videos
```
Save the full directory from above for later

### Install
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

#### 1.) build recorder
```
$ docker build -t chatrubate-recorder ./recorder/
```
If you prefer to use only the command line, then this call will help you:
``docker run -it -v /Users/CharlieScene/docker/chatrubate/input:/code/videos/ chatrubate-recorder /code/recorder.sh -u https://chaturbate.com/triple_crystal/ -c video_triple_crystal``


#### 2.) build web app
```
$ docker-compose -f dev_adapter_docker.yml build
```

#### 3.) directory path
Change the 'ABSOLUTE_HOST_MEDIA'-path in dev_adapter_docker.yml with the directory you got set at the start.

#### 4.) start the container
```
$ docker-compose -f dev_adapter_docker.yml up -d
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
Below is the list of awesome people supporting the development of DockerChaturbateRecorderGUI. 
You can also become one of them. [terrorist-squad](https://www.patreon.com/terrorist_squad)
- [Dethkiller15](https://github.com/Dethkiller15)
- [Nor882](https://github.com/Nor882)
- [meddle99](https://github.com/meddle99)
