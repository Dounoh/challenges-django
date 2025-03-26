from __future__ import annotations

from rest_framework.permissions import BasePermission


class IsAuthorOrAdmin(BasePermission):
    def has_permission(self, request, view):
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        else:
            return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        return request.user == obj.user or request.user.is_staff
