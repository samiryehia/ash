from stable_baselines3 import PPO
from notifications.models import Recommendation
from django.utils.timezone import now
import numpy as np


def generate_recommendations_from_logs(user_id, usage_logs):
    """
    Generate AI-based recommendations from usage logs.

    Args:
        user_id (str): The ID of the user.
        usage_logs (QuerySet): Recent usage logs for the user.

    Returns:
        None
    """
    if not usage_logs:
        print(f"No usage logs found for user_id: {user_id}")
        return

    # Prepare the AI model input
    energy_metrics = [log.energy_consumed for log in usage_logs]
    # Pad with zeros to match the required shape (16,)
    padded_metrics = energy_metrics + [0.0] * (16 - len(energy_metrics))
    usage_context = np.array(padded_metrics).reshape(1, -1)  # Shape: (1, 16)

    # Load the trained AI model
    model = PPO.load("ai/ml/models/trained_model")

    # Predict action
    action, _ = model.predict(usage_context, deterministic=True)

    # Map predicted action to recommendation details
    action_map = {
    0: {"action": "Turn off all lights", "reason": "Reduce unnecessary lighting energy", "expected_savings": "10%"},
    1: {"action": "Dim living room lights to 50%", "reason": "Lower lighting energy consumption during relaxation", "expected_savings": "5%"},
    2: {"action": "Turn off HVAC in unoccupied rooms", "reason": "Save energy in unused spaces", "expected_savings": "15%"},
    3: {"action": "Schedule HVAC to run during off-peak hours", "reason": "Avoid high energy costs during peak times", "expected_savings": "20%"},
    4: {"action": "Activate security cameras", "reason": "Enhance safety at night", "expected_savings": "N/A"},
    5: {"action": "Set thermostat to 22°C in the bedroom", "reason": "Maintain comfortable sleeping temperature", "expected_savings": "12%"},
    6: {"action": "Turn off kitchen appliances", "reason": "Avoid standby energy usage", "expected_savings": "8%"},
    7: {"action": "Enable eco mode on HVAC", "reason": "Optimize energy consumption", "expected_savings": "10%"},
    8: {"action": "Turn on water heater for 30 minutes", "reason": "Prepare for morning showers efficiently", "expected_savings": "5%"},
    9: {"action": "Enable night mode on lights", "reason": "Reduce unnecessary brightness during sleep", "expected_savings": "7%"},
    10: {"action": "Adjust thermostat in the living room to 24°C", "reason": "Reduce cooling energy consumption", "expected_savings": "8%"},
    11: {"action": "Switch off garage lights", "reason": "Prevent wasteful lighting in unoccupied areas", "expected_savings": "5%"},
    }


    recommendation_details = action_map.get(
        int(action),
        {"action": "Unknown", "reason": "No reason available", "expected_savings": "0%"},
    )

    # Save the recommendation in the database
    Recommendation.objects.create(
        user_id=user_id,
        device_id=None,  # General recommendations may not target specific devices
        timestamp=now(),
        type="Energy",
        feedback=None,
        details=recommendation_details,
    )
    print(f"Recommendation saved for user_id {user_id}: {recommendation_details}")
