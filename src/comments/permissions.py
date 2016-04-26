from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        """
        This method checks whether request method has a permission
        to an object
        """
        if request.method is permissions.SAFE_METHODS:
            return True
        return obj.user == request.user
