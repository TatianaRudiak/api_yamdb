from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (AuthEmailConfirmation, CategoriesListCreateDestroyViewSet, CommentsViewSet,
                    GenresListCreateDestroyViewSet, ReviewViewSet,
                    TitlesViewSet,
                    TokenObtainPairNoPasswordView, UsersViewSet)

router_v1 = DefaultRouter()
router_v1.register('users', UsersViewSet,
                   basename='users')
router_v1.register('titles',
                   TitlesViewSet,
                   basename='titles')
router_v1.register('categories',
                   CategoriesListCreateDestroyViewSet,
                   basename='categories')
router_v1.register('genres',
                   GenresListCreateDestroyViewSet,
                   basename='genres')
router_v1.register(r'titles/(?P<title_id>\d+)/reviews',
                   ReviewViewSet,
                   basename='reviews')
router_v1.register(r'titles/(?P<title_id>\d+)/reviews/'
                   r'(?P<review_id>\d+)/comments',
                   CommentsViewSet,
                   basename='comments')

auth_urlpatterns = [
    path('token/', TokenObtainPairNoPasswordView.as_view(),
         name='token_obtain_pair'),
    path('email/', AuthEmailConfirmation.as_view(),
         name='auth_request_confirmation_code'),
]

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/auth/', include(auth_urlpatterns)),
]
