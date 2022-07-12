from rest_framework import generics, permissions
from rest_framework.response import Response

from .models import Message, Ticket
from .permissions import IsOwnerOrStaff, IsTicketOwnerOrStaff
from .serializers import MessageSerializer, TicketSerializer
from .tasks import send_status_to_mail


class TicketListAPI(generics.ListCreateAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # QuerySet in depending on 'is_staff' and request
        if self.request.user.is_staff:
            if self.request.GET.get('status', False):
                return Ticket.objects.filter(status=self.request.GET['status'])
            return Ticket.objects.all().order_by('created_date')
        return Ticket.objects.filter(author=self.request.user).order_by('created_date')


class TicketDetailAPI(generics.RetrieveUpdateDestroyAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    permission_classes = [IsOwnerOrStaff]

    def retrieve(self, request, *args, **kwargs):
        response = super(TicketDetailAPI, self).retrieve(self, request, *args, **kwargs)
        # Upload messages for ticket
        messages = Message.objects.filter(ticket_id=response.data['id']).order_by('pub_date')
        message_serializer = MessageSerializer(messages, many=True)

        return Response({'ticket': response.data, 'messages': message_serializer.data})

    def put(self, request, *args, **kwargs):
        start_status = self.get_object().status

        self.update(request, *args, **kwargs)

        current_ticket = self.get_object()
        if current_ticket.status != start_status:
            send_status_to_mail.delay(current_ticket.status, current_ticket.author.email)

        ticket_serializer = TicketSerializer(current_ticket)

        return Response(ticket_serializer.data)

    def patch(self, request, *args, **kwargs):
        # Read start status in depending on request
        start_status = self.get_object().status if request.data.get('status', False) else None

        self.partial_update(request, *args, **kwargs)

        current_ticket = self.get_object()

        if start_status is not None:
            if current_ticket.status != start_status:
                send_status_to_mail.delay(current_ticket.status, current_ticket.author.email)

        ticket_serializer = TicketSerializer(current_ticket)

        return Response(ticket_serializer.data)


class MessageTicketAPI(generics.CreateAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsTicketOwnerOrStaff]
