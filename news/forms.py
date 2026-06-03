from django import forms
from .models import Post, Comment, Event

class PostForm(forms.ModelForm):
    author_name = forms.CharField(
        max_length=100,
        required=False,
        label="Your Name (optional)",
        help_text="Leave blank to post anonymously"
    )

    class Meta:
        model = Post
        fields = ['author_name', 'content', 'image']
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
        fields = ['author_name', 'text']
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
