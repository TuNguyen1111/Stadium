from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render, get_object_or_404
from django.views import View

from book_stadium.forms import UserProfileForm
from book_stadium.models import Stadium, User, TimeFrame


class UserProfile(LoginRequiredMixin, View):
    login_url = "home"
    form_class = UserProfileForm

    def get(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        stadiums_by_owner = Stadium.get_stadium_by_owner(request.user)
        form = self.form_class(instance=user)

        context = {
            'form': form,
            'fields': stadiums_by_owner,
        }
        return render(request, 'book_stadium/user_profile.html', context)

    def post(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        form = self.form_class(request.POST, instance=user)
        if form.is_valid():
            form.save()

        messages.success(request, 'Cập nhật thông tin thành công!')
        return redirect('user_profile', user.pk)
