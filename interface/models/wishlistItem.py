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

    RESOLUTION = (
      ('7680:4320', '8K / 8K UHD'),
      ('5120:2880', '5K'),
      ('4096:2160', '4K'),
      ('3840:2160', '2160p / UHD'),
      ('2560:1440', '1440p / QHD / QuadHD / WQHD'),
      ('2048:1080', '2K'),
      ('1920:1080', '1080p / Full HD / FHD'),
      ('1280:720', '720p / HD'),
      ('960:540', '540p / qHD'),
      ('640:480', '480p'),
    )


    REGION = (
      ('all', 'ALL'),
      ('NA', 'North American Cams'),
      ('O', 'Other Region Cams'),
      ('ER', 'Europe/Russian Cams'),
      ('AS', 'Asian Cams'),
      ('SA', 'South American Cams')
    )

    AGE = (
      ('all', 'ALL'),
      ('teen', 'Teen Cams (18+)'),
      ('18-21', '18 to 21 Cams'),
      ('20-30', '20 to 30 Cams'),
      ('30-50', '30 to 50 Cams'),
      ('50-100', 'Mature Cams (50+)')
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

    resolution = models.CharField(max_length=12, choices=RESOLUTION, default='1920:1080')
    type = models.CharField(max_length=1, choices=TYPE, default='c')
    title = models.CharField(db_index=True, unique=True, max_length=255)
    gender = models.CharField(max_length=1, choices=GENDER, default='a')
    age = models.CharField(max_length=10, choices=AGE, default='all')
    region = models.CharField(max_length=100, choices=REGION, default='all')
    prio = models.IntegerField(choices=PRIO, default=1)

    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    deleted = models.BooleanField(default=False, blank=False)
    status = models.BooleanField(default=False, blank=False)

    # MANAGERS
    unmanaged_objects = models.Manager()
    managed_objects = WishlistItemManager()
