# Generated by Django 4.0.4 on 2022-11-14 13:30

import datetime
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0010_alter_url_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='url',
            name='expiration_time',
            field=models.DateTimeField(validators=[django.core.validators.MinValueValidator(datetime.date.today)]),
        ),
    ]
