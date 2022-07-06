from rest_framework import serializers
from rest_framework.exceptions import ValidationError, PermissionDenied

from .models import Ticket, TicketStatus


class TicketSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    author_id = serializers.IntegerField(read_only=True)
    subject = serializers.CharField(max_length=100)
    description = serializers.CharField(max_length=500)
    status = serializers.CharField(max_length=10, required=False)
    created_date = serializers.DateTimeField(read_only=True)

    def create(self, validated_data):
        validated_data.update({'author_id': self.context['request'].user.pk})

        return Ticket.objects.create(**validated_data)

    def update(self, instance, validated_data):
        if not self.context['request'].user.is_staff:
            raise PermissionDenied

        instance.subject = validated_data.get('subject', instance.subject)
        instance.description = validated_data.get('description', instance.description)
        instance.status = validated_data.get('status', instance.status)

        if instance.status not in [i[0] for i in TicketStatus.choices]:
            raise ValidationError('Invalid status.')

        instance.save()

        return instance


class MessageSerializer(serializers.Serializer):
    ticket_id = serializers.IntegerField(read_only=True)
    author_id = serializers.IntegerField(read_only=True)
    message = serializers.CharField(max_length=500)
    pub_date = serializers.DateTimeField(read_only=True)
