from django.contrib import admin
from .models import Message

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    fields = (('from_user', 'to_user', 'created',), 'message')
    readonly_fields = ('created',)
    list_display = ('created', 'from_user', 'to_user', )
