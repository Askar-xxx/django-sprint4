from django import forms
from .models import Post, Comment
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

User = get_user_model()


class EditUserFormTester(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email']
        labels = {
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            'username': 'Имя пользователя',
            'email': 'Email'
        }
        help_texts = {
            'username': 'Обязательное поле. '
            'Не более 150 символов. Только буквы, цифры и @/./+/-/_',
        }

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exclude(
                pk=self.instance.pk).exists():
            raise ValidationError(
                'Пользователь с таким именем уже существует.')
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exclude(
                pk=self.instance.pk).exists():
            raise ValidationError('Пользователь с таким email уже существует.')
        return email

    @staticmethod
    def init_create_form_from_item(
            item,
            form_class,
            model_adapter,
            file_data=None,
            **update_form_data):
        """Статический метод, который ожидает тест"""
        form = form_class(instance=item)
        if update_form_data:
            for field, value in update_form_data.items():
                form.initial[field] = value
        return form


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
