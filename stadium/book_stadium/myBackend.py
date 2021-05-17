from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User

from .models import User

class CustomBackend(ModelBackend):
    # REVIEW: Viết docstring cho class này
    # Backend này để làm gì, có gì đặc biệt? (VD: cho phép authen bằng cả email và phone_number, v.v.)

    def authenticate(self, request, username=None, password=None):
        if '@' in username:
            kwargs = {'email': username}
        else:
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

