from django.contrib.auth.models import Group, Permission, User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "password", "group_ids"]
        extra_kwargs = {"password": {"write_only": True}}

    group_ids: serializers.PrimaryKeyRelatedField = serializers.PrimaryKeyRelatedField(
        read_only=True, many=True, source="groups"
    )

    def create(self, validated_data):
        default_permissions = list(
            Permission.objects.filter(
                codename__in=[
                    "add_group",
                    "change_group",
                    "delete_group",
                    "view_group",
                    "add_colorpallete",
                    "change_colorpallete",
                    "delete_colorpallete",
                    "view_colorpallete",
                ]
            )
        )

        group = Group.objects.create(name=validated_data["username"])

        user = User.objects.create_user(**validated_data)
        user.user_permissions.set(default_permissions)
        user.groups.add(group)

        return user
