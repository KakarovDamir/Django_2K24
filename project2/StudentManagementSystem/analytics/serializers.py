from rest_framework import serializers

class ActiveUserSerializer(serializers.Serializer):
    username = serializers.CharField()
    request_count = serializers.IntegerField()