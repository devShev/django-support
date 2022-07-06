from rest_framework import permissions


class IsOwnerOrStaff(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return bool(obj.author == request.user) or bool(request.user and request.user.is_staff)
