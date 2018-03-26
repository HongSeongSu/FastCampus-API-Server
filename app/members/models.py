from django.contrib.auth.models import AbstractUser, UserManager as DjangoUserManager


class UserManager(DjangoUserManager):
    pass


class User(AbstractUser):
    objects = UserManager()
