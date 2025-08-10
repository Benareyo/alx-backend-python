import django_filters
from .models import Message

class MessageFilter(django_filters.FilterSet):
    sent_at__gte = django_filters.DateTimeFilter(field_name='sent_at', lookup_expr='gte')
    sent_at__lte = django_filters.DateTimeFilter(field_name='sent_at', lookup_expr='lte')
    sender = django_filters.NumberFilter(field_name='sender__user_id')
    conversation = django_filters.NumberFilter(field_name='conversation__conversation_id')

    class Meta:
        model = Message
        fields = ['sender', 'conversation', 'sent_at__gte', 'sent_at__lte']
