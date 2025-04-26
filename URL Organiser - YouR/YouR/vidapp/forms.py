from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import VideoBookmark, Tag

class RegisterForm(UserCreationForm):
    email = forms.EmailField()
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class VideoBookmarkForm(forms.ModelForm):
    title = forms.CharField(required=False)  # Make title not required
    tags_input = forms.CharField(
        required=False, 
        help_text="Add tags separated by commas"
    )
    
    class Meta:
        model = VideoBookmark
        fields = ['url', 'title', 'description', 'thumbnail_url']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }
    
    def save(self, commit=True, user=None):
        instance = super().save(commit=False)
        if user:
            instance.user = user
        
        if commit:
            instance.save()
            
            # Process tags
            if self.cleaned_data.get('tags_input'):
                tag_names = [t.strip() for t in self.cleaned_data['tags_input'].split(',') if t.strip()]
                for tag_name in tag_names:
                    tag, created = Tag.objects.get_or_create(name=tag_name.lower())
                    instance.tags.add(tag)
        
        return instance

class SearchForm(forms.Form):
    query = forms.CharField(required=False, label='Search')
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple
    )
    source = forms.ChoiceField(
        choices=[
            ('', 'All Sources'),
            ('YouTube', 'YouTube'),
            ('Instagram', 'Instagram'),
            ('LinkedIn', 'LinkedIn'),
            ('X', 'X'),
            ('Threads', 'Threads'),
            ('Vimeo', 'Vimeo'),
            ('Other', 'Other'),
        ],
        required=False
    )