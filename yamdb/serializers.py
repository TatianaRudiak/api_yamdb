from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from rest_framework import serializers, status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import Category, Comment, Genre, Review, Title

User = get_user_model()


class UsersSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('first_name', 'last_name',
                  'username', 'bio', 'email',
                  'role')
        model = User


class EmailSerializer(serializers.Serializer):

    email = serializers.EmailField(required=True)


class TokenObtainPairNoPasswordSerializer(TokenObtainPairSerializer):

    confirmation_code = serializers.CharField(required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password'].required = False

    def validate(self, attrs):
        attrs.update({'password': ''})
        user = get_object_or_404(User, email=attrs.get('email'))
        confirmation_code = attrs.get('confirmation_code')
        if default_token_generator.check_token(user, confirmation_code):
            return Response({'detail': f'{confirmation_code} is not a valid confirmation code'},
                            status=status.HTTP_400_BAD_REQUEST)
        return super().validate(attrs)


class CategoriesSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug')
        model = Category


class GenresSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug')
        model = Genre


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
