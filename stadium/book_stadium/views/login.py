from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.shortcuts import redirect
from django.views import View

from book_stadium.myBackend import CustomAuthenticatedBackend
from book_stadium.models import Roles, Stadium
from ..messages import *

CustomAuthenticatedBackend = CustomAuthenticatedBackend()


class Login(View):
    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(
            request, username=email, password=password)

        if user:
            login(request, user)
            if user.role == Roles.OWNER:
                first_stadium = Stadium.get_first_stadium_of_owner(request.user)
                if first_stadium:
                    return redirect('owner', first_stadium.pk)
                else:
                    return redirect('create_stadium')
            else:
                if user.is_missing_information():
                    return redirect('user_profile', user.pk)
        else:
            messages.error(request, WRONG_USER_OR_PASS)
        return redirect('book_stadium')
