from django.contrib import admin
from .models import Resident, Vehicle, Visitor, Guard
# Register your models here.
admin.site.register(Resident)
admin.site.register(Vehicle)
admin.site.register(Visitor)
admin.site.register(Guard)