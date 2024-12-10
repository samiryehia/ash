from django.shortcuts import render
from .models import User, Device, Schedule
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
    recommendations = Recommendation.objects(user_id=user_id).order_by("-timestamp")[:5]
    
    # Fetch action logs
    action_logs = Log.objects(user_id=user_id).order_by("-timestamp")[:10]
    
    # Fetch usage logs
    usage_logs = UsageLog.objects(user_id=user_id).order_by("-timestamp")[:10]
    
    return render(
        request,
        "core/index.html",
        {
            "recommendations": recommendations,
            "action_logs": action_logs,
            "usage_logs": usage_logs,
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
