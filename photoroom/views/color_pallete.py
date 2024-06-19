from django.db.models import QuerySet
from rest_framework import viewsets

from photoroom.models import ColorPallete
from photoroom.permissions import IsColorPalleteTeamMember
from photoroom.serializers import ColorPalleteSerializer


class ColorPalleteViewSet(viewsets.ModelViewSet):
    queryset = ColorPallete.objects.select_related("owner").all()
    serializer_class = ColorPalleteSerializer
    permission_classes = [IsColorPalleteTeamMember]

    def get_queryset(self) -> QuerySet[ColorPallete]:
        """Show only color palletes of teams that the user is a member of.

        This does mean that when the user tries to retrieve a color
        pallete of a team that it is not a member of they will get a
        404. This is expected behavior. We do not want to leak the
        existence of the pallete.
        """

        return super().get_queryset().filter(owner__user=self.request.user)
