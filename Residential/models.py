from django.db import models
import uuid
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.
class Residentsdata(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,null=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    apartment_number = models.CharField(max_length=10, unique=True)
    cnic_number = models.CharField(max_length=15, unique=True, default='00000-0000000-0')
    age=models.CharField(max_length=20,default='00000-0000000-0')
    numberofpersons=models.CharField(max_length=25,default='00000-0000000-0')
    entry_code = models.UUIDField(default=uuid.uuid4, editable=False)

    def __str__(self):
        return self.user.username


    def __str__(self):
        return self.user.username
class Visitor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    visit_reason = models.CharField(max_length=100)
    # Add other fields as necessary

    def __str__(self):
        return self.user.username

class Vehiclesdata(models.Model):
    owner = models.ForeignKey(Residentsdata, on_delete=models.CASCADE, related_name='vehicles')
    vehicle_number = models.CharField(max_length=20, unique=True)
    vehicle_type = models.CharField(max_length=50)
    vehicle_model = models.CharField(max_length=50)
    car_number_plate=models.CharField(max_length=150,unique=True,default='00000-0000000-0')
    carmodel= models.CharField(max_length=100,unique=True,default='00000-0000000-0')  
    entry_codes=models.UUIDField(default=uuid.uuid4, editable=False)
    
    def __str__(self):
        return self.vehicle_number
    
    
class Guard(models.Model):
    badge_number = models.CharField(max_length=50, unique=True)
    shift_start_time = models.TimeField()
    shift_end_time = models.TimeField()

    def __str__(self):
        return self.user.username
        
class User(models.Model):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('resident', 'Resident'),
        ('visitor', 'Visitor'),
        ('guard', 'Guard'),
    )
    
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    def __str__(self):
        return self.username
