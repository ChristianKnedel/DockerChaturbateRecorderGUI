from django.db import models


from models.managers.wishlistItemManager import WishlistItemManager

class WishlistItem(models.Model):

    # META CLASS
    class Meta:
        app_label = 'main'
        db_table = 'wishlist_item'

    TYPE = (
      ('f', 'filter'),
      ('c', 'channel')
    )

    GENDER = (
      ('a', 'ALL'),
      ('w', 'WOMEN'),
      ('m', 'MEN'),
      ('c', 'COUPLES'),
      ('t', 'TRANS')
    )

    PRIO = (
      (1, 1),
      (2, 2),
      (3, 3),
      (4, 4),
      (5, 5),
      (6, 6),
      (7, 7),
      (8, 8),
      (9, 9),
    )


    title = models.CharField(db_index=True, unique=True, max_length=255)
    gender = models.CharField(max_length=1, choices=GENDER, default='a')
    type = models.CharField(max_length=1, choices=TYPE, default='c')
    prio = models.IntegerField(choices=PRIO, default=1)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    deleted = models.BooleanField(default=False, blank=False)
    status = models.BooleanField(default=False, blank=False)

    # MANAGERS
    unmanaged_objects = models.Manager()
    managed_objects = WishlistItemManager()