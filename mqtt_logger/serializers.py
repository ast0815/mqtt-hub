"""Serializers for the use with rest-pandas"""

from rest_framework import serializers

from .models import MQTTMessage

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = MQTTMessage
        fields = ('id', 'time_recorded', 'topic', 'payload')
