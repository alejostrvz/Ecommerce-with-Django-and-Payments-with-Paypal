from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Wishlist, WishlistItem
from products.models import Product

@login_required(login_url='login_user')
def get_whishlist(request):
    if request.user.is_authenticated:
        products = request.user.wishlist.products.all()

        return render(request, "user/wishlist.html", {
            "products": products
        })
    return redirect("/")
@login_required(login_url='login_user')
def add_to_wishlist(request, idProduct):
    if request.user.is_authenticated:
        wishlistItem = WishlistItem()
        wishlistItem.product = Product.objects.get(pk=idProduct)
        wishlistItem.amount = 1
        wishlistItem.wishlist = request.user.wishlist

        wishlistItem.save()

    return redirect("/")
@login_required(login_url='login_user')
def delete_from_wishlist(request, id_wishlist_item):
    if request.user.is_authenticated:
        wishlist_item = WishlistItem.objects.get(pk=id_wishlist_item)
        if wishlist_item.wishlist.user == request.user:
            wishlist_item.delete()

            return redirect("/wishlist")

    return redirect("/")