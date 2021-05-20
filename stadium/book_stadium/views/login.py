from django.contrib import messages
from django.shortcuts import redirect
from book_stadium.models import Roles, Stadium
from django.views import View
from django.contrib.auth import login
from book_stadium.myBackend import CustomAuthenticatedBackend

CustomAuthenticatedBackend = CustomAuthenticatedBackend()


class Login(View):
    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = CustomAuthenticatedBackend.authenticate(
            request, username=email, password=password)

        if user:
            login(request, user,
                  backend='book_stadium.myBackend.CustomAuthenticatedBackend')

            if user.role == Roles.OWNER:
                stadiums = Stadium.objects.filter(owner=request.user)

                if len(stadiums) == 0:
                    return redirect('create_stadium')
                else:
                    fisrt_stadium = stadiums.first()
                    return redirect('owner', fisrt_stadium.pk)
            else:
                if user.is_missing_information():
                    return redirect('user_profile', user.pk)
        else:
            messages.error(request, 'Tên đăng nhập hoặc mật khẩu không đúng!')
        return redirect('home')
