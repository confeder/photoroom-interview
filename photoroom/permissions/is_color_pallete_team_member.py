from rest_framework import permissions
from rest_framework.request import Request

from photoroom.models import ColorPallete


class IsColorPalleteTeamMember(permissions.BasePermission):
    def has_permission(self, request: Request, view) -> bool:
        if not request.user or not request.user.is_authenticated:
            return False

        # Restricting the queryset to only view/retrieve color
        # palletes of teams the user is a member of is handled
        # in the view by restricting the query set.
        if view.action in ("list", "retrieve"):
            return request.user.has_perm("photoroom.view_colorpallete")

        # TODO: this could be made more efficient by fetching all
        # the model level permissions and checking against that
        # instead of doing it one by one
        return (
            request.user.has_perm("photoroom.add_colorpallete")
            or request.user.has_perm("photoroom.change_colorpallete")
            or request.user.has_perm("photoroom.delete_colorpallete")
        )

    def has_object_permission(
        self, request: Request, view, color_pallete: ColorPallete
    ) -> bool:
        is_member_of_owner_team = request.user.groups.filter(id=color_pallete.owner_id).exists()  # type: ignore[union-attr]
        if not is_member_of_owner_team:
            return False

        if view.action in ("update", "partial_update"):
            return request.user.has_perm("photoroom.change_colorpallete")
        elif view.action == "destroy":
            return request.user.has_perm("photoroom.delete_colorpallete")

        # Situation we didn't handle, but better not give permission.
        # Sane defaults etc...
        return False
