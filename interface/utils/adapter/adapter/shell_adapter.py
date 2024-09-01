
class ShellAdapter(object):
   def getInstances(self, prefix):
        return "ps -aux | grep 'recorder.sh' | awk '{ print $16 }' | sed -e '/^ *$/d'"

   def stopInstance(self, containerName):
        return "kill -int $(ps -aux | grep 'ffmpeg' | grep '" + containerName + "' | awk '{ print $2 }')"


   def startInstance(self, media_path, containerName, title, limit_in_gb, imageName, UID, GID, resolution):
        # Form the URL using the title
        url = f"https://chaturbate.com/{title}/"

        # Fetch the HTML content from the URL
        response = requests.get(url)
        html_content = response.text

        # Find all occurrences of URLs ending with .m3u8
        streams = re.findall(r'https://[a-zA-Z0-9.+-_:/]*\.m3u8', html_content)

        if urls:
            stream = re.sub(r'\\u([0-9A-Fa-f]{4})', lambda m: chr(int(m.group(1), 16)), streams[0])
            # Return the Docker command if .m3u8 URLs are found
            FoundStreamVar = "Found stream for {}.".format(
                title
            )
            # print(FoundStreamVar)
            return "/recorder/recorder.sh -u {} -c {} -r {} &".format(
                stream,
                containerName,
                resolution
            )
        else:
            StreamNotFoundVar = "No stream found for {}.".format(
                title
            )
            # print(StreamNotFoundVar)
            
            return "echo No Stream found for title {}. Skipping. > /dev/null 2>&1".format(
                title
            )
