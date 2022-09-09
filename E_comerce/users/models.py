from django.db import models
#Import models
from django.contrib.auth.models import AbstractUser
#Import from manager

# Create your models here.
class User(AbstractUser):
    #Options
    GENDER_CHOICES = (
        ('M','Masculino'),
        ('F','Femenino'),
        ('O','Otros'),
    )
    #Relations
    #Fields
    isEmailValid = models.BooleanField(default=False)
    emailValidationUUID = models.CharField(max_length=50, null=True)
    email = models.EmailField(unique=True)
    names = models.CharField(max_length=50,blank=True)
    last_names = models.CharField(max_length=50,blank=True)
    gender = models.CharField( max_length=1,choices=GENDER_CHOICES,blank=True)
    age = models.PositiveBigIntegerField(default=0)
    country = models.CharField(max_length=20,blank=True)
    direction = models.CharField(max_length=20,blank=True)
    #required
    #Manager

