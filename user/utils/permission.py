# utils/permission.py
from rest_framework.permissions import BasePermission


class SVIPPermission(BasePermission):
    message = "必须是SVIP才能访问"

    def has_permission(self, request, view):
        if not request.user or hasattr(request.user, 'is_anonymous') or request.user.user_type != 3:
            return False
        return True


class VIPPermission(BasePermission):
    message = "必须高于VIP才能访问"

    def has_permission(self, request, view):
        if not request.user or hasattr(request.user, 'is_anonymous') or request.user.user_type == 1:
            return False
        return True
