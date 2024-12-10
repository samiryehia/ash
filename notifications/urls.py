from django.urls import path
from . import views

app_name = "notifications"

urlpatterns = [
    # Notifications
    path("", views.notifications_list, name="notifications_list"),
    path("mark-as-read/<str:notification_id>/", views.mark_as_read, name="mark_as_read"),
    path("clear-notifications/", views.clear_notifications, name="clear_notifications"),

    # Logs
    path("logs/", views.logs_list, name="logs_list"),
    path("usage-logs/", views.usage_logs_list, name="usage_logs_list"),
    path("clear-logs/", views.clear_logs, name="clear_logs"),
]
