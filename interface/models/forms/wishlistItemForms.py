from django.forms import ModelForm


from models.wishlistItem import WishlistItem

# Create the form class.
class WishlistItemForm(ModelForm):
     class Meta:
         model = WishlistItem
         exclude = ['pk', 'status', 'deleted']
