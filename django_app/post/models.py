from django.conf import settings
from django.db import models


class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    title = models.CharField(max_length=100)
    img_cover = models.ImageField(upload_to='post', blank=True)
    content = models.TextField(blank=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('-pk',)