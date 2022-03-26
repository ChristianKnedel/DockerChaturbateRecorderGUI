class DockerAdapter(object):
   def getInstances(self, prefix):
        return "docker container ls --format '{{.Names}}' | grep '" + prefix + "'"

   def stopInstance(self, containerName):
        return "docker exec '{}' pkill -int ffmpeg &".format(containerName)

   def startInstance(self, media_path, containerName, title):
       return "docker run -d --rm -v {}:/output --name {} chatrubate-recorder /code/recorder.sh -u https://chaturbate.com/{}/ &".format(media_path, containerName, title)