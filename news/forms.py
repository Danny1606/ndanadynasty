from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser, Post, Comment, Event

class CustomSignupForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, label="First Name")
    last_name = forms.CharField(max_length=150, required=False, label="Last Name")
    pin = forms.CharField(max_length=4, help_text="Enter a 4-digit PIN")
    unit = forms.CharField(max_length=100, required=False, label="Unit/Location", help_text="e.g., 'Unit A', 'Main House', 'Apartment 3B'")

    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'pin', 'unit', 'picture')


class CustomLoginForm(AuthenticationForm):
    pin = forms.CharField(max_length=4, widget=forms.PasswordInput)


class PostForm(forms.ModelForm):
    author_name = forms.CharField(
        max_length=100, 
        required=False, 
        label="Your Name (optional)",
        help_text="Leave blank to post anonymously"
    )
    
    class Meta:
        model = Post
        fields = ['content', 'image']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Share something with your family...'})
        }


class CommentForm(forms.ModelForm):
    author_name = forms.CharField(
        max_length=100, 
        required=False, 
        label="Your Name (optional)",
        help_text="Leave blank to comment anonymously"
    )
    
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Add a comment...'})
        }


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'date', 'time', 'description', 'image', 'location']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
            'description': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Event details...'}),
            'title': forms.TextInput(attrs={'placeholder': 'Event title'}),
            'location': forms.TextInput(attrs={'placeholder': 'Where?'})
        }
