from django import forms
from django.contrib.auth.models import User
from .models import Profile


class ProfileEditForm(forms.ModelForm):
    username = forms.CharField(max_length=150, label="Имя пользователя")
    email = forms.EmailField(label="Email")

    class Meta:
        model = Profile
        fields = ['bio']
        labels = {
            'bio': 'Биография',
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['username'].initial = user.username
            self.fields['email'].initial = user.email

    def save(self, commit=True):
        profile = super().save(commit=False)
        user = profile.user
        user.username = self.cleaned_data['username']
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            profile.save()
        return profile