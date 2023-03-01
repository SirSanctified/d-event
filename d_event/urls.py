"""d_event URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, re_path
from django.contrib.auth.urls import views as auth_views
from django.views.generic import RedirectView

from d_event import settings
from d_event.settings import DEBUG
from main import views

favicon_view = RedirectView.as_view(url='/static/images/favicon.ico', permanent=True)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('events/', views.EventListView.as_view(), name='events'),
    path('event_list/', views.ModEventListView.as_view(), name='events_list'),
    path('events/<int:pk>/', views.EventDetailView.as_view(), name='event_detail'),
    path('events/new/', views.EventCreateView.as_view(), name='event_create'),
    path('events/<int:pk>/update/', views.EventUpdateView.as_view(), name='event_update'),
    path('events/<int:pk>/delete/', views.EventDeleteView.as_view(), name='event_delete'),
    path('participants/', views.ParticipantListView.as_view(), name='participants'),
    path('participants/<int:pk>/delete/', views.ParticipantDeleteView.as_view(), name='participant_delete'),
    path('participants/<int:pk>/', views.ParticipantProfileView.as_view(), name='participant_profile'),
    path('accounts/register/', views.UserRegisterView.as_view(), name='register'),
    path('accounts/login/', views.user_login, name='login'),
    path('accounts/logout/', views.UserLogoutView.as_view(), name='logout'),
    path('categories/', views.CategoryListView.as_view(), name='categories'),
    path('categories/new/', views.CategoryCreateView.as_view(), name='category_create'),
    path('categories/<int:pk>/update/', views.CategoryUpdateView.as_view(), name='category_update'),
    path('categories/<int:pk>/delete/', views.CategoryDeleteView.as_view(), name='category_delete'),
    path('speakers/', views.SpeakerListView.as_view(), name='speakers'),
    path('speakers/<int:pk>/', views.SpeakerProfileView.as_view(), name='speaker_profile'),
    path('speakers/new/', views.SpeakerCreateView.as_view(), name='speaker_create'),
    path('speakers/<int:pk>/update/', views.SpeakerUpdateView.as_view(), name='speaker_update'),
    path('speakers/<int:pk>/delete/', views.SpeakerDeleteView.as_view(), name='speaker_delete'),
    path('moderators/<int:pk>/', views.ModeratorProfileView.as_view(), name='mod_profile'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('events/<int:event_id>/register/', views.register_for_event, name='register_for_event'),
    path('events/<int:event_id>/unregister/', views.unregister_from_event, name='unregister_from_event'),
    path('messages/', views.MessageListView.as_view(), name='messages'),
    path('messages/<int:pk>/', views.MessageDetailView.as_view(), name='message_detail'),
    path('contact/', views.MessageCreateView.as_view(), name='contact'),
    path('messages/<int:pk>/delete/', views.MessageDeleteView.as_view(), name='message_delete'),
    path('about/', views.about, name='about'),
    re_path(r'^favicon\.ico$', favicon_view),
]

if DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
