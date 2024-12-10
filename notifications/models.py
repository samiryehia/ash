from django.db import models

# Create your models here.
from mongoengine import Document, StringField, DateTimeField, BooleanField, DictField, FloatField

class Notification(Document):
    """
    Model for storing user notifications.
    """
    user_id = StringField(required=True)  # Foreign key to the User table (SQL ID)
    message = StringField(required=True)  # Notification content
    type = StringField(choices=['Recommendation', 'Alert'], required=True)
    timestamp = DateTimeField()  # Time when notification was created
    status = StringField(choices=['Read', 'Unread'], default='Unread')
    action_required = BooleanField(default=False)
    related_id = StringField()  # Link to related recommendations or logs


class Recommendation(Document):
    """
    Model for storing recommendations for energy efficiency.
    """
    user_id = StringField(required=True)  # Foreign key to the User table (SQL ID)
    device_id = StringField()  # Device ID related to the recommendation
    timestamp = DateTimeField()  # Time when recommendation was created
    type = StringField()  # Recommendation type, e.g., 'Energy', 'Usage'
    feedback = StringField()  # User feedback on the recommendation
    details = DictField()  # Extra details, e.g., expected savings, reasons


class Log(Document):
    """
    Model to log device actions and energy usage.
    """
    user_id = StringField(required=True)  # User ID (from SQL)
    device_id = StringField(required=True)  # Device ID (from SQL)
    action = StringField(required=True)  # Action performed, e.g., "Turn On"
    timestamp = DateTimeField(required=True)  # Time of the action
    details = DictField()  # Additional metadata about the action

class UsageLog(Document):
    """
    Model to monitor device energy usage.
    """
    device_id = StringField(required=True)  # Device ID (from SQL)
    user_id = StringField(required=True)  # User ID (from SQL)
    timestamp = DateTimeField(required=True)  # Time of the log
    energy_consumed = FloatField(required=True)  # Energy consumed (kWh)
    details = DictField()  # Additional usage details
