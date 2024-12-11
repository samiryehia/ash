from django.shortcuts import render
from .models import User, Device, Schedule, Room
from notifications.models import Notification, Log, UsageLog  # Import NoSQL model
 
from django.shortcuts import redirect, render
from django.utils.timezone import now
from notifications.models import Recommendation, UsageLog
from notifications.utils import generate_recommendations
def index(request):
    """
    Dashboard view with logs, notifications, and recommendations.
    """
    user_id = "1"  # Replace with dynamic user authentication logic

    # Fetch recommendations
    recommendations = Recommendation.objects(user_id=user_id).order_by("-timestamp")[:3]
    rooms = Room.objects.prefetch_related("users").all()  # Fetch rooms and their users
    devices = Device.objects.select_related("room").all()  # Fetch devices and their associated rooms

    # Fetch notifications
    notifications = Notification.objects.all() # Latest notifications for the user

    # Fetch action logs
    action_logs = Log.objects.order_by("-timestamp")[:3]  # Ordered by most recent

    # Fetch usage logs
    usage_logs = UsageLog.objects(user_id=user_id).order_by("-timestamp")[:3]

    return render(
        request,
        "core/index.html",
        {
            "recommendations": recommendations,
            "action_logs": action_logs,
            "usage_logs": usage_logs,
            "notifications": notifications,
            "rooms": rooms,
            "devices": devices,
        },
    )


from django.shortcuts import redirect
from notifications.utils import generate_recommendations

def generate_recommendations_view(request):
    """
    Trigger recommendation generation and redirect to the dashboard.
    """
    
    if request.method == "POST":
        user_id = "1"  # Replace with dynamic user authentication logic
        generate_recommendations(user_id)  # Generate recommendations
    return redirect("core:index")  # Redirect back to the dashboard



def users(request):
    """
    List all users.
    """
    users = User.objects.all()
    return render(request, "core/users.html", {"users": users})


def devices(request):
    """
    List all devices.
    """
    devices = Device.objects.all()
    return render(request, "core/devices.html", {"devices": devices})


def schedules(request):
    """
    List all schedules.
    """
    schedules = Schedule.objects.select_related("device")
    return render(request, "core/schedules.html", {"schedules": schedules})

def toggle_device(request, device_id):
    """
    Toggle the status of a device (ON/OFF).
    Log the action and update the device status.
    """
    device = Device.objects.get(id=device_id)
    user = request.user  # The logged-in user performing the action

    # Toggle the device status
    previous_status = device.status
    device.status = "OFF" if device.status == "ON" else "ON"
    device.save()

    # Log the action in the Log collection
    Log.objects.create(
        user_id=str(user.id),
        device_id=str(device.id),
        action=f"Turned {device.status}",
        timestamp=now(),
        details={
            "device_name": device.name,
            "previous_status": previous_status,
            "current_status": device.status,
        },
    )

    return redirect("core:index")
