from django.urls import path, include
from rest_framework import routers
from rest_framework_nested import routers as nested_routers
from .views import UserViewSet, ConversationViewSet, MessageViewSet

router = routers.DefaultRouter()
router.register(r'users', UserViewSet, basename='user') 
router.register(r'conversations', ConversationViewSet, basename='conversation')
router.register(r'messages', MessageViewSet, basename='message')

# Nested routers under users
user_nested_router = nested_routers.NestedDefaultRouter(router, r'users', lookup='user')
user_nested_router.register(r'messages', MessageViewSet, basename='user-messages')

# Nested routers under conversations
conversation_nested_router = nested_routers.NestedDefaultRouter(router, r'conversations', lookup='conversation')
conversation_nested_router.register(r'messages', MessageViewSet, basename='conversation-messages')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(user_nested_router.urls)),
    path('', include(conversation_nested_router.urls)),
]
