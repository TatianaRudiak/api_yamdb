from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (CategoriesListCreateDestroyViewSet, CommentsViewSet,
                    GenresListCreateDestroyViewSet, ReviewViewSet,
                    TitlesViewSet, TokenObtainPairNoPasswordView,
                    TokenRefreshNoPasswordView, UsersViewSet)

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

token_urlpatterns = [
    path('token/', TokenRefreshNoPasswordView.as_view(),
         name='token_obtain_pair'),
    path('email/', TokenObtainPairNoPasswordView.as_view(),
         name='token_request_pair'),
]

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/auth/', include(token_urlpatterns)),
]
