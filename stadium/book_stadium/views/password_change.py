from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.shortcuts import redirect, render
from django.contrib.auth.forms import PasswordChangeForm
from django.views import View


class PasswordChange(View):
    form_class = PasswordChangeForm

    def get(self, request):
        form = self.form_class(request.user)
        context = {
            'form': form
        }
        return render(request, 'password_reset/password_change.html', context)

    def post(self, request):
        form = self.form_class(request.user, request.POST)

        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Thay đổi mật khẩu thành công!')
        return redirect('password_change')
