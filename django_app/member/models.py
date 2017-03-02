from django.contrib.auth.models import AbstractUser, UserManager


class MyUserManager(UserManager):
    pass


class MyUser(AbstractUser):
    objects = MyUserManager()
