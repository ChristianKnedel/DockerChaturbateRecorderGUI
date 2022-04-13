class DockerAdapter(object):
   def getInstances(self, prefix):
        return "docker container ls --format '{{.Names}}' | grep '" + prefix + "'"

   def stopInstance(self, containerName):
        return "docker exec '{}' pkill -int ffmpeg &".format(containerName)

   def startInstance(self, media_path, containerName, title, limit_in_gb, imageName, UID, GID):
        limit_in_kb = int( int( limit_in_gb ) * 1024 * 1024)
        return "docker run -d -e MAXIMUM_FOLDER_KB={} -e UID={} -e GID={} --rm -v {}:/output --name {} {} /code/recorder.sh -c {} &".format(
            limit_in_kb,
            UID,
            GID,
            media_path, 
            containerName, 
            imageName,
            title
        )
