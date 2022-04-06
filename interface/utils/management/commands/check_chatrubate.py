#base
from django.core.management.base import BaseCommand, CommandError

from utils.adapter.adapter_factory import AdapterFactory

#utils
import os, subprocess
import re
from django.template.defaultfilters import slugify

#models and manager
from models.wishlistItem import WishlistItem

class Command(BaseCommand):
    containerPrefix = os.environ['CONTAINER_PREFFIX']
    adapter_factory = AdapterFactory()

    def stopAllChannels(self):
        items = WishlistItem.unmanaged_objects.filter(type='c', status=1)
        for item in items:
            slug = slugify(item.title)
            containerName = str(self.containerPrefix + slug)
            item.status = 0
            item.save()
            self.stopContainer(containerName)



        
    def stopContainer(self, containerName):

        return subprocess.Popen(
            self.adapter_factory.create_adapter(os.environ['COMMAND_ADAPTER']).stopInstance(containerName), 
            shell=True, 
            stdout=subprocess.PIPE,
            close_fds=True
        )

    def deletedChannels(self):
        deleted_items = WishlistItem.unmanaged_objects.filter(type='c', deleted=1).order_by('-prio')
        for item in deleted_items:
            slug = slugify(item.title)
            containerName = str(self.containerPrefix + slug)
            self.stopContainer(containerName)
            item.delete()

    def getContainer(self):
        containers = subprocess.run(
            self.adapter_factory.create_adapter(os.environ['COMMAND_ADAPTER']).getInstances(self.containerPrefix), 
            shell=True, 
            stdout=subprocess.PIPE
        ).stdout.decode().splitlines()
        return containers


    def checkChannels(self):
        containers = self.getContainer()

        items = WishlistItem.unmanaged_objects.filter(type='c', deleted=0).order_by('-prio')

        for item in items:

            slug = slugify(item.title)
            containerName = str(self.containerPrefix + slug)

            if containerName in containers:
                item.status = 1
                item.save()

            else:
                if int(os.environ['LIMIT_MAXIMUM_DOCKER_CONTAINER']) != 0 and len(containers) > int(os.environ['LIMIT_MAXIMUM_DOCKER_CONTAINER']):
                    break

                container = subprocess.Popen(
                    self.adapter_factory.create_adapter(os.environ['COMMAND_ADAPTER']).startInstance(
                        os.environ['ABSOLUTE_HOST_MEDIA'], 
                        containerName, 
                        item.title,
                        int(os.environ['LIMIT_MAXIMUM_FOLDER_GB']),
                        os.environ['RECORDER_IMAGE'],
                        os.environ['USER_UID'],
                        os.environ['USER_GID']
                    ),
                    shell=True, 
                    stdout=subprocess.PIPE,
                    close_fds=True
                )

                if item.status == 1:
                    item.status = 0
                    item.save()

    def checkFilter(self):
        containers = self.getContainer()
        delta = 1024

        if int(os.environ['LIMIT_MAXIMUM_DOCKER_CONTAINER']) != 0: 
            delta = int(os.environ['LIMIT_MAXIMUM_DOCKER_CONTAINER']) - len(containers)

        if delta == 0:
            return False
        
        items = WishlistItem.unmanaged_objects.filter(type='f', deleted=0).order_by('-prio')
            
        for item in items:
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

        self.checkChannels()

        self.deletedChannels()
        self.checkFilter()
        self.deleteFilter()
