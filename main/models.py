from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

User._meta.get_field('email')._unique = True


class Participant(models.Model):
    attendant = models.OneToOneField(User, related_name='participant', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='participants', null=True, blank=True)

    def __str__(self):
        return self.attendant.username


class Event(models.Model):
    title = models.CharField(max_length=255, null=False, blank=False)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='events', null=True, blank=True)
    date = models.DateField(null=False, blank=False, default=timezone.now)
    start_time = models.TimeField(null=False, blank=False, default=timezone.now)
    end_time = models.TimeField(null=False, blank=False, default=timezone.now)
    location = models.CharField(max_length=255, null=False, blank=False)
    participants = models.ManyToManyField('Participant', related_name='registered_events', blank=True)
    speakers = models.ManyToManyField('Speaker', related_name='events', )
    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='events', null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class Speaker(models.Model):
    presenter = models.OneToOneField(User, related_name='speaker', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='speakers', null=True)
    title = models.CharField(max_length=256, null=True)
    bio = models.TextField(null=True, blank=True)
    is_speaking = models.BooleanField(default=False)

    def __str__(self):
        return self.presenter.first_name + ' ' + self.presenter.last_name


class Category(models.Model):
    class Meta:
        verbose_name_plural = 'Categories'
        verbose_name = 'Category'

    name = models.CharField(max_length=255, null=False, blank=False)

    def __str__(self):
        return self.name


class Message(models.Model):
    sender_name = models.CharField(max_length=255, null=False, blank=False)
    sender_email = models.EmailField(null=False, blank=False)
    content = models.TextField(null=False, blank=False)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.sender_name
