from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth import get_user_model
from .models import Conversation, Message

User = get_user_model()


class ConversationViewSetTestCase(APITestCase):
    """Test cases for ConversationViewSet"""

    def setUp(self):
        """Set up test users and conversations"""
        self.client = APIClient()

        # Create test users
        self.user1 = User.objects.create_user(
            email='user1@test.com',
            password='testpass123',
            first_name='User',
            last_name='One'
        )
        self.user2 = User.objects.create_user(
            email='user2@test.com',
            password='testpass123',
            first_name='User',
            last_name='Two'
        )
        self.user3 = User.objects.create_user(
            email='user3@test.com',
            password='testpass123',
            first_name='User',
            last_name='Three'
        )

        # Create a test conversation
        self.conversation = Conversation.objects.create()
        self.conversation.participants.set([self.user1, self.user2])

    def test_list_conversations_authenticated(self):
        """Test listing conversations for authenticated user"""
        self.client.force_authenticate(user=self.user1)
        url = reverse('conversation-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_list_conversations_unauthenticated(self):
        """Test listing conversations without authentication fails"""
        url = reverse('conversation-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_conversation_with_valid_participants(self):
        """Test creating a new conversation with valid participant emails"""
        self.client.force_authenticate(user=self.user1)
        url = reverse('conversation-list')
        data = {
            'participants': ['user2@test.com', 'user3@test.com']
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Conversation.objects.count(), 2)

        # Verify all participants are included (including the creator)
        new_conversation = Conversation.objects.get(
            conversation_id=response.data['conversation_id']
        )
        self.assertEqual(new_conversation.participants.count(), 3)
        self.assertIn(self.user1, new_conversation.participants.all())

    def test_create_conversation_with_invalid_email(self):
        """Test creating conversation with non-existent user email"""
        self.client.force_authenticate(user=self.user1)
        url = reverse('conversation-list')
        data = {
            'participants': ['nonexistent@test.com']
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('Users not found', response.data['error'])

    def test_create_conversation_with_invalid_format(self):
        """Test creating conversation with invalid participants format"""
        self.client.force_authenticate(user=self.user1)
        url = reverse('conversation-list')
        data = {
            'participants': 'not-a-list'
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('must be a list', response.data['error'])

    def test_retrieve_conversation_as_participant(self):
        """Test retrieving a conversation as a participant"""
        self.client.force_authenticate(user=self.user1)
        url = reverse('conversation-detail', kwargs={'pk': self.conversation.conversation_id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data['conversation_id'],
            str(self.conversation.conversation_id)
        )

    def test_retrieve_conversation_as_non_participant(self):
        """Test retrieving a conversation as non-participant fails"""
        self.client.force_authenticate(user=self.user3)
        url = reverse('conversation-detail', kwargs={'pk': self.conversation.conversation_id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_filter_conversations_by_participant(self):
        """Test filtering conversations by participant email"""
        # Create another conversation
        conversation2 = Conversation.objects.create()
        conversation2.participants.set([self.user1, self.user3])

        self.client.force_authenticate(user=self.user1)
        url = reverse('conversation-list')
        response = self.client.get(url, {'participants__email': 'user2@test.com'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_search_conversations(self):
        """Test searching conversations by participant name"""
        self.client.force_authenticate(user=self.user1)
        url = reverse('conversation-list')
        response = self.client.get(url, {'search': 'User Two'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)


class MessageViewSetTestCase(APITestCase):
    """Test cases for MessageViewSet"""

    def setUp(self):
        """Set up test users, conversations, and messages"""
        self.client = APIClient()

        # Create test users
        self.user1 = User.objects.create_user(
            email='user1@test.com',
            password='testpass123',
            first_name='User',
            last_name='One'
        )
        self.user2 = User.objects.create_user(
            email='user2@test.com',
            password='testpass123',
            first_name='User',
            last_name='Two'
        )
        self.user3 = User.objects.create_user(
            email='user3@test.com',
            password='testpass123',
            first_name='User',
            last_name='Three'
        )

        # Create conversations
        self.conversation = Conversation.objects.create()
        self.conversation.participants.set([self.user1, self.user2])

        # Create test messages
        self.message1 = Message.objects.create(
            conversation=self.conversation,
            sender=self.user1,
            message_body='Hello from user1'
        )
        self.message2 = Message.objects.create(
            conversation=self.conversation,
            sender=self.user2,
            message_body='Reply from user2'
        )

    def test_list_messages_as_participant(self):
        """Test listing messages in a conversation as participant"""
        self.client.force_authenticate(user=self.user1)
        url = reverse('conversation-message-list', kwargs={
            'conversation_pk': self.conversation.conversation_id
        })
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)

    def test_list_messages_as_non_participant(self):
        """Test listing messages as non-participant returns empty"""
        self.client.force_authenticate(user=self.user3)
        url = reverse('conversation-message-list', kwargs={
            'conversation_pk': self.conversation.conversation_id
        })
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 0)

    def test_create_message_as_participant(self):
        """Test creating a message as conversation participant"""
        self.client.force_authenticate(user=self.user1)
        url = reverse('conversation-message-list', kwargs={
            'conversation_pk': self.conversation.conversation_id
        })
        data = {
            'message_body': 'New test message'
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Message.objects.count(), 3)
        self.assertEqual(response.data['sender']['email'], 'user1@test.com')

    def test_create_message_with_empty_body(self):
        """Test creating message with empty body fails"""
        self.client.force_authenticate(user=self.user1)
        url = reverse('conversation-message-list', kwargs={
            'conversation_pk': self.conversation.conversation_id
        })
        data = {
            'message_body': ''
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_message_in_nonexistent_conversation(self):
        """Test creating message in non-existent conversation"""
        self.client.force_authenticate(user=self.user1)
        fake_uuid = '00000000-0000-0000-0000-000000000000'
        url = reverse('conversation-message-list', kwargs={
            'conversation_pk': fake_uuid
        })
        data = {
            'message_body': 'Test message'
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_message_as_participant(self):
        """Test retrieving a specific message as participant"""
        self.client.force_authenticate(user=self.user1)
        url = reverse('conversation-message-detail', kwargs={
            'conversation_pk': self.conversation.conversation_id,
            'pk': self.message1.message_id
        })
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message_body'], 'Hello from user1')

    def test_filter_messages_by_sender(self):
        """Test filtering messages by sender email"""
        self.client.force_authenticate(user=self.user1)
        url = reverse('conversation-message-list', kwargs={
            'conversation_pk': self.conversation.conversation_id
        })
        response = self.client.get(url, {'sender__email': 'user2@test.com'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(
            response.data['results'][0]['sender']['email'],
            'user2@test.com'
        )

    def test_search_messages(self):
        """Test searching messages by content"""
        self.client.force_authenticate(user=self.user1)
        url = reverse('conversation-message-list', kwargs={
            'conversation_pk': self.conversation.conversation_id
        })
        response = self.client.get(url, {'search': 'Reply'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertIn('Reply', response.data['results'][0]['message_body'])

    def test_ordering_messages_by_sent_at(self):
        """Test ordering messages by sent_at timestamp"""
        self.client.force_authenticate(user=self.user1)
        url = reverse('conversation-message-list', kwargs={
            'conversation_pk': self.conversation.conversation_id
        })
        response = self.client.get(url, {'ordering': '-sent_at'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Most recent message should be first when descending
        self.assertEqual(
            response.data['results'][0]['message_id'],
            str(self.message2.message_id)
        )

    def test_unauthenticated_access_denied(self):
        """Test unauthenticated access to messages is denied"""
        url = reverse('conversation-message-list', kwargs={
            'conversation_pk': self.conversation.conversation_id
        })
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_pagination_works(self):
        """Test that pagination is applied to message list"""
        # Create more messages
        for i in range(15):
            Message.objects.create(
                conversation=self.conversation,
                sender=self.user1,
                message_body=f'Message {i}'
            )

        self.client.force_authenticate(user=self.user1)
        url = reverse('conversation-message-list', kwargs={
            'conversation_pk': self.conversation.conversation_id
        })
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('count', response.data)
        self.assertIn('next', response.data)
        self.assertIn('previous', response.data)
