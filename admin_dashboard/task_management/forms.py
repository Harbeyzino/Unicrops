from django import forms
from .models import Task, SubTask, TaskProgress, Comment
from django.contrib.auth import get_user_model

User = get_user_model()

class TaskForm(forms.ModelForm):
    assigned_to = forms.EmailField(required=False)
    
    class Meta:
        model = Task
        fields = ['title', 'description', 'time_value', 'time_unit', 'assigned_to']
    
    def clean_assigned_to(self):
        email = self.cleaned_data.get('assigned_to')
        if email:
            try:
                return User.objects.get(email=email)
            except User.DoesNotExist:
                raise forms.ValidationError("User with this email does not exist.")
        return None

class SubTaskForm(forms.ModelForm):
    class Meta:
        model = SubTask
        fields = ['title', 'description']

class ProgressForm(forms.ModelForm):
    class Meta:
        model = TaskProgress
        fields = ['status', 'notes', 'proof']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']