from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method is permissions.SAFE_METHODS:
            print "request.method is permissions.SAFE_METHODS", request.method is permissions.SAFE_METHODS
            return True
        print "obj.user:", obj.user
        print "request.user:", request.user
        return obj.user == request.user # True / False
        
