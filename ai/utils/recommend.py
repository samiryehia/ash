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
    0: {"action": "Turn off all devices", "reason": "Reduce standby energy usage", "expected_savings": "15%"},
    1: {"action": "Enable eco mode", "reason": "Optimize energy consumption", "expected_savings": "10%"},
    2: {"action": "Dim lights", "reason": "Lower lighting energy consumption", "expected_savings": "5%"},
    3: {"action": "Schedule HVAC usage", "reason": "Avoid peak hours for HVAC", "expected_savings": "20%"},
    4: {"action": "Activate security cameras", "reason": "Enhance safety during nighttime", "expected_savings": "N/A"},
    5: {"action": "Adjust thermostat to 22°C", "reason": "Maintain comfortable temperature", "expected_savings": "12%"},
    6: {"action": "Turn on water heater", "reason": "Prepare for morning showers", "expected_savings": "5%"},
    7: {"action": "Disable standby mode", "reason": "Save idle power usage", "expected_savings": "3%"},
    8: {"action": "Turn on outdoor lights", "reason": "Increase security visibility", "expected_savings": "N/A"},
    9: {"action": "Close window blinds", "reason": "Retain indoor heat", "expected_savings": "8%"},
    10: {"action": "Turn off non-essential appliances", "reason": "Minimize energy waste", "expected_savings": "10%"},
    11: {"action": "Schedule dishwasher usage", "reason": "Run during off-peak hours", "expected_savings": "15%"},
    12: {"action": "Switch to renewable power source", "reason": "Reduce carbon footprint", "expected_savings": "N/A"},
    13: {"action": "Enable night mode", "reason": "Reduce unnecessary light brightness", "expected_savings": "7%"},
    14: {"action": "Optimize ventilation system", "reason": "Improve air circulation", "expected_savings": "5%"},
    15: {"action": "Monitor refrigerator temperature", "reason": "Prevent overcooling", "expected_savings": "4%"},
    16: {"action": "Enable smart scheduling", "reason": "Synchronize device usage", "expected_savings": "18%"},
    17: {"action": "Turn off gaming consoles", "reason": "Minimize idle power draw", "expected_savings": "6%"},
    18: {"action": "Reduce HVAC power during peak hours", "reason": "Minimize energy costs", "expected_savings": "20%"},
    19: {"action": "Install energy-saving bulbs", "reason": "Reduce lighting costs", "expected_savings": "25%"},
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
