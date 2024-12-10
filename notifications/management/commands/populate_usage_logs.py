from django.core.management.base import BaseCommand
from notifications.models import UsageLog
from core.models import Device
from django.utils.timezone import now
import random

class Command(BaseCommand):
    help = "Populate usage logs with relevant data"

    def handle(self, *args, **kwargs):
        devices = Device.objects.all()

        for _ in range(50):  # Generate 50 usage logs
            device = random.choice(devices)
            UsageLog.objects.create(
                device_id=str(device.id),
                user_id=str(device.user.id),
                timestamp=now(),
                energy_consumed=random.uniform(0.5, 5.0),
                details={"device_name": device.name, "status": device.status},
            )
        
        self.stdout.write(self.style.SUCCESS("Usage logs populated successfully!"))
