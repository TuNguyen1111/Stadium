from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import login

from book_stadium.forms import UserCreationForm
from book_stadium.models import Roles


class Register(View):
    form_class = UserCreationForm

    def post(self, request):
        create_user_form = self.form_class(request.POST)

        if create_user_form.is_valid():
            user = create_user_form.save()
            login(request, user,
                  backend='book_stadium.myBackend.CustomAuthenticatedBackend')

            if user.role == Roles.OWNER:
                return redirect('create_stadium')
            else:
                if user.is_missing_information():
                    return redirect('user_profile', user.pk)
                return redirect('home')
        else:
            context = {
                'register_form': create_user_form
            }
            return render(request, 'book_stadium/home.html', context)
