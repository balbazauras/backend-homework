# Generated by Django 4.0.4 on 2022-11-10 07:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0003_alter_url_click_current_alter_url_click_limit_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='url',
            old_name='long',
            new_name='long_url',
        ),
        migrations.RenameField(
            model_name='url',
            old_name='short',
            new_name='short_url',
        ),
    ]