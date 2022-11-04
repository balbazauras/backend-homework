from django.db import models
from django.conf import settings
import datetime


class Url(models.Model):
    short = models.CharField(max_length=250)
    long = models.URLField(max_length=200)
    created_at = models.DateTimeField('%Y-%m-%d %H:%M:%S', auto_now_add=True)
    expiration_time = models.DateTimeField('%Y-%m-%d %H:%M:%S')

    def __str__(self) -> str:
        return self.long

    @property
    def expired(self):
        return datetime.datetime.now() > self.expiration_time
