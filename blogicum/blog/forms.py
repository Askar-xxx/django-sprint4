from django import forms
from .models import Post, Comment
from django.utils import timezone
from django.contrib.auth import get_user_model

User = get_user_model()


class EditUserFormTester(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email']
        exclude = ('password',)


class PostForm(forms.ModelForm):
    pub_date = forms.DateTimeField(
        initial=timezone.now,
        required=True,
        widget=forms.DateTimeInput(
            attrs={
                'type': 'datetime-local',
            },
            format='%Y-%m-%dT%H:%M',
        ),
    )

    class Meta:
        model = Post
        fields = (
            'title',
            'image',
            'text',
            'pub_date',
            'location',
            'category',
            'is_published',
        )


class CommentCreateForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)
