from django.contrib.auth.models import Group
from rest_framework import permissions
from rest_framework.request import Request


class IsNewTeamOrMember(permissions.BasePermission):
    def has_permission(self, request: Request, view) -> bool:
        if not request.user or not request.user.is_authenticated:
            return False

        # Restricting the queryset to only view/retrieve teams
        # the user is a member of is handled in the view.
        if view.action in ("list", "retrieve"):
            return request.user.has_perm("auth.view_group")

        # TODO: this could be made more efficient by fetching all
        # the model level permissions and checking against that
        # instead of doing it one by one
        return (
            request.user.has_perm("auth.add_group")
            or request.user.has_perm("auth.change_group")
            or request.user.has_perm("auth.delete_group")
        )

    def has_object_permission(self, request: Request, view, group: Group) -> bool:
        is_member_of_team = request.user.groups.filter(id=group.id).exists()  # type: ignore[union-attr]
        if not is_member_of_team:
            return False

        if view.action in ("update", "partial_update"):
            return request.user.has_perm("auth.change_group")
        elif view.action == "destroy":
            return request.user.has_perm("auth.delete_group")

        # Situation we didn't handle, but better not give permission.
        # Sane defaults etc...
        return False
