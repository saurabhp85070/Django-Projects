from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError
import re
from .models import UserProfile
from django.contrib.auth.forms import PasswordChangeForm


# SIGNUP FORM
class SignupForm(UserCreationForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')
        
    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update({
            'placeholder': 'First Name'
        })
        self.fields['last_name'].widget.attrs.update({
            'placeholder': 'Last Name'
        })
        self.fields['username'].widget.attrs.update({
            'placeholder': 'username should be unique and can\'t change later'
        })
        self.fields['email'].widget.attrs.update({
            'placeholder': 'enter only valid email. example: demo@gmail.com'
        })
        self.fields['password1'].widget.attrs.update({
            'placeholder': 'strong password atleast 8 characters',
        })
        self.fields['password2'].widget.attrs.update({
            'placeholder': 'repeat above password'
        })
        
        # Ensure no autofocus is set here (added following code because of automatically added autofocus class on username)
        for field_name, field in self.fields.items():
            if 'autofocus' in field.widget.attrs:
                del field.widget.attrs['autofocus']
    
    
        
    # validating first_name
    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if not re.match(r'^[A-Za-z\s]+$', first_name):
            raise ValidationError('Please enter a valid first name.')
        return first_name

    # validating last_name
    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if not re.match(r'^[A-Za-z\s]+$', last_name):
            raise ValidationError('Please enter a valid last name.')
        return last_name
    
    # validating username
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError('This username is already taken. Please choose another one.')
        return username
    
    # validating email
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError('This email is already in use. Please use a different email.')
        return email
    
# SIGNIN FORM
class SigninForm(AuthenticationForm):
    username = forms.CharField(required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)  
    
    class Meta:
        model = User
        fields = ('username', 'password')
        
    def __init__(self, *args, **kwargs):
        super(SigninForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'placeholder': 'enter correct username'
        })
        self.fields['password'].widget.attrs.update({
            'placeholder': 'enter correct password'
        })

# CHANGE PASSWORD FORM
class ChangePasswordForm(PasswordChangeForm):
    old_password = forms.CharField(
        label="Current Password",
        widget=forms.PasswordInput(attrs={'placeholder': 'enter your current password'})
    )
    new_password1 = forms.CharField(
        label="New Password",
        widget=forms.PasswordInput(attrs={'placeholder': 'enter your new password'})
    )
    new_password2 = forms.CharField(
        label="Confirm New Password",
        widget=forms.PasswordInput(attrs={'placeholder': 'repeat your new password'})
    )

# USER PROFILE FORM
class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email']

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['readonly'] = True

# USER PROFILE FORM
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['profession', 'profile_pic', 'about', 'linkedin', 'github', 'kaggle', 'X', 'other_link']

# UPDATE PROFILE FORM
class UpdateProfileForm(forms.ModelForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    username = forms.CharField(required=True, widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    email = forms.EmailField(required=True)


    class Meta:
        model = UserProfile
        fields = ['first_name', 'last_name', 'email', 'username', 'profession', 'profile_pic', 'about', 'linkedin', 'github', 'kaggle', 'X', 'other_link']
        widgets = {
            'profile_pic': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'about': forms.Textarea(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(UpdateProfileForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update({
            'placeholder': 'First Name'
        })
        self.fields['last_name'].widget.attrs.update({
            'placeholder': 'Last Name'
        })
        self.fields['username'].widget.attrs.update({
            'placeholder': 'Unique username'
        })
        self.fields['email'].widget.attrs.update({
            'placeholder': 'enter only valid email. example: demo@gmail.com'
        })
        self.fields['profession'].widget.attrs.update({
            'placeholder': 'enter your profession. example: Software Engineer'
        })
        self.fields['about'].help_text = 'Please write something about yourself so that other user know you better.'
        self.fields['linkedin'].widget.attrs.update({
            'placeholder': 'example: https://www.linkedin.com/in/yourusername'
        })
        self.fields['github'].widget.attrs.update({
            'placeholder': 'example: https://github.com/yourusername'
        })
        self.fields['kaggle'].widget.attrs.update({
            'placeholder': 'example: https://www.kaggle.com/yourusername'
        })
        self.fields['X'].widget.attrs.update({
            'placeholder': 'example: https://www.x.com/yourusername'
        })
        self.fields['other_link'].widget.attrs.update({
            'placeholder': 'example: https://yourwebsite.com'
        })

    # validating first_name
    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if not re.match(r'^[A-Za-z\s]+$', first_name):
            raise ValidationError('Please enter a valid first name.')
        return first_name

    # validating last_name
    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if not re.match(r'^[A-Za-z\s]+$', last_name):
            raise ValidationError('Please enter a valid last name.')
        return last_name
    
    # validating email
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.exclude(pk=self.instance.user.pk).filter(email=email).exists():
            raise ValidationError('This email is already in use. Please use a different email.')
        return email

    # validating profession
    def clean_profession(self):
        profession = self.cleaned_data.get('profession')
        if profession and not re.match(r'^[A-Za-z\s]+$', profession):
            raise ValidationError('Please enter a valid profession name.')
        return profession
    
    def clean_profile_pic(self):
        profile_pic = self.cleaned_data.get('profile_pic')

        if profile_pic:
            # Check the file extension
            file_extension = profile_pic.name.split('.')[-1].lower()
            allowed_extensions = ['jpg', 'jpeg', 'png']
            if file_extension not in allowed_extensions:
                raise ValidationError('Unsupported file format. Please upload a .jpg, .jpeg, or .png image.')

            # Check the file size (max 2 MB)
            max_size_mb = 2
            if profile_pic.size > max_size_mb * 1024 * 1024:
                raise ValidationError(f'File size exceeds {max_size_mb} MB limit.')

        return profile_pic