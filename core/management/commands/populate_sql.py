from django.core.management.base import BaseCommand
from core.models import User, Device, Schedule
from django.utils.timezone import now, timedelta

class Command(BaseCommand):
    help = "Populate SQL collections for testing"

    def handle(self, *args, **kwargs):
        # Create users
        user = User.objects.create(
            email="testuser@example.com", username="testuser"
        )

        # Create devices
        device1 = Device.objects.create(
            user=user, name="Living Room Light", type="Light", status="OFF"
        )
        device2 = Device.objects.create(
            user=user, name="HVAC", type="HVAC", status="ON"
        )

        # Create schedules
        Schedule.objects.create(
            user=user,
            device=device1,
            time=now() + timedelta(hours=1),
            action="TURN_ON",
        )
        Schedule.objects.create(
            user=user,
            device=device2,
            time=now() + timedelta(hours=2),
            action="TURN_OFF",
        )

        self.stdout.write(self.style.SUCCESS("SQL collections populated successfully!"))
