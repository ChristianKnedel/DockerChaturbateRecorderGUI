class DockerAdapter(object):
   def getInstances(self, prefix):
        return "docker container ls --format '{{.Names}}' | grep '" + prefix + "'"

   def stopInstance(self, containerName):
        return "docker exec '{}' pkill -int ffmpeg &".format(containerName)

   def startInstance(self, media_path, containerName, stream, limit_in_gb, imageName, UID, GID, resolution, recording_limit):
        return "docker run -d -e LIMIT_MAXIMUM_FOLDER_GB={} -e UID={} -e GID={} --rm -v {}:/code/videos/ --name {} {} /code/recorder.sh -u {} -c {} -r {} -l {} &".format(
            limit_in_gb,
            UID,
            GID,
            media_path, 
            containerName, 
            imageName,
            stream,
            containerName,
            resolution,
            recording_limit
        )
