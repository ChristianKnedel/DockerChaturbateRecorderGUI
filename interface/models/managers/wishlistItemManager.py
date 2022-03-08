#model core
from django.db import models


from django.utils.dateformat import format

class WishlistItemManager(models.Manager):


    def getAll(self):
        return self.filter(deleted=0).order_by('-prio').values('id', 'title', 'prio', 'type', 'gender', 'status', 'updated_at')


    def getByID(self, id):
        return self.get(pk=id)

