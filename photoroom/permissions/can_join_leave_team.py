from rest_framework import permissions
from rest_framework.request import Request


class CanJoinLeaveTeam(permissions.BasePermission):
    def has_permission(self, request: Request, view) -> bool:
        if not request.user or not request.user.is_authenticated:
            return False

        return request.user.has_perm("auth.change_group")
