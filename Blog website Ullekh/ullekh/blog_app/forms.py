from django import forms
from .models import BlogPost, Category
from tinymce.widgets import TinyMCE
from django.core.exceptions import ValidationError

class BlogPostForm(forms.ModelForm):
    body = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 30}))
    categories = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Enter categories separated by commas (e.g., Health, Technology)'}),
        help_text='You can provide at least 1 and at most 5 categories, separated by commas.'
    )
    image = forms.ImageField(required=False, help_text='You can add a header image for your blog else default will be applied.')

    class Meta:
        model = BlogPost
        fields = ['title', 'image', 'body', 'categories']
        
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Give a suitable title to your blog'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.initial['categories'] = ', '.join([cat.name for cat in self.instance.categories.all()])

    def clean_categories(self):
        categories = [cat.strip().lower() for cat in self.cleaned_data['categories'].split(',') if cat.strip()]
        if len(categories) < 1 or len(categories) > 5:
            raise forms.ValidationError("Please provide minimum 1 and maximum 5 categories.")
        return categories
    
    def clean_image(self):
        image = self.cleaned_data.get('image')

        if image:
            # Check the file extension
            file_extension = image.name.split('.')[-1].lower()
            allowed_extensions = ['jpg', 'jpeg', 'png']
            if file_extension not in allowed_extensions:
                raise ValidationError('Unsupported file format. Please upload a .jpg, .jpeg, or .png image.')

            # Check the file size (max 3 MB)
            max_size_mb = 3
            if image.size > max_size_mb * 1024 * 1024:
                raise ValidationError(f'File size exceeds {max_size_mb} MB limit.')

        return image

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
            self.save_categories(instance)
        return instance

    def save_categories(self, instance):
        instance.categories.clear()
        for category_name in self.cleaned_data['categories']:
            category, created = Category.objects.get_or_create(name=category_name)
            instance.categories.add(category)