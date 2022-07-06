from rest_framework.response import Response
from .models import Ticket, Message
from .serializers import TicketSerializer, MessageSerializer
from rest_framework import generics, permissions
from .permissions import IsOwnerOrStaff


class TicketListAPI(generics.ListCreateAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # QuerySet в зависимости от is_staff и статуса запроса
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
        # Подгрузка сообщений для тикета
        messages = Message.objects.filter(ticket_id=response.data['id']).order_by('pub_date')
        message_serializer = MessageSerializer(messages, many=True)

        return Response({'ticket': response.data, 'messages': message_serializer.data})


class MessageTicketAPI(generics.CreateAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]
