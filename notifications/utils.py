from notifications.models import UsageLog
from ai.utils.recommend import generate_recommendations_from_logs

def generate_recommendations(user_id):
    """
    Generate recommendations based on the AI model and usage logs.
    
    Args:
        user_id (str): The ID of the user.
    
    Returns:
        None
    """
    # Fetch recent usage logs for the user
    usage_logs = UsageLog.objects(user_id=user_id).order_by("-timestamp")[:5]

    # Generate recommendations using the AI model
    generate_recommendations_from_logs(user_id, usage_logs)
