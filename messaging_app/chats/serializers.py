from rest_framework import serializers
from .models import User, Conversation, Message

class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the User model.
    """
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'phone_number', 'role']
        read_only_fields = ['id', 'role']

class MessageSerializer(serializers.ModelSerializer):
    """
    Serializer for the Message model.
    The sender is represented by their email address.
    """
    sender = serializers.SlugRelatedField()

    class Meta:
        model = Message
        fields = ['id', 'conversation', 'sender', 'message_body', 'sent_at']
        read_only_fields = ['id', 'sent_at']

class ConversationSerializer(serializers.ModelSerializer):
    """
    Serializer for the Conversation model.
    Includes nested serialization participants and messages.
    """
    messages = MessageSerializer(many=True, read_only=True)
    participants = UserSerializer(many=True, read_only=True)

    class Meta:
        model = Conversation
        read_only_fields = ['id', 'created_at', 'messages', 'participants']