from django.db import models
from products.models import Product
from django.contrib.auth import get_user_model

User = get_user_model()


class Wishlist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="wishlist")
    #products = models.ManyToOneRel(field="CartItem", field_name="id", to="id" )


# Create your models here.
class WishlistItem(models.Model):
    amount = models.IntegerField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    wishlist = models.ForeignKey(Wishlist, on_delete=models.CASCADE, related_name="products")