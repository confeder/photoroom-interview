from django.contrib.auth.models import Group
from rest_framework import serializers

from photoroom.models import ColorPallete

from .team import TeamSerializer


class TeamPrimaryKeyRelatedField(serializers.PrimaryKeyRelatedField):
    """Custom field to allow the user to only created palletes against teams it
    is a member of."""

    def get_queryset(self, *args, **kwargs):
        return Group.objects.filter(user=self.context["request"].user)


class ColorPalleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = ColorPallete
        fields = ["id", "name", "colors", "owner_id", "owner"]
        depth = 1

    # We're doing nested serialization for list/retrieve so that
    # a potential UI could display the name of the team that
    # owns the pallete.
    #
    # For writes, we want to accept just a primary key. We don't
    # need the caller to pass all the team details.
    owner_id = TeamPrimaryKeyRelatedField(
        queryset=Group.objects.all(), write_only=True, source="owner"
    )
    owner = TeamSerializer(read_only=True)
