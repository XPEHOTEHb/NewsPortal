from django import forms
from .models import Post
from django.core.validators import ValidationError


class PostForm(forms.ModelForm):
    #description = forms.CharField(min_length=20)

    class Meta:
        model = Post
        fields = [
            'author',
            'title',
            'postCategory',
            'text',
        ]

"""    def clean(self):
        cleaned_data = super().clean()
        description = cleaned_data.get('decription')
        name = cleaned_data.get('name')
        if name == description:
            raise ValidationError({'name': "Name can;t be equal description"})

        return cleaned_data"""
