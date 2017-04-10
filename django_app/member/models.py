from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models


class MyUserManager(UserManager):
    pass


class MyUser(AbstractUser):
    objects = MyUserManager()


class CeleryTest(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
