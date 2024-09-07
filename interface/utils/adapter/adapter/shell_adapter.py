
class ShellAdapter(object):
   def getInstances(self, prefix):
        return "ps -aux | grep 'recorder.sh' | awk '{ print $16 }' | sed -e '/^ *$/d'"

   def stopInstance(self, containerName):
        return "kill -int $(ps -aux | grep 'ffmpeg' | grep '" + containerName + "' | awk '{ print $2 }')"


   def startInstance(self, media_path, containerName, stream, limit_in_gb, imageName, UID, GID, resolution):
        return "/recorder/recorder.sh -u {} -c {} -r {} &".format(
            stream,
            containerName,
            resolution
        )
