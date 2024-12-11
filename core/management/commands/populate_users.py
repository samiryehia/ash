from django.core.management.base import BaseCommand
from core.models import User

class Command(BaseCommand):
    help = "Populate User models with specific names for testing"

    def handle(self, *args, **kwargs):
        users_data = [
            {"username": "mohamed_watfa", "email": "mohamed.watfa@ash.com"},
            {"username": "majid_el_ezzi", "email": "majid.el.ezzi@ash.com"},
            {"username": "jad_awar", "email": "jad.awar@ash.com"},
            {"username": "abdulaziz_el_sayyed", "email": "abdulaziz.el.sayyed@ash.com"},
            {"username": "samir_yehia", "email": "samir.yehia@ash.com"},
        ]

        for user_data in users_data:
            User.objects.create(**user_data)

        self.stdout.write(self.style.SUCCESS(f"Populated {len(users_data)} users successfully!"))
