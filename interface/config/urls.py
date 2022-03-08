from django.urls import path

#views
from apps.frontend.main import views as mainViews
from apps.frontend.wishlist import views as wishlistViews


from django.urls import include, path

urlpatterns = [
    path('', mainViews.index, name='index'),

    path('wishlist/', wishlistViews.index, name='wishlist'),
    path('wishlist/add', wishlistViews.addWishlistItem, name='addwishlistItem'),
    path('wishlist/delete/<int:id>/', wishlistViews.deleteWishlistItem, name='deleteWishlistItem'),
]
