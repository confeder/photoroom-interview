from django.contrib.auth.models import Group
from django.db.models import QuerySet
from rest_framework import authentication, serializers, viewsets
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response

from photoroom.permissions import CanJoinLeaveTeam, IsNewTeamOrMember
from photoroom.serializers import TeamSerializer


class TeamMembershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group.user_set.through
        fields = ["group", "user"]


class TeamViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = TeamSerializer
    authentication_classes = [authentication.BasicAuthentication]
    permission_classes = [IsNewTeamOrMember]

    def perform_create(self, serializer) -> None:
        """Creates the team and adds the user to it."""

        team = serializer.save()
        self.request.user.groups.add(team)  # type: ignore[union-attr]

    def get_queryset(self) -> QuerySet[Group]:
        """Show only teams that the user is a part of.

        This does mean that when the user tries to retrieve a team it is
        not a member of they get a 404 instead of a permission denied.
        This expected behavior. We do not want to leak that the team
        exists.
        """

        return super().get_queryset().filter(user=self.request.user)

    @action(
        detail=True,
        methods=["PUT"],
        name="Join/leave team",
        permission_classes=[CanJoinLeaveTeam],
    )
    def membership(self, request: Request, pk: int) -> Response:
        serializer = TeamMembershipSerializer(
            data=dict(group=pk, user=self.request.user.id)
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=204)

    @membership.mapping.delete
    def delete_membership(self, request: Request, pk: int) -> Response:
        deleted_count, test = Group.user_set.through.objects.filter(
            group_id=pk, user=self.request.user
        ).delete()
        if deleted_count > 0:
            return Response(status=204)

        return Response(status=404)
