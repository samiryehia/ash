from django.core.management.base import BaseCommand
from core.models import Room, Device
from django.contrib.auth import get_user_model
import random

# Get the custom User model
User = get_user_model()

class Command(BaseCommand):
    help = "Delete all records from Devices and Rooms and repopulate them"

    def handle(self, *args, **kwargs):
        # Step 1: Delete all existing records for devices and rooms
        self.stdout.write("Deleting all devices and rooms...")
        Device.objects.all().delete()
        Room.objects.all().delete()

        # Step 2: Create or fetch users without duplication
        self.stdout.write("Creating users...")
        users_data = [
            {"username": "mohamed", "email": "mohamed@example.com"},
            {"username": "majid", "email": "majid@example.com"},
            {"username": "jad", "email": "jad@example.com"},
            {"username": "abdulaziz", "email": "abdulaziz@example.com"},
            {"username": "samir", "email": "samir@example.com"},
        ]

        users = []
        for user_data in users_data:
            user, created = User.objects.get_or_create(
                username=user_data["username"],
                defaults={"email": user_data["email"]}
            )
            users.append(user)

        # Step 3: Create rooms and assign users
        self.stdout.write("Creating rooms and devices...")
        rooms_data = [
            {"name": "Living Room", "admin": users[0], "users": [users[0], users[1]]},
            {"name": "Kitchen", "admin": users[1], "users": [users[1], users[2]]},
            {"name": "Bedroom", "admin": users[2], "users": [users[2], users[3]]},
            {"name": "Office", "admin": users[3], "users": [users[3], users[4]]},
            {"name": "Garage", "admin": users[4], "users": [users[4], users[0]]},
        ]

        for room_data in rooms_data:
            # Explicitly fetch the User instance for the admin
            admin = User.objects.get(username=room_data["admin"].username)
            room = Room.objects.create(name=room_data["name"], admin=admin)
            room.users.set(room_data["users"])  # Set other users for the room
            room.save()

            # Step 4: Add devices to the room
            device_types = ["Light", "Thermostat", "HVAC", "Security Camera", "Smart Plug"]
            for i in range(3):  # Add 3 devices per room
                Device.objects.create(
                    name=f"{room.name} {device_types[i % len(device_types)]}",
                    type=device_types[i % len(device_types)],
                    status=random.choice(["ON", "OFF"]),
                    room=room,
                    energy_usage=round(random.uniform(0.5, 5.0), 2),  # Random energy usage in kWh
                )

        self.stdout.write(self.style.SUCCESS("All devices and rooms reset and repopulated successfully!"))
