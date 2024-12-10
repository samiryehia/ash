from django.db import models

class User(models.Model):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=100)
    preferences = models.JSONField(default=dict)  # User preferences stored as JSON

    def __str__(self):
        return self.username


class Device(models.Model):
    STATUS_CHOICES = [
        ('ON', 'On'),
        ('OFF', 'Off'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='devices')
    name = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='OFF')
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
