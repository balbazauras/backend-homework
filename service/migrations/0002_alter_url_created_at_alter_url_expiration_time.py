# Generated by Django 4.0.4 on 2022-11-04 12:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='url',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='%Y-%m-%d %H:%M:%S'),
        ),
        migrations.AlterField(
            model_name='url',
            name='expiration_time',
            field=models.DateTimeField(verbose_name='%Y-%m-%d %H:%M:%S'),
        ),
    ]
