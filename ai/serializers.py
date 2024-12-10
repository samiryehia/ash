from rest_framework import serializers

class RecommendationInputSerializer(serializers.Serializer):
    """
    Serializer for input to the recommendation API.
    """
    state = serializers.ListField(
        child=serializers.FloatField(),
        min_length=15,
        max_length=15
    )

class RecommendationOutputSerializer(serializers.Serializer):
    """
    Serializer for output from the recommendation API.
    """
    action = serializers.IntegerField()
    description = serializers.CharField()
