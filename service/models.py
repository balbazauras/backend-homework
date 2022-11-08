from django.db import models
from django.conf import settings
import datetime
from django.contrib.auth.models import AbstractUser
from .utils import idToShortURL
from django.contrib.auth.models import User
from django.utils.timezone import utc


class Url(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    short = models.CharField(max_length=250)
    long = models.URLField(max_length=200)
    created_at = models.DateTimeField('%Y-%m-%d %H:%M:%S', auto_now_add=True)
    expiration_time = models.DateTimeField('%Y-%m-%d %H:%M:%S')
    active = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.long

    def generate_short_url(self):
        self.short = idToShortURL(self.id)
        self.save()

    def toggle_active(self):
        if self.active is True:
            self.active = False
        else:
            self.active = True
        self.save()

    def set_datetime(self, datetime):
        self.expiration_time = datetime
        self.save()

    def get_time_delta(self):
        now = datetime.datetime.utcnow().replace(tzinfo=utc)
        secs = self.expiration_time - now
        secs = secs.total_seconds()
        delta_time_string = ""
        if secs > 86400:  # 60sec * 60min * 24hrs
            days = secs // 86400
            delta_time_string += "{} days".format(int(days))
            secs = secs - days*86400

        if secs > 3600:
            hrs = secs // 3600
            delta_time_string += " {} hours".format(int(hrs))
            secs = secs - hrs*3600

        if secs > 60:
            mins = secs // 60
            delta_time_string += " {} minutes".format(int(mins))
            secs = secs - mins*60

        if secs > 0:
            delta_time_string += " {} seconds".format(int(secs))
        return delta_time_string
    # @property
    # def expired(self):
    #    return datetime.datetime.now() > self.expiration_time
