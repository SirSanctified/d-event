from datetime import datetime
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LogoutView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django_filters.views import FilterView

from .forms import EventForm, CategoryForm, SpeakerForm, UserRegisterForm, UserUpdateForm, \
    UserLoginForm, SpeakerUpdateForm, ParticipantUpdateForm, MessageForm
from .models import Event, Category, Speaker, Participant, Message
from .filters import EventFilter, MessageFilter


class EventListView(ListView, FilterView):
    model = Event
    template_name = 'main/events.html'
    context_object_name = 'events'
    ordering = ['-date']
    paginate_by = 15

    def get_queryset(self):
        queryset = super().get_queryset()
        filter = EventFilter(self.request.GET, queryset)
        return filter.qs

    def get_context_data(self, **kwargs):
        context = super(EventListView, self).get_context_data(**kwargs)
        filter = EventFilter(self.request.GET)
        context['filter'] = filter
        return context


class ModEventListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Event
    template_name = 'main/event_list.html'
    context_object_name = 'events'
    ordering = ['-date']
    login_url = reverse_lazy('login')
    paginate_by = 15

    def get_queryset(self):
        queryset = super().get_queryset()
        filter = EventFilter(self.request.GET, queryset)
        return filter.qs

    def get_context_data(self, **kwargs):
        context = super(ModEventListView, self).get_context_data(**kwargs)
        filter = EventFilter(self.request.GET)
        context['filter'] = filter
        return context

    def test_func(self):
        return self.request.user.groups.filter(name='mod').exists() or self.request.user.is_superuser


class EventDetailView(DetailView):
    model = Event
    template_name = 'main/event_details.html'


class EventCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Event
    template_name = 'main/event_form.html'
    form_class = EventForm
    permission_required = 'main.add_event'
    success_url = reverse_lazy('events_list')
    login_url = reverse_lazy('login')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class EventUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Event
    template_name = 'main/event_form.html'
    form_class = EventForm
    permission_required = 'main.change_event'
    login_url = reverse_lazy('login')
    success_url = reverse_lazy('events_list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class EventDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Event
    template_name = 'main/event_confirm_delete.html'
    permission_required = 'main.delete_event'
    login_url = reverse_lazy('login')
    success_url = reverse_lazy('events_list')


class ModeratorProfileView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = User
    template_name = 'main/mod_profile.html'
    login_url = reverse_lazy('login')
    context_object_name = 'user'
    fields = '__all__'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['events'] = Event.objects.all()
        context['participants'] = Participant.objects.all()
        context['speakers'] = Speaker.objects.all()
        context['categories'] = Category.objects.all()
        context['u_form'] = UserUpdateForm(instance=self.request.user)
        return context

    def test_func(self):
        return self.request.user == User.objects.get(id=self.kwargs['pk'])

    def post(self, request, *args, **kwargs):
        u_form = UserUpdateForm(self.request.POST, instance=self.request.user)

        if u_form.is_valid():
            u_form.save()
            messages.success(request, 'Your profile has been updated successfully')
            return redirect('mod_profile', self.request.user.id)


class ParticipantProfileView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = User
    template_name = 'main/participant_profile.html'
    context_object_name = 'user'
    fields = '__all__'
    login_url = reverse_lazy('login')
    success_url = reverse_lazy('participant_profile')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['u_form'] = UserUpdateForm(instance=self.request.user)
        context['p_form'] = ParticipantUpdateForm(instance=self.request.user.participant)
        return context

    def post(self, request, *args, **kwargs):
        u_form = UserUpdateForm(self.request.POST, instance=self.request.user)
        p_form = ParticipantUpdateForm(self.request.POST, self.request.FILES, instance=self.request.user.participant)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Your profile has been updated successfully')
            return redirect('participant_profile', self.request.user.id)

    def test_func(self):
        return self.request.user == User.objects.get(id=self.kwargs['pk'])


class SpeakerProfileView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = User
    template_name = 'main/speaker_profile.html'
    login_url = reverse_lazy('login')
    context_object_name = 'user'
    fields = '__all__'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['u_form'] = UserUpdateForm(instance=self.request.user)
        context['s_form'] = SpeakerUpdateForm(instance=self.request.user.speaker)
        return context

    def post(self, request, *args, **kwargs):
        u_form = UserUpdateForm(self.request.POST, instance=self.request.user)
        s_form = SpeakerUpdateForm(self.request.POST, self.request.FILES, instance=self.request.user.speaker)

        if u_form.is_valid() and s_form.is_valid():
            u_form.save()
            s_form.save()
            messages.success(request, 'Your profile has been updated successfully')
            return redirect('speaker_profile', self.request.user.id)

    def test_func(self):
        return self.request.user == User.objects.get(id=self.kwargs['pk'])


class CategoryListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Category
    template_name = 'main/categories.html'
    context_object_name = 'categories'
    login_url = reverse_lazy('login')
    ordering = ['name']
    paginate_by = 15

    def test_func(self):
        return self.request.user.groups.filter(name='mod').exists() or self.request.user.is_superuser


class CategoryCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Category
    template_name = 'main/category_form.html'
    form_class = CategoryForm
    permission_required = 'main.add_category'
    login_url = reverse_lazy('login')
    success_url = reverse_lazy('categories')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class CategoryUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Category
    template_name = 'main/category_form.html'
    form_class = CategoryForm
    permission_required = 'main.change_category'
    login_url = reverse_lazy('login')
    success_url = reverse_lazy('categories')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class CategoryDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Category
    template_name = 'main/category_confirm_delete.html'
    permission_required = ('main.change_category', 'main.delete_category')
    login_url = reverse_lazy('login')
    success_url = reverse_lazy('categories')


class SpeakerListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Speaker
    template_name = 'main/speakers.html'
    context_object_name = 'speakers'
    login_url = reverse_lazy('login')
    ordering = ['id']
    paginate_by = 15

    def test_func(self):
        return self.request.user.groups.filter(name='mod').exists() or self.request.user.is_superuser


class SpeakerCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Speaker
    template_name = 'main/speaker_form.html'
    form_class = SpeakerForm
    login_url = reverse_lazy('login')
    permission_required = 'main.add_speaker'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class SpeakerUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Speaker
    template_name = 'main/speaker_form.html'
    form_class = SpeakerUpdateForm
    permission_required = ('main.view_speaker', 'main.change_speaker')
    login_url = reverse_lazy('login')
    success_url = reverse_lazy('speakers')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        return self.request.user.groups.filter(name='mod').exists() or self.request.user.is_superuser


class SpeakerDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Speaker
    template_name = 'main/speaker_confirm_delete.html'
    permission_required = ('main.change_speaker', 'main.delete_speaker')
    login_url = reverse_lazy('login')
    success_url = reverse_lazy('speakers')


class ParticipantListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Participant
    template_name = 'main/participants.html'
    login_url = reverse_lazy('login')
    context_object_name = 'participants'
    ordering = ['id']
    paginate_by = 15

    def test_func(self):
        return self.request.user.groups.filter(name='mod').exists() or self.request.user.is_superuser


class ParticipantDeleteView(LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin, DeleteView):
    permission_required = 'main.delete_participant'
    model = Participant
    login_url = reverse_lazy('login')
    template_name = 'main/participant_confirm_delete.html'

    def get_success_url(self):
        if self.request.user.groups.filter(name='mod').exists():
            return redirect('mod_profile', self.request.user.id)
        return reverse_lazy('home')

    def test_func(self):
        return self.request.user.participant == Participant.objects.get(id=self.kwargs['pk'])


class MessageListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Message
    template_name = 'main/messages.html'
    login_url = reverse_lazy('login')
    context_object_name = 'messages'
    ordering = ['-date']
    paginate_by = 15

    def get_queryset(self):
        queryset = super().get_queryset()
        filter = MessageFilter(self.request.GET, queryset)
        return filter.qs

    def get_context_data(self, **kwargs):
        context = super(MessageListView, self).get_context_data(**kwargs)
        filter = MessageFilter(self.request.GET)
        context['filter'] = filter
        return context

    def test_func(self):
        return self.request.user.groups.filter(name='mod').exists() or self.request.user.is_superuser


class MessageDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Message
    template_name = 'main/message_confirm_delete.html'
    login_url = reverse_lazy('login')
    success_url = reverse_lazy('messages')

    def test_func(self):
        return self.request.user.groups.filter(name='mod').exists() or self.request.user.is_superuser


class MessageDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Message
    login_url = reverse_lazy('login')
    template_name = 'main/message_detail.html'

    def test_func(self):
        return self.request.user.groups.filter(name='mod').exists() or self.request.user.is_superuser


class MessageCreateView(CreateView):
    model = Message
    template_name = 'main/message_form.html'
    form_class = MessageForm
    success_url = reverse_lazy('contact')

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, 'Your message has been sent! One of our staff will get back to you as soon as '
                                       'possible')
        return super().form_valid(form)


class UserRegisterView(CreateView):
    template_name = 'accounts/register.html'
    form_class = UserRegisterForm
    success_url = reverse_lazy('login')

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            messages.success(self.request, f'Your account has been created! You are now able to log in')
            return redirect('login')
        else:
            return render(request, self.template_name, {'form': form})


class UserLogoutView(LoginRequiredMixin, LogoutView):
    login_url = reverse_lazy('login')

    def get_success_url(self):
        return reverse_lazy('login')


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                if user.groups.filter(name='participant').exists():
                    return redirect('participant_profile', user.id)
                elif user.groups.filter(name='mod').exists() or user.is_staff:
                    return redirect('mod_profile', user.id)
                else:
                    return redirect('speaker_profile', user.id)
            else:
                messages.error(request, 'Invalid username or password')
                return render(request, 'accounts/login.html', {'form': form})
    else:
        form = UserLoginForm()
    return render(request, 'accounts/login.html', {'form': form})


def home(request):
    return render(request, 'main/index.html')


@login_required(login_url='login')
def register_for_event(request, event_id):
    event = Event.objects.get(id=event_id)
    if event.date >= datetime.now().date():
        event.participants.add(request.user.participant)
        event.save()
        messages.success(request, 'You have successfully registered for this event')
    else:
        messages.error(request, 'You cannot register for an event that has already passed')
    return redirect('event_detail', event_id)


@login_required(login_url='login')
def unregister_from_event(request, event_id):
    event = Event.objects.get(id=event_id)
    event.participants.remove(request.user.participant)
    event.save()
    messages.success(request, 'You have successfully unregistered from this event')
    return redirect('event_detail', event_id)


def about(request):
    return render(request, 'main/about.html')
