import django_filters
from django_filters import CharFilter, DateFilter

from .models import Event, Message


class EventFilter(django_filters.FilterSet):
    title = CharFilter(field_name='title', lookup_expr='icontains')
    location = CharFilter(field_name='location', lookup_expr='icontains')

    class Meta:
        model = Event
        fields = ['category', 'title', 'location']


class MessageFilter(django_filters.FilterSet):
    date_received = DateFilter(field_name='date', lookup_expr='lt')
    body = CharFilter(field_name='content', lookup_expr='icontains')

    class Meta:
        model = Message
        fields = ['sender_email', 'body', 'date_received']
