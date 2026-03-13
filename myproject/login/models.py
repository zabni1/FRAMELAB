from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    full_name = models.CharField(max_length=100)
    photo = models.ImageField(upload_to = 'photos', blank = True, null = True)

