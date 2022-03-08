#base
from django.core.management.base import BaseCommand, CommandError

#utils
import os, subprocess
from django.template.defaultfilters import slugify

#models and manager
from models.wishlistItem import WishlistItem

class Command(BaseCommand):
    help = 'import Catlogue'
    containerPrefix = 'cr_'


    
    def handle(self, *args, **options):

        deleted_items = WishlistItem.unmanaged_objects.filter(deleted=1).order_by('-prio')
        for item in deleted_items:

            slug = slugify(item.title)
            containerName = str(self.containerPrefix + 'cr_' + slug)
          

            container = subprocess.Popen(
                'docker stop ' + containerName +' &', 
                 shell=True, 
                 stdout=subprocess.PIPE,
                 close_fds=True
            )




        items = WishlistItem.unmanaged_objects.filter(deleted=0).order_by('-prio')

        containers = subprocess.run("docker container ls --format '{{.Names}}' | grep 'cr_'", shell=True, stdout=subprocess.PIPE).stdout.decode().splitlines()

        for item in items:

            slug = slugify(item.title)
            containerName = str(self.containerPrefix + 'cr_' + slug)
          

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
   
            