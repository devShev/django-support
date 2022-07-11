from rest_framework import permissions
from rest_framework.generics import get_object_or_404

from support_app.models import Ticket


class IsOwnerOrStaff(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return bool(obj.author == request.user) or bool(request.user and request.user.is_staff)


class IsTicketOwnerOrStaff(permissions.BasePermission):

    def has_permission(self, request, view):
        ticket_id = view.kwargs['pk']
        ticket = get_object_or_404(Ticket.objects.get_queryset(), pk=ticket_id)
        return bool(request.user.is_staff) or bool(ticket.author == request.user)
