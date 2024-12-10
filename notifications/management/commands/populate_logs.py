from django.core.management.base import BaseCommand
from notifications.models import Log, UsageLog
from core.models import Device
from django.utils.timezone import now, timedelta
import random


class Command(BaseCommand):
    help = "Populate action logs and energy usage logs for testing"

    def handle(self, *args, **kwargs):
        # Fetch devices
        devices = Device.objects.all()

        # Populate action logs
        for device in devices:
            Log.objects.create(
                user_id=str(device.user.id),
                device_id=str(device.id),
                action=f"Turn {'ON' if device.status == 'OFF' else 'OFF'}",
                timestamp=now() - timedelta(minutes=random.randint(1, 60)),
                details={"device_name": device.name, "type": device.type},
            )

        self.stdout.write(self.style.SUCCESS("Action logs populated successfully!"))

        # Populate energy usage logs
        for device in devices:
            UsageLog.objects.create(
                device_id=str(device.id),
                user_id=str(device.user.id),
                timestamp=now() - timedelta(minutes=random.randint(1, 60)),
                energy_consumed=random.uniform(0.5, 5.0),  # Random energy usage (kWh)
                details={"device_name": device.name, "status": device.status},
            )

        self.stdout.write(self.style.SUCCESS("Energy usage logs populated successfully!"))
