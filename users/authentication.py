from .models import MyUser
from django.contrib.auth.backends import BaseBackend


class UsernameAuthBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None):

        try:
            user = MyUser.objects.get(username=username)

            if user.check_password(password):
                return user
            return None
        except MyUser.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return MyUser.objects.get(pk=user_id)
        except MyUser.DoesNotExist:
            return None
