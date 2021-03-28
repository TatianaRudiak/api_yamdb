from datetime import datetime

from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class UserRole(models.TextChoices):
    USER = 'user', _('User')
    MODERATOR = 'moderator', _('Moderator')
    ADMIN = 'admin', _('Admin')


class CustomUser(AbstractUser):

    role = models.CharField(
        _('User role'),
        choices=UserRole.choices,
        default=UserRole.USER,
        max_length=40
    )
    email = models.EmailField(_('email address'),
                              unique=True)
    bio = models.TextField(_('about me'),
                           max_length=300,
                           null=True,
                           blank=True)

    REQUIRED_FIELDS = ['username']
    USERNAME_FIELD = 'email'

    def get_short_name(self):
        return self.email

    def __str__(self):
        return self.email

    class Meta:
        ordering = ['role']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Category(models.Model):
    name = models.CharField(verbose_name='Категория',
                            max_length=200)
    slug = models.SlugField(max_length=100,
                            unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-id']
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Genre(models.Model):
    name = models.CharField(verbose_name='Жанр',
                            max_length=200)
    slug = models.SlugField(max_length=100,
                            unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-id']
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Title(models.Model):
    name = models.CharField(verbose_name='Название произведения',
                            max_length=200)
    year = models.PositiveSmallIntegerField(verbose_name='Дата выхода',
                                            validators=[MaxValueValidator
                                                        (datetime.now().year)])
    category = models.ForeignKey(Category,
                                 verbose_name='Категория',
                                 on_delete=models.SET_NULL,
                                 related_name='titles',
                                 blank=True,
                                 null=True,
                                 help_text='Выберите категорию.')
    description = models.TextField(verbose_name='Описание',
                                   max_length=250)
    genre = models.ManyToManyField(Genre,
                                   verbose_name='Жанр',
                                   related_name='titles',
                                   blank=True, )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-id']
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'


class Review(models.Model):
    title = models.ForeignKey(Title,
                              on_delete=models.CASCADE,
                              related_name='reviews',
                              null=False)
    text = models.TextField()
    author = models.ForeignKey(CustomUser,
                               on_delete=models.CASCADE,
                               related_name='reviews',
                               null=False)
    score = models.PositiveIntegerField(
        'Оценка', null=False,
        validators=[MinValueValidator(1, 'Не меньше 1'),
                    MaxValueValidator(10, 'Не больше 10')]
    )
    pub_date = models.DateTimeField('Дата публикации',
                                    auto_now_add=True,
                                    db_index=True)

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'


class Comment(models.Model):
    title = models.ForeignKey(Title,
                              on_delete=models.CASCADE,
                              related_name='comments',
                              null=False)
    review = models.ForeignKey(Review,
                               on_delete=models.CASCADE,
                               related_name='comments',
                               null=False)
    text = models.TextField(null=False)
    author = models.ForeignKey(CustomUser,
                               on_delete=models.CASCADE,
                               related_name='comments',
                               null=False)
    pub_date = models.DateTimeField('Дата публикации',
                                    auto_now_add=True,
                                    db_index=True)

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
