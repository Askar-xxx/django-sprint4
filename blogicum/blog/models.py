from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import Truncator
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from .constants import (
    POST_TITLE_MAX_LENGTH_TITLE,
    CATEGORY_SLUG_MAX_LENGTH,
    CATEGORY_TITLE_MAX_LENGTH,
    LOCATION_NAME_MAX_LENGTH
)

User = get_user_model()


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(
            pub_date__lte=timezone.now(),
            is_published=True,
            category__is_published=True
        ).select_related('category', 'location', 'author')


class BaseModel(models.Model):
    is_published = models.BooleanField(
        _('Опубликовано'),
        default=True,
        help_text=_('Снимите галочку, чтобы скрыть публикацию.')
    )
    created_at = models.DateTimeField(
        _('Добавлено'),
        auto_now_add=True
    )

    class Meta:
        abstract = True


class Location(BaseModel):
    name = models.CharField(
        _('Название места'),
        max_length=LOCATION_NAME_MAX_LENGTH,
        unique=True
    )

    class Meta:
        verbose_name = _('местоположение')
        verbose_name_plural = _('Местоположения')
        ordering = ('name',)

    def __str__(self):
        return Truncator(self.name).chars(50)


class Category(BaseModel):
    title = models.CharField(
        _('Заголовок'),
        max_length=CATEGORY_TITLE_MAX_LENGTH
    )
    description = models.TextField(_('Описание'))
    slug = models.SlugField(
        _('Идентификатор'),
        max_length=CATEGORY_SLUG_MAX_LENGTH,
        unique=True,
        help_text=_('Идентификатор страницы для URL')
    )

    class Meta:
        verbose_name = _('категория')
        verbose_name_plural = _('Категории')
        ordering = ('title',)

    def __str__(self):
        return Truncator(self.title).chars(50)


class Post(BaseModel):
    title = models.CharField(
        _('Заголовок'), max_length=POST_TITLE_MAX_LENGTH_TITLE)
    text = models.TextField(_('Текст'))
    pub_date = models.DateTimeField(
        _('Дата и время публикации'),
        help_text=_('Если установить дату и время в будущем '
                    '— можно делать отложенные публикации.')
    )
    author = models.ForeignKey(
        User,
        verbose_name=_('Автор публикации'),
        on_delete=models.CASCADE,
        related_name='posts'
    )
    location = models.ForeignKey(
        Location,
        verbose_name=_('Местоположение'),
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    category = models.ForeignKey(
        Category,
        verbose_name=_('Категория'),
        on_delete=models.SET_NULL,
        null=True,
        related_name='category_posts'
    )
    image = models.ImageField(
        _('Изображение'),
        upload_to='posts_images/',
        blank=True
    )

    objects = models.Manager()
    published = PublishedManager()

    class Meta:
        verbose_name = _('публикация')
        verbose_name_plural = _('Публикации')
        ordering = ('-pub_date',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:post_detail', kwargs={'post_id': self.pk})


class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    text = models.TextField(_('Текст'))
    created_at = models.DateTimeField(_('Дата создания'), auto_now_add=True)
    is_edited = models.BooleanField(_('Отредактировано'), default=False)

    class Meta:
        verbose_name = _('комментарий')
        verbose_name_plural = _('Комментарии')
        ordering = ('created_at',)

    def __str__(self):
        return f'Комментарий {self.author} к посту {self.post}'
