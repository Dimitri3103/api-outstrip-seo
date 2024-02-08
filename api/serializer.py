from rest_framework import serializers

class InputSerializer(serializers.Serializer):
    url = serializers.URLField()