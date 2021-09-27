from rest_framework import permissions
from account.models import AccessToEdit
from django.contrib.auth.models import User


class AccessPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        try:
            if request.method == "POST":
                user = User.objects.get(auth_token=request.data['token'])
            else:
                user = User.objects.get(auth_token=request.headers['Token'])
        except:
            return False
        if request.method == "GET":
            return True
        else:
            if user.groups.filter(id=6).exists() or AccessToEdit.objects.filter(
                    school_id=user.libraryuser.school.id, edit_status=1).exists():
                return True
            else:
                return False


class HeadlibrianPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.groups.filter(id__in=[1, 6]).exists()


class HeadlibrianPermissionByPosition(permissions.BasePermission):

    def has_permission(self, request, view):
        from . import user_utils
        return user_utils.user_schools(request.user).filter(positions__in=[
            user_utils.LIBRARIAN,
            user_utils.LIBRARIAN_ZAM
        ]).exists() or request.user.is_superuser



class SuperUserPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.is_superuser

class AccessPermissionS12(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user:
            if AccessToEdit.objects.filter(
                    school_id=request.user.libraryuser.school.id, status_12=1).exists():
                return True
            else:
                return False
        else:
            try:
                if request.method == "POST":
                    user = User.objects.get(auth_token=request.data['token'])
                else:
                    user = User.objects.get(auth_token=request.headers['Token'])
            except:
                return False
            if request.method == "GET":
                return True
            else:
                if user.groups.filter(id=6).exists() or AccessToEdit.objects.filter(
                        school_id=user.libraryuser.school.id, edit_status=1, edit_status_12=1).exists():
                    return True
                else:
                    return False
