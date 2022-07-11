from django.contrib import admin

from .models import Message, Ticket


class TicketAdmin(admin.ModelAdmin):
    list_display = ('id', 'subject', 'status', 'author', 'created_date')
    list_display_links = ('subject',)
    search_fields = ('subject', 'author', 'status')
    list_editable = ('status', )


class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'ticket_id', 'author', 'pub_date')
    list_display_links = ('id', )


admin.site.register(Ticket, TicketAdmin)
admin.site.register(Message, MessageAdmin)
