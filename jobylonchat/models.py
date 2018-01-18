from django.db import models
from django.contrib.auth.models import User

class Message(models.Model):
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="messages_from")
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="messages_to")
    message = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('created',)
