import datetime

from django.contrib.auth.models import User
from django.db import models
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.utils.timezone import utc
from django.core.validators import MinValueValidator
from .utils import get_short_url_base58


class Url(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    short_url = models.CharField(max_length=250)
    long_url = models.URLField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    expiration_time = models.DateTimeField(
        validators=[MinValueValidator(timezone.now())])
    active = models.BooleanField(default=True)
    click_limit = models.PositiveIntegerField()

    def __str__(self) -> str:
        return self.long_url

    def generate_short_url_base58(self):
        self.short_url = get_short_url_base58(self.id)
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
        if secs > 0:
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
        else:
            return "Url expired"

    def is_expired(self):
        if timezone.now() > self.expiration_time:
            return True

    def get_number_of_clicks(self):
        clicks = get_object_or_404(
            Url, short_url=self.short_url).click_set.all()
        return clicks.count()


class Click(models.Model):
    url = models.ForeignKey(Url, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)
    referer = models.CharField(max_length=250)
    ip = models.GenericIPAddressField()
    redirect_time = models.FloatField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, url, referer, ip, *args, **kwargs):
        self.url = url
        self.referer = referer
        self.ip = ip
        super(Click, self).save(*args, **kwargs)

    def save_redirect_time(self, duration, *args, **kwargs):
        self.redirect_time = duration
        super(Click, self).save(*args, **kwargs)
