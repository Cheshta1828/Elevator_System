from django.contrib import admin

# Register your models here.
from .models import Elevator,Building,ElevatorRequest
admin.site.register(Elevator)
admin.site.register(Building)
admin.site.register(ElevatorRequest)