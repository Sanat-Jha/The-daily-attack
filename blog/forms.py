from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Post, Tag, UserProfile

class SignUpForm(UserCreationForm):
    # Remove the user_type field from the form
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        # Removed user_type from fields

class PostForm(forms.ModelForm):
    tags = forms.CharField(required=False, help_text='Enter tags separated by commas')
    
    class Meta:
        model = Post
        fields = ('title', 'content', 'status', 'tags')
        widgets = {
            'content': forms.Textarea(attrs={'class': 'richtext-editor'}),
        }
    
    def clean_tags(self):
        tags_string = self.cleaned_data.get('tags', '')
        tag_names = [tag.strip() for tag in tags_string.split(',') if tag.strip()]
        return tag_names
    
    def save(self, commit=True):
        post = super().save(commit=False)
        
        if commit:
            post.save()
            
            # Handle tags
            tag_names = self.cleaned_data.get('tags', [])
            post.tags.clear()
            
            for tag_name in tag_names:
                tag, created = Tag.objects.get_or_create(name=tag_name)
                post.tags.add(tag)
                
        return post