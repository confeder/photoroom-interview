from django.contrib.auth.models import Group
from rest_framework import viewsets

from photoroom.serializers import TeamSerializer


class TeamViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = TeamSerializer

    def perform_create(self, serializer):
        """Creates the team and adds the user to it."""

        team = serializer.save()
        self.request.user.groups.add(team)
