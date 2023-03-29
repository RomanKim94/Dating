from rest_framework.permissions import BasePermission


class IsAuthenticatedOrCreate(BasePermission):

    def has_permission(self, request, view):
        return bool(view.action == 'create' or request.user and request.user.is_authenticated)
