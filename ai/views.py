from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from stable_baselines3 import PPO
import numpy as np
from .serializers import RecommendationInputSerializer, RecommendationOutputSerializer

# Action descriptions
action_descriptions = {
    0: "Turn off all devices.",
    1: "Set the thermostat to energy-saving mode.",
    2: "Turn off lights in unoccupied rooms.",
    3: "Activate security cameras.",
    4: "Reduce HVAC power during non-peak hours.",
    5: "Turn on the entertainment system.",
    6: "Schedule device usage for off-peak hours.",
    7: "Enable eco mode for all devices.",
    8: "Send a notification about energy usage.",
    9: "Perform a maintenance check on devices."
}

class RecommendationView(APIView):
    """
    API View to get energy efficiency recommendations.
    """
    def post(self, request):
        # Validate input
        input_serializer = RecommendationInputSerializer(data=request.data)
        if not input_serializer.is_valid():
            return Response(input_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Load the trained model
        model = PPO.load("ai/ml/model/trained_model")

        # Predict the action
        state = np.array(input_serializer.validated_data['state']).reshape(1, -1)
        action, _ = model.predict(state, deterministic=True)

        # Prepare the response
        output_data = {
            "action": int(action),
            "description": action_descriptions.get(int(action), "Unknown action")
        }
        output_serializer = RecommendationOutputSerializer(output_data)
        return Response(output_serializer.data, status=status.HTTP_200_OK)
