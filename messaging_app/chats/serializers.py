from rest_framework import serializers
from .models import User, Conversation, Message

class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the User model.
    """
    class Meta:
        model = User
        fields = ['user_id', 'first_name', 'last_name', 'email', 'phone_number', 'role']
        read_only_fields = ['user_id', 'role']

class MessageSerializer(serializers.ModelSerializer):
    """
    Serializer for the Message model.
    The sender is represented by their email address.
    """
    sender = serializers.SlugRelatedField(
        read_only=True,
        slug_field='email'
    )

    class Meta:
        model = Message
        fields = ['message_id', 'conversation', 'sender', 'message_body', 'sent_at']
        read_only_fields = ['message_id', 'sent_at', 'conversation']

class ConversationSerializer(serializers.ModelSerializer):
    """
    Serializer for the Conversation model.
    Includes nested serialization participants and messages.
    """
    messages = MessageSerializer(many=True, read_only=True)
    participants = UserSerializer(many=True, read_only=True)

    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participants', 'messages', 'created_at']
        read_only_fields = ['conversation_id', 'participants', 'messages', 'created_at']
