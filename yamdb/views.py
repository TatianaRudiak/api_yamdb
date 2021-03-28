from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import mail_admins, send_mail
from django.db.models import Avg
from django_filters import FilterSet
from django_filters.filters import CharFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, status
from rest_framework.decorators import action
from rest_framework.generics import CreateAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework_simplejwt.views import TokenViewBase

from .models import Category, Comment, Genre, Review, Title
from .permissions import IsAdmin, IsAdminOrReadOnly, IsAuthorOrModerator
from .serializers import (CategoriesSerializer, CommentSerializer,
                          EmailSerializer, GenresSerializer, ReviewSerializer,
                          TitleReadSerializer, TitleWriteSerializer,
                          TokenObtainPairNoPasswordSerializer,
                          UsersSerializer)

User = get_user_model()


class MixinsViewSet(mixins.ListModelMixin,
                    mixins.DestroyModelMixin,
                    mixins.CreateModelMixin,
                    GenericViewSet):
    pass


class AuthEmailConfirmation(CreateAPIView):

    def post(self, request, *args, **kwargs):
        serializer = EmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = User.objects.get(email=serializer.validated_data.get('email'))
        token = default_token_generator.make_token(user)
        subject = 'Confirmation code'
        message = {
            'user': user,
            'confirmation_code': token,
        }
        send_mail(subject, message, mail_admins, [user.email], fail_silently=False)
        return Response({'message': message}, status=status.HTTP_200_OK)


class TokenObtainPairNoPasswordView(TokenViewBase):
    serializer_class = TokenObtainPairNoPasswordSerializer


class UsersViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UsersSerializer
    permission_classes = [IsAuthenticated, IsAdmin]
    lookup_field = 'username'

    @action(detail=False, methods=['GET', 'PATCH'],
            permission_classes=[IsAuthenticated])
    def me(self, request):
        instance = request.user
        serializer = self.get_serializer(instance)
        if request.method == 'PATCH':
            serializer = self.get_serializer(instance,
                                             data=request.data,
                                             partial=True)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
        return Response(serializer.data)


class TitlesFilter(FilterSet):
    genre = CharFilter(field_name='genre__slug',
                       lookup_expr='icontains')
    category = CharFilter(field_name='category__slug',
                          lookup_expr='icontains')
    name = CharFilter(field_name='name',
                      lookup_expr='icontains')

    class Meta:
        model = Title
        fields = ['year']


class TitlesViewSet(ModelViewSet):
    queryset = Title.objects.all().annotate(rating=Avg('reviews__score'))
    permission_classes = [IsAdminOrReadOnly, ]
    filter_backends = [DjangoFilterBackend]
    filterset_class = TitlesFilter

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitleReadSerializer
        return TitleWriteSerializer


class CategoriesListCreateDestroyViewSet(MixinsViewSet):
    queryset = Category.objects.all()
    serializer_class = CategoriesSerializer
    permission_classes = [IsAdminOrReadOnly, ]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', ]
    lookup_field = 'slug'


class GenresListCreateDestroyViewSet(MixinsViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenresSerializer
    permission_classes = [IsAdminOrReadOnly, ]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', ]
    lookup_field = 'slug'


class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [IsAdminOrReadOnly | IsAuthorOrModerator, ]

    def get_queryset(self):
        return self.get_current_title().reviews.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user,
                        title=self.get_current_title())

    def get_current_title(self):
        return get_object_or_404(Title,
                                 pk=self.kwargs.get('title_id'))


class CommentsViewSet(ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAdminOrReadOnly | IsAuthorOrModerator]

    def get_queryset(self):
        title = get_object_or_404(Title,
                                  pk=self.kwargs.get('title_id'))
        review = get_object_or_404(Review,
                                   pk=self.kwargs.get('review_id'),
                                   title__id=self.kwargs.get('title_id'))
        queryset = Comment.objects.filter(title=title,
                                          review=review).all()
        return queryset

    def perform_create(self, serializer):
        title = get_object_or_404(Title,
                                  pk=self.kwargs.get('title_id'))
        review = get_object_or_404(Review,
                                   pk=self.kwargs.get('review_id'),
                                   title__id=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user,
                        title=title,
                        review=review)
