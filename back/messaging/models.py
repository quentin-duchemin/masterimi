from django.contrib.auth.models import User
from django.db import models


class Conversation(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Message(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    text = models.TextField()

    conversations = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='conversations')



