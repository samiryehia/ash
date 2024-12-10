from django.shortcuts import render, redirect
from django.http import JsonResponse
from notifications.models import Notification, Log, UsageLog
from django.utils.timezone import now


def notifications_list(request):
    """
    View to display all notifications for the logged-in user.
    """
    user_id = "1"  # Replace with dynamic user authentication logic
    notifications = Notification.objects(user_id=user_id).order_by("-timestamp")
    return render(request, "notifications/notifications.html", {"notifications": notifications})


def mark_as_read(request, notification_id):
    """
    Mark a notification as read.
    """
    notification = Notification.objects(id=notification_id).first()
    if notification:
        notification.status = "Read"
        notification.save()
    return redirect("notifications:notifications_list")


def clear_notifications(request):
    """
    Clear all notifications for the logged-in user.
    """
    user_id = "1"  # Replace with dynamic user authentication logic
    Notification.objects(user_id=user_id).delete()
    return redirect("notifications:notifications_list")


def logs_list(request):
    """
    View to display all action logs for the logged-in user.
    """
    user_id = "1"  # Replace with dynamic user authentication logic
    logs = Log.objects(user_id=user_id).order_by("-timestamp")
    return render(request, "notifications/logs.html", {"logs": logs})


def usage_logs_list(request):
    """
    View to display all energy usage logs for the logged-in user.
    """
    user_id = "1"  # Replace with dynamic user authentication logic
    usage_logs = UsageLog.objects(user_id=user_id).order_by("-timestamp")
    return render(request, "notifications/usage_logs.html", {"usage_logs": usage_logs})


def clear_logs(request):
    """
    Clear all logs for the logged-in user.
    """
    user_id = "1"  # Replace with dynamic user authentication logic
    Log.objects(user_id=user_id).delete()
    UsageLog.objects(user_id=user_id).delete()
    return redirect("notifications:logs_list")
