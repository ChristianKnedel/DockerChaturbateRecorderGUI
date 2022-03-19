#base
from django.core.management.base import BaseCommand, CommandError

#utils
import os, subprocess
import re
from django.template.defaultfilters import slugify

#models and manager
from models.wishlistItem import WishlistItem

class Command(BaseCommand):
    containerPrefix = 'cr_'

    def stopAllChannels(self):
        self.stdout.write(self.style.SUCCESS('stopAllChannels'))
        items = WishlistItem.unmanaged_objects.filter(type='c', status=1)
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
        deleted_items = WishlistItem.unmanaged_objects.filter(type='c', deleted=1).order_by('-prio')
        for item in deleted_items:
            slug = slugify(item.title)
            containerName = str(self.containerPrefix + 'cr_' + slug)
            self.stopContainer(containerName)
            item.delete()

    def getContainer(self):
        containers = subprocess.run("docker container ls --format '{{.Names}}' | grep 'cr_'", shell=True, stdout=subprocess.PIPE).stdout.decode().splitlines()
        return containers


    def checkChannels(self):
        self.stdout.write(self.style.SUCCESS('checkFilter'))
        containers = self.getContainer()

        items = WishlistItem.unmanaged_objects.filter(type='c', deleted=0).order_by('-prio')
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
                if len(containers) < int(os.environ['MAXIMUM_DOCKER_CONTAINER']):

                    container = subprocess.Popen(
                        'docker run -u 0 -d --rm -v ' + os.environ['ABSOLUTE_HOST_MEDIA'] + ':/output --name ' + containerName +' chatrubate-recorder /code/recorder.sh -u https://chaturbate.com/' + item.title + '/ &', 
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
        

    def checkFilter(self):
        self.stdout.write(self.style.SUCCESS('checkFilter'))
        containers = self.getContainer()

        delta = int(os.environ['MAXIMUM_DOCKER_CONTAINER']) - len(containers)
        self.stdout.write(self.style.ERROR('delta  '+ str(delta)))

        if delta == 0:
            return False
        
        items = WishlistItem.unmanaged_objects.filter(type='f', deleted=0).order_by('-prio')
            
        for item in items:

            self.stdout.write(self.style.SUCCESS('title' + item.title))
            self.stdout.write(self.style.SUCCESS('age' + item.age))

            url = 'https://chaturbate.com/'

            if item.age != 'all':
                url = 'https://chaturbate.com/' + item.age  + '-cams/'
            elif item.region != 'all':
                url = 'https://chaturbate.com/' + item.region  + '-cams/'
            else:
                url = 'https://chaturbate.com/tag/' + item.title + '/'
   

            if item.region == 'all' and item.age == 'all':
                if item.gender == 'w':
                    url += 'w/'
                elif item.gender == 'm':
                    url += 'm/'
                elif item.gender == 'c':
                    url += 'c/'
                elif item.gender == 't':
                    url += 't/'
            else:
                if item.gender == 'w':
                    url += 'female/'
                elif item.gender == 'm':
                    url += 'male/'
                elif item.gender == 'c':
                    url += 'couple/'
                elif item.gender == 't':
                    url += 'trans/'

            channels = subprocess.run(
                "curl " + url + " | grep 'data-room' | grep -v 'no_select' | uniq", 
                shell=True, 
                stdout=subprocess.PIPE
            ).stdout.decode()

            for channel in re.findall(r'(?<=<a href="/)[^/"]*', channels):
                self.stdout.write(self.style.SUCCESS( 'create wishlist item ' + channel))


                if delta == 0:
                    return False

                WishlistItem.unmanaged_objects.get_or_create(
                    title = channel,
                    type = 'c',
                    prio = item.prio
                )

                delta = delta-1

    def deleteFilter(self):
        WishlistItem.unmanaged_objects.filter(type='f', deleted=1).delete()

    def handle(self, *args, **options):
        PROJECT_ROOT = os.path.realpath(os.path.dirname(__file__))
        videoDir = os.path.join(PROJECT_ROOT, '../../../media/videos')

        containers = str(self.du(videoDir))
        if int(self.du(videoDir)) > ( int(os.environ['MAXIMUM_FOLDER_GB']) +11 * 1024 * 1024):
            self.stdout.write(self.style.SUCCESS('maximum size is reached'))
            self.stopAllChannels()

        else:
            self.stdout.write(self.style.SUCCESS('ok'))
            self.checkChannels()

        self.deletedChannels()
        self.checkFilter()
        self.deleteFilter()
