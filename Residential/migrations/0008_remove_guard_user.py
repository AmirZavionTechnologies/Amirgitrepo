# Generated by Django 5.0.6 on 2024-05-30 10:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Residential', '0007_guard_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='guard',
            name='user',
        ),
    ]
