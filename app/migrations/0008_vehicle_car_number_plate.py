# Generated by Django 5.0.6 on 2024-05-21 11:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_remove_resident_household_members'),
    ]

    operations = [
        migrations.AddField(
            model_name='vehicle',
            name='car_number_plate',
            field=models.CharField(default='00000-0000000-0', max_length=150, unique=True),
        ),
    ]
