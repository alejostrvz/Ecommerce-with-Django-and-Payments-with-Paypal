from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.FloatField()
    description = models.TextField()
    image = models.CharField(max_length=200)
    image2 = models.CharField(max_length=200, null=True)
    image3 = models.CharField(max_length=200, null=True)

    
    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=50)
    products = models.ManyToManyField(Product, related_name="categories")

    def __str__(self):
        return self.name

class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL,null=True)
    content = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL,null=True)
