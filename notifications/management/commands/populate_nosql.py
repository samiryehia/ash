from django.core.management.base import BaseCommand
from notifications.models import Notification

class Command(BaseCommand):
    help = "Populate NoSQL collections for testing"

    def handle(self, *args, **kwargs):
        # Add notifications
        Notification.objects.create(
            user_id="1",
            message="Living Room Light is scheduled to turn ON in 1 hour.",
            type="Alert",
            timestamp="2024-12-08T19:00:00+00:00",
            status="Unread",
            action_required=True,
        )
        Notification.objects.create(
            user_id="1",
            message="Your HVAC system is running in energy-saving mode.",
            type="Recommendation",
            timestamp="2024-12-08T20:00:00+00:00",
            status="Unread",
            action_required=False,
        )

        self.stdout.write(self.style.SUCCESS("NoSQL collections populated successfully!"))
