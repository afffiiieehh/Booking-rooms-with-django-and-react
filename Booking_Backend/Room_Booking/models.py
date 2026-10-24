from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
# Create your models here.

class Room(models.Model):


    Room_TYPE = [
        ('suite','Suite'),
        ('standard','Standard Room'),
        ('deluxe','Deluxe Room'),
    ]
    CURRENCY_TYPE = [
        ('USD','USD'),
        ('EUR','EUR'),
    ]

    name = models.CharField(max_length=100, blank=True, default='')
    type = models.CharField(max_length=20, choices=Room_TYPE,)
    pricePerNight = models.IntegerField(default=150)
    currency = models.CharField(max_length=10, choices=CURRENCY_TYPE, default='USD')
    maxOccupancy = models.IntegerField(default=1)
    description = models.TextField(max_length=500, blank=True, default='')

    def __str__(self):
        return f"{self.name} ({self.type})"
    
class RoomImage(models.Model):
    image = models.ImageField(upload_to='room_images/')
    caption = models.CharField(max_length=100, blank=True, default='write')
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='images')

    def __str__(self):
        return f"Image for {self.room.name} - {self.caption or 'No Caption '}"


class OccupiedDate(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='occupied_dates')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='booked_dates')
    date = models.DateField()



class User(AbstractUser):
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=100, blank=True, default='')

    def __str__(self):
        return super().__str__()

