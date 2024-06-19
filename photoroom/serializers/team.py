from django.contrib.auth.models import Group, User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email"]


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ["id", "name", "users"]
        depth = 2

    users = UserSerializer(many=True, read_only=True, source="user_set")
