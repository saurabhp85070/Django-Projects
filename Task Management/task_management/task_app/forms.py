from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'example@gmail.com'}),
    )
    password1 = forms.CharField(
        label='Password',
        strip=False,
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter a strong password'}),
    )
    password2 = forms.CharField(
        label='Password confirmation',
        widget=forms.PasswordInput(attrs={'placeholder': 'Repeat your password'}),
        strip=False,
        help_text='Enter the same password as before, for verification.',
    )

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')



# Reordering Form and View
class PositionForm(forms.Form):
    position = forms.CharField()