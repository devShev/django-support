from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied, ValidationError

from .models import Message, Ticket, TicketStatus
from .tasks import send_status_to_mail


class TicketSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    author_id = serializers.IntegerField(read_only=True)
    subject = serializers.CharField(max_length=100)
    description = serializers.CharField(max_length=500)
    status = serializers.CharField(max_length=10, required=False)
    created_date = serializers.DateTimeField(read_only=True)

    def create(self, validated_data):
        # Current user as author
        validated_data.update({'author_id': self.context['request'].user.pk})

        return Ticket.objects.create(**validated_data)

    def update(self, instance, validated_data):
        if not self.context['request'].user.is_staff:
            raise PermissionDenied

        start_status = instance.status

        instance.subject = validated_data.get('subject', instance.subject)
        instance.description = validated_data.get('description', instance.description)
        instance.status = validated_data.get('status', instance.status)

        if instance.status not in [i[0] for i in TicketStatus.choices]:
            raise ValidationError('Invalid status.')

        instance.save()

        if start_status != instance.status:
            send_status_to_mail.delay(instance.status, instance.author.email)

        return instance


class MessageSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    ticket_id = serializers.IntegerField(read_only=True)
    author_id = serializers.IntegerField(read_only=True)
    message = serializers.CharField(max_length=500)
    pub_date = serializers.DateTimeField(read_only=True)

    def create(self, validated_data):
        # View for get 'pk'
        view = self.context.get('view')
        ticket_id = view.kwargs['pk']

        # Current user as author of message
        validated_data.update({'author_id': self.context['request'].user.pk})
        # 'pk' from view as 'ticket_id'
        validated_data.update({'ticket_id': ticket_id})

        return Message.objects.create(**validated_data)
