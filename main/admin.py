from django.contrib import admin
from .models import Event, Participant, Speaker, Category, Message


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'start_time', 'end_time', 'location')
    list_filter = ('date', 'start_time', 'category')
    search_fields = ('title', 'location', 'category__name')
    ordering = ('start_time', 'end_time')
    filter_horizontal = ('speakers',)


@admin.register(Participant)
class ParticipantAdmin(admin.ModelAdmin):
    list_display = ('attendant', )
    search_fields = ('attendant__username',)
    ordering = ('attendant',)


@admin.register(Speaker)
class SpeakerAdmin(admin.ModelAdmin):
    list_display = ('presenter', 'is_speaking')
    list_filter = ('is_speaking',)
    search_fields = ('presenter__username',)
    ordering = ('presenter',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ('name',)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender_name', 'sender_email', 'date')
    search_fields = ('sender_name', 'sender_email')
    ordering = ('date',)
