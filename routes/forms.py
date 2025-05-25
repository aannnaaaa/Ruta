from django import forms
from .models import Route, RoutePoint

class RouteStep1Form(forms.ModelForm):
    class Meta:
        model = Route
        fields = ['title', 'description', 'photo']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Например: Выходные в горах'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Расскажите о маршруте...'
            }),
            'photo': forms.ClearableFileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            })
        }

class RoutePointForm(forms.ModelForm):
    class Meta:
        model = RoutePoint
        fields = ['name', 'point_type', 'address', 'description', 'photo']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Например: Смотровая площадка'
            }),
            'point_type': forms.Select(attrs={
                'class': 'form-control'
            }),
            'address': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Улица, город...'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Что особенного в этом месте?'
            }),
            'photo': forms.ClearableFileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            })
        }

class RouteStep3Form(forms.ModelForm):
    class Meta:
        model = Route
        fields = ['travel_date', 'route_type']
        widgets = {
            'travel_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),
            'route_type': forms.Select(attrs={
                'class': 'form-control'
            })
        }