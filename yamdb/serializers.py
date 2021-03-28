from django.contrib.auth import get_user_model
from django.core.mail import mail_admins, send_mail
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.serializers import (TokenObtainPairSerializer,
                                                  TokenRefreshSerializer)

from .models import Category, Comment, Genre, Review, Title

User = get_user_model()


class UsersSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('first_name', 'last_name',
                  'username', 'bio', 'email',
                  'role')
        model = User


class TokenObtainPairNoPasswordSerializer(TokenObtainPairSerializer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password'].required = False

    def validate(self, attrs):
        attrs.update({'password': ''})
        data = super(TokenObtainPairNoPasswordSerializer,
                     self).validate(attrs)
        user = User.objects.get(email=self.context['request'].data.get('email')
                                )
        data = data["refresh"]
        send_mail(
            'Ваш confirmation_code',
            f'Ваш confirmation_code {data}.',
            mail_admins,
            [user.email],
            fail_silently=False,
        )
        return {'message': 'Вам отправлено письмо с confirmation_code'}


class TokenRefreshNoPassworSerializer(TokenRefreshSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['refresh'].required = False

    def validate(self, attrs):
        attrs.update({'refresh':
                      self.context['request'].data.get('confirmation_code')})
        return super().validate(attrs)


class CategoriesSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug')
        model = Category


class GenresSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug')
        model = Genre


class GenresField(serializers.SlugRelatedField):
    def to_internal_value(self, data):
        try:
            return self.get_queryset().get(**{self.slug_field: data})
        except (TypeError, ValueError):
            self.fail('invalid')

    def to_representation(self, value):
        return GenresSerializer(value).data


class CategoriesField(serializers.SlugRelatedField):
    def to_internal_value(self, data):
        try:
            return self.get_queryset().get(**{self.slug_field: data})
        except (TypeError, ValueError):
            self.fail('invalid')

    def to_representation(self, value):
        return CategoriesSerializer(value).data


class TitleReadSerializer(serializers.ModelSerializer):
    genre = GenresSerializer(many=True,
                             read_only=True)
    category = CategoriesSerializer(read_only=True)
    rating = serializers.FloatField()

    class Meta:
        fields = ('id', 'name', 'year', 'genre', 'rating',
                  'category', 'description')
        read_only_fields = ('id', 'rating')
        model = Title


class TitleWriteSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        many=True,
        required=False,
        queryset=Genre.objects.all()
    )
    category = serializers.SlugRelatedField(
        slug_field='slug',
        required=False,
        queryset=Category.objects.all()
    )

    class Meta:
        fields = ('id', 'name', 'year', 'genre',
                  'category', 'description')
        model = Title


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(read_only=True,
                                          slug_field='username')

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date',)
        read_only_fields = ('id', 'author', 'pub_date')
        model = Review

    def validate(self, data):
        if self.context['view'].action != 'create':
            return data
        title_id = self.context['view'].kwargs.get('title_id')
        user = self.context['request'].user
        if Review.objects.filter(author=user,
                                 title_id=title_id).exists():
            raise ValidationError('Отзыв уже был оставлен.')

        return data


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(slug_field='username',
                                          read_only=True)

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date',)
        read_only_fields = ('id', 'author', 'pub_date',)
        model = Comment
