from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsProjectOwner(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return super().has_permission(request, view)
    def has_object_permission(self, request, view, obj):
        return super().has_object_permission(request, view, obj)

class IsProjectLead(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user.is_authenticated and request.user.role.lower() == 'lead'

    def has_object_permission(self, request, view, obj):
        return request.user.role.lower() == 'lead'