from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User

from .models import User

class CustomBackend(ModelBackend):
    def authenticate(self, username=None, password=None):
        if '@' in username:
            print(username)
            kwargs = {'email': username}
        else:
            print(username)
            kwargs = {'phone_number': username}
        try:
            user = User.objects.get(**kwargs)
            if user.check_password(password):
                user = user
                return user
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None