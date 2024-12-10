from rest_framework import serializers
from .models import Notification, Recommendation

class NotificationSerializer(serializers.Serializer):
    """
    Serializer for Notification model.
    """
    id = serializers.CharField(read_only=True)
    user_id = serializers.CharField()
    message = serializers.CharField()
    type = serializers.CharField()
    timestamp = serializers.DateTimeField()
    status = serializers.CharField(default="Unread")
    action_required = serializers.BooleanField(default=False)
    related_id = serializers.CharField(required=False)

    def create(self, validated_data):
        return Notification(**validated_data).save()

    def update(self, instance, validated_data):
        instance.update(**validated_data)
        instance.reload()
        return instance


class RecommendationSerializer(serializers.Serializer):
    """
    Serializer for Recommendation model.
    """
    id = serializers.CharField(read_only=True)
    user_id = serializers.CharField()
    device_id = serializers.CharField()
    timestamp = serializers.DateTimeField()
    type = serializers.CharField()
    feedback = serializers.CharField(required=False)
    details = serializers.DictField()

    def create(self, validated_data):
        return Recommendation(**validated_data).save()

    def update(self, instance, validated_data):
        instance.update(**validated_data)
        instance.reload()
        return instance
