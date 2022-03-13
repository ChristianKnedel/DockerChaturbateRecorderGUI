#base
from django.core.management.base import BaseCommand, CommandError

#utils
import os, subprocess
from django.template.defaultfilters import slugify

#models and manager
from models.wishlistItem import WishlistItem

class Command(BaseCommand):
    containerPrefix = 'cr_'

    def stopAllChannels(self):
        self.stdout.write(self.style.SUCCESS('stopAllChannels'))
        items = WishlistItem.unmanaged_objects.filter(status=1)
        for item in items:
            slug = slugify(item.title)
            containerName = str(self.containerPrefix + 'cr_' + slug)
            item.status = 0
            item.save()
            self.stopContainer(containerName)
        
    def stopContainer(self, containerName):
        self.stdout.write(self.style.SUCCESS('stop  '+ containerName))
        return subprocess.Popen(
            'docker exec ' + containerName +' pkill -int ffmpeg &', 
            shell=True, 
            stdout=subprocess.PIPE,
            close_fds=True
        )

    def deletedChannels(self):
        self.stdout.write(self.style.SUCCESS('deletedChannels'))
        deleted_items = WishlistItem.unmanaged_objects.filter(deleted=1).order_by('-prio')
        for item in deleted_items:
            slug = slugify(item.title)
            containerName = str(self.containerPrefix + 'cr_' + slug)
            self.stopContainer(containerName)
            item.delete()

    def checkChanels(self):
        self.stdout.write(self.style.SUCCESS('checkChanels'))
        containers = subprocess.run("docker container ls --format '{{.Names}}' | grep 'cr_'", shell=True, stdout=subprocess.PIPE).stdout.decode().splitlines()


        self.stdout.write(self.style.SUCCESS(str(containers)))

        if len(containers) >= int(os.environ['MAXIMUM_DOCKER_CONTAINER']):
            self.stdout.write(self.style.SUCCESS('maximum containers is reached'))
         
        else:
            items = WishlistItem.unmanaged_objects.filter(deleted=0).order_by('-prio')
            self.stdout.write(self.style.SUCCESS(str(len(items))))

            for item in items:

                slug = slugify(item.title)
                containerName = str(self.containerPrefix + 'cr_' + slug)
                self.stdout.write(self.style.SUCCESS('check  '+ containerName))

                if containerName in containers:
                    item.status = 1
                    item.save()
                    self.stdout.write(self.style.SUCCESS('run  '+ containerName))

                else:
                    container = subprocess.Popen(
                        'docker run -u 0 -d --rm -v ' + os.environ['HOST_MEDIA'] + ':/output --name ' + containerName +' chatrubate-recorder /code/recorder.sh -u https://chaturbate.com/' + item.title + '/ &', 
                        shell=True, 
                        stdout=subprocess.PIPE,
                        close_fds=True
                    )

                    if item.status == 1:
                        item.status = 0
                        item.save()

                    self.stdout.write(self.style.ERROR('dead  '+ containerName))

    def du(self, path):
        """disk usage in human readable format (e.g. '2,1GB')"""
        return subprocess.check_output(['du','-s', path]).split()[0].decode('utf-8')

    def handle(self, *args, **options):
        PROJECT_ROOT = os.path.realpath(os.path.dirname(__file__))
        videoDir = os.path.join(PROJECT_ROOT, '../../../media/videos')

        containers = str(self.du(videoDir))
        if int(self.du(videoDir)) > ( int(os.environ['MAXIMUM_FOLDER_GB']) +11 * 1024 * 1024):
            self.stdout.write(self.style.SUCCESS('maximum size is reached'))
            self.stopAllChannels()

        else:
            self.stdout.write(self.style.SUCCESS('ok'))
            self.checkChanels()

        self.deletedChannels()

