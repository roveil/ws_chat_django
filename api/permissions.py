from rest_framework import permissions
from api.models import Message
from rest_framework.exceptions import NotFound

class UserAccessPermission(permissions.BasePermission):
    allowed_methods = ['HEAD', 'OPTIONS', 'POST']

    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True
        if request.method in self.allowed_methods:
            return True
        return False

class MessagesAccessPermission(permissions.BasePermission):
    safe_methods = ['GET', 'POST', 'OPTIONS', 'HEAD']
    unsafe_methods = ['DELETE', 'PUT']

    def has_permission(self, request, view):
        if request.user.is_anonymous:
            return False
        if request.user.is_superuser:
            return True
        if request.method in self.safe_methods:
            return True
        if request.method in self.unsafe_methods:
            #If User is owner of message
            try:
                return request.user == Message.objects.get(pk=view.kwargs['pk']).user
            except:
                raise NotFound("Message not found!")
        return False