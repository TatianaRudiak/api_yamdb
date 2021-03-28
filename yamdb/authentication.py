from django.contrib.auth import get_user_model
from django.contrib.auth.backends import BaseBackend

from yamdb.models import UserRole

User = get_user_model()


class AuthenticationWithoutPassword(BaseBackend):

    def authenticate(self, request, username=None, password=None, **kwargs):
        email = kwargs.get('email')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            user = User(email=email)
            user.username = user.email
            user.save()
        return user
