from rest_framework import permissions

from app.models import Profile


class LibrarianEditOrReadOnly(permissions.BasePermission):

    edit_methods = ("POST", "PUT", "PATCH")

    def has_permission(self, request, view):
        profile = Profile.objects.get(user=request.user)
        if profile.user_type == "librarian":
            return True
        return False