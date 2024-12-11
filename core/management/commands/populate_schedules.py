from django.core.management.base import BaseCommand
from core.models import Schedule, Device
from django.utils.timezone import now, timedelta
import random

class Command(BaseCommand):
    help = "Populate Schedule models with meaningful data for testing"

    def handle(self, *args, **kwargs):
        devices = Device.objects.all()

        # Check if devices exist
        if not devices.exists():
            self.stdout.write(self.style.ERROR("No devices found! Please populate devices first."))
            return

        actions = ["TURN_ON", "TURN_OFF"]
        schedules_data = []

        # Generate schedules for each device
        for device in devices:
            for i in range(2):  # Assign 2 schedules per device
                schedule = Schedule(
                    device=device,
                    time=now() + timedelta(hours=random.randint(1, 72)),
                    action=random.choice(actions)
                )
                schedules_data.append(schedule)

        # Bulk create schedules to optimize database writes
        Schedule.objects.bulk_create(schedules_data)

        self.stdout.write(self.style.SUCCESS(f"Populated {len(schedules_data)} schedules successfully!"))
