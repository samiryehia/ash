from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
class User(AbstractUser):
    preferences = models.JSONField(default=dict)  # User preferences stored as JSON

    def __str__(self):
        return self.username

class Room(models.Model):
    """
    Represents a room in the house.
    """
    name = models.CharField(max_length=100)
    admin = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="admin_rooms")
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="accessible_rooms")

    def __str__(self):
        return self.name


class Device(models.Model):
    """
    Represents a smart home device.
    """
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=50)
    status = models.CharField(max_length=10, choices=[("ON", "On"), ("OFF", "Off")], default="OFF")
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="devices")
    type = models.CharField(max_length=50)  # Device type, e.g., 'Light', 'HVAC'
    energy_usage = models.FloatField(default=0.0)  # Energy usage in kWh

    def __str__(self):
        return self.name



class Schedule(models.Model):
    ACTION_CHOICES = [
        ('TURN_ON', 'Turn On'),
        ('TURN_OFF', 'Turn Off'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    time = models.DateTimeField()
    action = models.CharField(max_length=50, choices=ACTION_CHOICES)  # Scheduled action

    def __str__(self):
        return f"{self.action} {self.device.name} at {self.time}"
