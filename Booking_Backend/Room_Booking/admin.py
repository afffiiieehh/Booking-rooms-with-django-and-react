from django.contrib import admin
from .models import Room, RoomImage, OccupiedDate
from .models import User   # your custom user model

# Register your models here.

admin.site.register(User)
admin.site.register(Room)
admin.site.register(RoomImage)
admin.site.register(OccupiedDate)


