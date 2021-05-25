from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.shortcuts import redirect
from django.views import View

from book_stadium.myBackend import CustomAuthenticatedBackend
from book_stadium.models import Roles, Stadium

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
                first_stadium = Stadium.objects.filter(
                    owner=request.user).first()
                if first_stadium:
                    return redirect('owner', first_stadium.pk)
                else:
                    return redirect('create_stadium')
            else:
                if user.is_missing_information():
                    return redirect('user_profile', user.pk)
        else:
            messages.error(request, 'Tên đăng nhập hoặc mật khẩu không đúng!')
        return redirect('home')
