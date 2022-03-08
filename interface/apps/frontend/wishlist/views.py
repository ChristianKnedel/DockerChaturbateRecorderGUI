
#utils
import simplejson as json
from django.shortcuts import render, redirect

from django.http import HttpResponseRedirect, HttpResponse, Http404

from models.wishlistItem import WishlistItem

from models.forms.wishlistItemForms import WishlistItemForm


def index(request):

    items = list(WishlistItem.managed_objects.getAll())

    return HttpResponse(
        json.dumps(
            items, 
            indent=4, 
            sort_keys=True, 
            default=str
        ), 
        content_type='application/json'
    )

def addWishlistItem(request):
    

    if request.method == 'POST':
        form = WishlistItemForm(request.POST)

        if form.is_valid():
            newItem = form.save()


            return redirect('/')
    else:
        form = WishlistItemForm()


    return render(
        request,
        'frontend/wishlist/addwishlistItem.html',
        {
            'form': form
        }
    )

def deleteWishlistItem(request, id):

    item = WishlistItem.managed_objects.getByID(id)
    item.deleted = 1
    item.save()

    return redirect('/')
