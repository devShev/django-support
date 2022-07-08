from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers
from rest_framework.exceptions import ValidationError, PermissionDenied, NotFound

from .models import Ticket, TicketStatus, Message
from .tasks import send_status_to_mail


class TicketSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    author_id = serializers.IntegerField(read_only=True)
    subject = serializers.CharField(max_length=100)
    description = serializers.CharField(max_length=500)
    status = serializers.CharField(max_length=10, required=False)
    created_date = serializers.DateTimeField(read_only=True)

    def create(self, validated_data):
        # Текущий пользователь как автор
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
            send_status_to_mail(instance)

        return instance


class MessageSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    ticket_id = serializers.IntegerField(read_only=True)
    author_id = serializers.IntegerField(read_only=True)
    message = serializers.CharField(max_length=500)
    pub_date = serializers.DateTimeField(read_only=True)

    def create(self, validated_data):
        # Вьюшка для получения значения 'pk'
        view = self.context.get('view')
        ticket_id = view.kwargs['pk']

        try:
            ticket = Ticket.objects.get(pk=ticket_id)
        except ObjectDoesNotExist:
            raise NotFound

        if not (self.context['request'].user.is_staff or ticket.author == self.context['request'].user):
            raise PermissionDenied

        # Текущий пользователь как автор сообщения
        validated_data.update({'author_id': self.context['request'].user.pk})
        # pk из вьюшки как ticket_id
        validated_data.update({'ticket_id': ticket_id})

        return Message.objects.create(**validated_data)
