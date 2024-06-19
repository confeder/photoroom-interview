from django.contrib.auth.models import Group
from django.db.models import QuerySet
from rest_framework import viewsets

from photoroom.permissions import IsNewTeamOrMember
from photoroom.serializers import TeamSerializer


class TeamViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = TeamSerializer
    permission_classes = [IsNewTeamOrMember]

    def perform_create(self, serializer):
        """Creates the team and adds the user to it."""

        team = serializer.save()
        self.request.user.groups.add(team)

    def get_queryset(self) -> QuerySet[Group]:
        """Show only teams that the user is a part of.

        This does mean that when the user tries to retrieve a team it is
        not a member of they get a 404 instead of a permission denied.
        This expected behavior. We do not want to leak that the team
        exists.
        """

        return super().get_queryset().filter(user=self.request.user)
