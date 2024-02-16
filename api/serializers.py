from rest_framework import serializers


class MoodcheckSerializer(serializers.Serializer):
    text = serializers.CharField()
