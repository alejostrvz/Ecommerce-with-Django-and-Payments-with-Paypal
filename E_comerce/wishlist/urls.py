from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_whishlist, name="wishlist"),
    path('add/<int:idProduct>', views.add_to_wishlist, name="add_to_wishlist"),
    path('delete/<int:id_wishlist_item>', views.delete_from_wishlist, name="delete_from_wishlist"),
]
