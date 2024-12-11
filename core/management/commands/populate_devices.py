from django.core.management.base import BaseCommand
from core.models import Device, User
import random

class Command(BaseCommand):
    help = "Populate Device models with meaningful names for testing"

    def handle(self, *args, **kwargs):
        # Get all users
        users = User.objects.all()
        if not users.exists():
            self.stdout.write(self.style.ERROR("No users found! Please populate users first."))
            return

        device_types = ["Light", "Thermostat", "HVAC", "Security Camera", "Smart Plug"]
        devices_data = []

        for user in users:
            for i in range(3):  # Assign 3 devices per user
                devices_data.append({
                    "user": user,
                    "name": f"{random.choice(['Living Room', 'Bedroom', 'Kitchen', 'Garage', 'Office'])} {random.choice(device_types)}",
                    "type": random.choice(device_types),
                    "status": random.choice(["ON", "OFF"]),
                })

        for device_data in devices_data:
            Device.objects.create(**device_data)

        self.stdout.write(self.style.SUCCESS(f"Populated {len(devices_data)} devices successfully!"))
