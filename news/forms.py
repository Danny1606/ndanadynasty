from django import forms
from .models import FamilyNews, Notification

class FamilyNewsForm(forms.ModelForm):
    class Meta:
        model = FamilyNews
        fields = ["title", "content", "author"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter post title"}),
            "content": forms.Textarea(attrs={"class": "form-control", "rows": 4, "placeholder": "Write your update here..."}),
            "author": forms.TextInput(attrs={"class": "form-control", "placeholder": "Your name"}),
        }

class NotificationForm(forms.ModelForm):
    class Meta:
        model = Notification
        fields = ["message", "date"]
        widgets = {
            "message": forms.TextInput(attrs={"class": "form-control", "placeholder": "Upcoming event details"}),
            "date": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
        }
