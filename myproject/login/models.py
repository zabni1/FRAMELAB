from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    full_name = models.CharField(max_length=100)
    photo = models.ImageField(upload_to = 'photos', blank = True, null = True)
    active_status = models.BooleanField(default=False)


