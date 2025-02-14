from django import forms
from django.forms import ModelForm
from .models import Task

from django.contrib.auth.models import User

class CustomRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean(self):
        cleaned_data = super().clean()
        if User.objects.filter(username=cleaned_data["username"]).exists():
            raise forms.ValidationError("The username is taken, please try another one")
        
        
class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'completed']  # Include only 'title' and 'completed' fields in the form

    title = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control form-control-lg",
                "placeholder": "What’s on your mind today?",
            }
        ),
    )
    completed = forms.BooleanField(
        required=False,
        widget=forms.widgets.CheckboxInput(attrs={"class": "form-check-input"}),
    )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)  # Retrieve user from kwargs
        super(TaskForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super(TaskForm, self).save(commit=False)
        if self.user:
            instance.user = self.user  # Assign the user to the task instance
        if commit:
            instance.save()
        return instance