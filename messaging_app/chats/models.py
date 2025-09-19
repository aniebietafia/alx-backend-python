import uuid

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = 'admin', 'Admin'
        GUEST = 'guest', 'Guest'
        HOST = 'host', 'Host'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_index=True)
    first_name = models.CharField(max_length=150, blank=False)
    last_name = models.CharField(max_length=150, blank=False)
    email = models.EmailField(unique=True, blank=False)
    phone_number = models.CharField(max_length=20, null=True, blank=False)
    role = models.CharField(max_length=10, choices=Role.choices, default=Role.GUEST)
    created_at = models.DateTimeField(auto_now_add=True)

    username = None  # Remove username field
    USERNAME_FIELD = 'email'  # Use email as the unique identifier
    REQUIRED_FIELDS = ['first_name', 'last_name']  # Fields required when creating a superuser

    def __str__(self):
        return self.email

class Conversation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_index=True)
    participants = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='conversations')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Conversation {self.id}"

class Message(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_index=True)
    conversation = models.ForeignKey(Conversation, related_name='messages', on_delete=models.CASCADE)
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='sent_messages', on_delete=models.CASCADE)
    message_body = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message {self.id} in Conversation {self.conversation.id} by {self.sender.email}"

    class Meta:
        ordering = ['sent_at']
