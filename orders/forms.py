from django import forms
from .models import Order


class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['full_name', 'email', 'phone_number', 'address', 'city', 'state']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'w-full border rounded px-3 py-2'}),
            'email': forms.EmailInput(attrs={'class': 'w-full border rounded px-3 py-2'}),
            'phone_number': forms.TextInput(attrs={'class': 'w-full border rounded px-3 py-2'}),
            'address': forms.TextInput(attrs={'class': 'w-full border rounded px-3 py-2'}),
            'city': forms.TextInput(attrs={'class': 'w-full border rounded px-3 py-2'}),
            'state': forms.TextInput(attrs={'class': 'w-full border rounded px-3 py-2'}),
        }
