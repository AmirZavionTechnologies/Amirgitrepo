# Generated by Django 5.0.6 on 2024-05-24 08:49

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Resident',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('phone_number', models.CharField(max_length=15)),
                ('apartment_number', models.CharField(max_length=10, unique=True)),
                ('cnic_number', models.CharField(default='00000-0000000-0', max_length=15, unique=True)),
                ('age', models.CharField(default='00000-0000000-0', max_length=20)),
                ('numberofpersons', models.CharField(default='00000-0000000-0', max_length=25)),
                ('entry_code', models.UUIDField(default=uuid.uuid4, editable=False)),
            ],
        ),
    ]
