from django.urls import path, include
from rest_framework.routers import DefaultRouter

from messaging_app.chats.views import ConversationViewSet, MessageViewSet

router = DefaultRouter()
router.register(r'conversations', ConversationViewSet)

# URL patterns for messages within a conversation
message_list = MessageViewSet.as_view({'get': 'list', 'post': 'create'})
message_detail = MessageViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy', 'patch': 'partial_update'})

urlpatterns = [
    path('', include(router.urls)),
    path('conversations/<uuid:conversation_id>/messages/', message_list, name='conversation-messages'),
    path('conversations/<uuid:conversation_id>/messages/<uuid:pk>/', message_detail, name='message-detail'),
]