from django.forms import ModelForm
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from .models import Event, Speaker, Category, Participant, Message


class EventForm(ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description', 'image', 'date', 'start_time', 'end_time', 'location', 'speakers', 'category']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Event Title'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'Event Date'}),
            'start_time': forms.TimeInput(attrs={'class': 'form-control', 'placeholder': 'Event Starting Time'}),
            'end_time': forms.TimeInput(attrs={'class': 'form-control', 'placeholder': 'Event Ending Time'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Event Location'}),
            'speakers': forms.SelectMultiple(attrs={'class': 'form-control', 'placeholder': 'Event Speakers'}),
            'category': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Event Category'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Event Description'}),
        }

    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        self.fields['speakers'].queryset = Speaker.objects.all()
        self.fields['category'].queryset = Category.objects.all()


class CategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Category Name'}),
        }

    def __init__(self, *args, **kwargs):
        super(CategoryForm, self).__init__(*args, **kwargs)
        self.fields['name'].queryset = Category.objects.all()


class SpeakerForm(ModelForm):
    class Meta:
        model = Speaker
        fields = ['presenter', 'bio']
        widgets = {
            'presenter': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Speaker Name'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Speaker Bio'}),
        }

    def __init__(self, *args, **kwargs):
        super(SpeakerForm, self).__init__(*args, **kwargs)
        self.fields['presenter'].queryset = Speaker.objects.all()


class SpeakerUpdateForm(ModelForm):
    class Meta:
        model = Speaker
        is_speaking = forms.BooleanField(widget=forms.CheckboxInput)
        fields = ['title', 'bio', 'image', 'is_speaking']

    def __init__(self, *args, **kwargs):
        super(SpeakerUpdateForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Your job title'})
        self.fields['bio'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Your Bio'})
        self.fields['is_speaking'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Are you speaking?'})
        self.fields['image'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Profile Picture'})


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=100, required=True)
    last_name = forms.CharField(max_length=100, required=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2', ]

    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Username'})
        self.fields['first_name'].widget.attrs.update({'class': 'form-control', 'placeholder': 'First Name'})
        self.fields['last_name'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Last Name'})
        self.fields['email'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Email'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Password'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Confirm Password'})


class UserLoginForm(forms.Form):
    username = forms.CharField(max_length=100, min_length=3, strip=True)
    password = forms.CharField(max_length=256, widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Username'})
        self.fields['password'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Password'})


class UserUpdateForm(ModelForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=100, required=True)
    last_name = forms.CharField(max_length=100, required=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

    def __init__(self, *args, **kwargs):
        super(UserUpdateForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Username'})
        self.fields['first_name'].widget.attrs.update({'class': 'form-control', 'placeholder': 'First Name'})
        self.fields['last_name'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Last Name'})
        self.fields['email'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Email'})


class ParticipantUpdateForm(ModelForm):
    class Meta:
        model = Participant
        fields = ['image', ]

    def __init__(self, *args, **kwargs):
        super(ParticipantUpdateForm, self).__init__(*args, **kwargs)
        self.fields['image'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Profile Picture'})


class ParticipantForm(ModelForm):
    class Meta:
        model = Participant
        fields = ['attendant', 'image']


class MessageForm(ModelForm):
    class Meta:
        model = Message
        fields = ['sender_name', 'sender_email', 'content']

    def __init__(self, *args, **kwargs):
        super(MessageForm, self).__init__(*args, **kwargs)
        self.fields['sender_name'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Your Full Name'})
        self.fields['sender_email'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Your Email'})
        self.fields['content'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Your Message'})
