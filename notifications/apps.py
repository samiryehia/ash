from django.apps import AppConfig
from mongoengine import connect


class NotificationsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "notifications"
    def ready(self):
        """
        Connect to MongoDB when the app is ready.
        """
        MONGO_DB_NAME = "ash"
        connect(
            db=MONGO_DB_NAME,
            host="localhost",
            port=27017
        )
